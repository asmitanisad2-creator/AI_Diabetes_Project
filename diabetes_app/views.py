from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import darkblue, green, red
from reportlab.lib.units import inch

import joblib
import numpy as np

from .models import Patient, Contact
from django.db.models import Count
from datetime import datetime

# Load Machine Learning Model
model = joblib.load("model/diabetes_model.pkl")
scaler = joblib.load("model/scaler.pkl")

# ==========================
# Home Page
# ==========================
def home(request):
    return render(request, "home.html")


# ==========================
# Prediction Page
# ==========================
@login_required(login_url='login')
def predict(request):

    if request.method == "POST":

        # Get values from form
        name = request.POST["name"]
        pregnancies = int(request.POST["pregnancies"])
        glucose = float(request.POST["glucose"])
        blood_pressure = float(request.POST["blood_pressure"])
        skin_thickness = float(request.POST["skin_thickness"])
        insulin = float(request.POST["insulin"])
        bmi = float(request.POST["bmi"])
        diabetes_pedigree = float(request.POST["diabetes_pedigree"])
        age = int(request.POST["age"])

        # Prepare input for ML Model
        features = np.array([[
            pregnancies,
            glucose,
            blood_pressure,
            skin_thickness,
            insulin,
            bmi,
            diabetes_pedigree,
            age
        ]])

        scaled_features = scaler.transform(features)

        # Predict
        result = model.predict(scaled_features)

        # Prediction Confidence
        confidence = round(
            max(model.predict_proba(scaled_features)[0]) * 100,
            2
        )
        print("Confidence:", confidence)

        # Prediction Result
        if result[0] == 1:
            prediction = "Diabetic"
        else:
            prediction = "Not Diabetic"

        # Save data into database
        patient = Patient.objects.create(
            user=request.user,
            name=name,
            age=age,
            pregnancies=pregnancies,
            glucose=glucose,
            blood_pressure=blood_pressure,
            skin_thickness=skin_thickness,
            insulin=insulin,
            bmi=bmi,
            diabetes_pedigree=diabetes_pedigree,
            prediction=prediction,
            confidence=confidence,
        )

        # Redirect to Result Page
        return redirect("result", patient_id=patient.id)

    # Show prediction form on GET request
    return render(request, "predict.html")
# ==========================
# Result Page
# ==========================

@login_required(login_url='login')
def result(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id,
        user=request.user
    )

    return render(
    request,
    "result.html",
    {
        "patient": patient,
        "today": datetime.now(),
    }
    )

@login_required(login_url='login')
def download_pdf(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id,
        user=request.user
    )

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="Diabetes_Report_{patient.id}.pdf"'
    )

    doc = SimpleDocTemplate(response)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER
    title.textColor = darkblue

    heading = styles["Heading2"]

    normal = styles["BodyText"]

    story = []

    story.append(Paragraph("AI Diabetes Prediction Report", title))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("<b>Patient Information</b>", heading))
    story.append(Paragraph(f"Name : {patient.name}", normal))
    story.append(Paragraph(f"Age : {patient.age}", normal))
    story.append(Paragraph(f"Date : {patient.created_at.strftime('%d-%m-%Y %I:%M %p')}", normal))

    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("<b>Medical Values</b>", heading))
    story.append(Paragraph(f"Pregnancies : {patient.pregnancies}", normal))
    story.append(Paragraph(f"Glucose : {patient.glucose}", normal))
    story.append(Paragraph(f"Blood Pressure : {patient.blood_pressure}", normal))
    story.append(Paragraph(f"Skin Thickness : {patient.skin_thickness}", normal))
    story.append(Paragraph(f"Insulin : {patient.insulin}", normal))
    story.append(Paragraph(f"BMI : {patient.bmi}", normal))
    story.append(Paragraph(f"Diabetes Pedigree : {patient.diabetes_pedigree}", normal))

    story.append(Spacer(1, 0.25 * inch))

    if patient.prediction == "Diabetic":
        prediction = Paragraph(
            "<font color='red'><b>Prediction : HIGH RISK (Diabetic)</b></font>",
            heading
        )
    else:
        prediction = Paragraph(
            "<font color='green'><b>Prediction : LOW RISK (Not Diabetic)</b></font>",
            heading
        )

    story.append(prediction)

    story.append(
        Paragraph(
            f"Confidence : {patient.confidence}%",
            normal
        )
    )

    story.append(Spacer(1, 0.4 * inch))

    story.append(
        Paragraph(
            "<b>Generated by AI-Based Early Diabetes Prediction System</b>",
            normal
        )
    )

    doc.build(story)

    return response


# ==========================
# About Page
# ==========================
def about(request):
    return render(request, "about.html")


# ==========================
# Contact Page
# ==========================
def contact(request):

    if request.method == "POST":

        Contact.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            subject=request.POST["subject"],
            message=request.POST["message"],
        )

        return render(request, "contact.html", {
            "success": "Your message has been sent successfully!"
        })

    return render(request, "contact.html")
# ==========================
# History Page
# ==========================
@login_required(login_url='login')
def history(request):

    search = request.GET.get("search", "")

    patients = Patient.objects.filter(
        user=request.user
    ).order_by("-created_at")

    if search:
        patients = patients.filter(
            name__icontains=search
        )

    context = {
        "patients": patients,
        "search": search,
        "total": patients.count(),
    }

    return render(request, "history.html", context)

@login_required(login_url='login')
def delete_report(request, patient_id):

    patient = get_object_or_404(
        Patient,
        id=patient_id,
        user=request.user
    )

    patient.delete()

    messages.success(request, "Report deleted successfully.")

    return redirect("history")
# ==========================
# Dashboard
# ==========================

@login_required(login_url='login')
def dashboard(request):

    # Logged-in user's predictions only
    patients = Patient.objects.filter(
        user=request.user
    ).order_by("-created_at")

    # Statistics
    total = patients.count()

    healthy = patients.filter(
        prediction="Not Diabetic"
    ).count()

    high_risk = patients.filter(
        prediction="Diabetic"
    ).count()

    # Latest Prediction
    latest_prediction = patients.first()

    # Last 5 Predictions
    recent_patients = patients[:5]

    context = {

        "total": total,

        "healthy": healthy,

        "high_risk": high_risk,

        "latest_prediction": latest_prediction,

        "recent_patients": recent_patients,

    }

    return render(
        request,
        "dashboard.html",
        context
    )

# ---------------- LOGIN ----------------

def login_user(request):

    if request.method == "POST":

        username = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        else:

            messages.error(request, "Invalid Email or Password")

    return render(request, "login.html")


# ---------------- REGISTER ----------------

def register(request):

    if request.method == "POST":

        username = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():

            messages.error(request, "Email already registered.")

        else:

            User.objects.create_user(
                username=username,
                email=username,
                password=password
            )

            messages.success(request, "Registration Successful")

            return redirect("login")

    return render(request, "register.html")


# ---------------- LOGOUT ----------------

def logout_user(request):

    logout(request)

    return redirect("login")

from django.contrib import messages

@login_required(login_url='login')
def profile(request):

    user = request.user

    if request.method == "POST":

        user.username = request.POST.get("username")
        user.email = request.POST.get("email")

        user.save()

        messages.success(request, "Profile updated successfully!")

        return redirect("profile")

    patients = Patient.objects.filter(user=user).order_by("-created_at")

    latest = patients.first()

    context = {

        "total": patients.count(),

        "healthy": patients.filter(prediction="Not Diabetic").count(),

        "high_risk": patients.filter(prediction="Diabetic").count(),

        "latest": latest,

    }

    return render(request, "profile.html", context)