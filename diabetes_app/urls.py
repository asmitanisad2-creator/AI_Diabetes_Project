from django.urls import path
from . import views

urlpatterns = [

    # Home
    path("", views.home, name="home"),

    # Authentication
    path("login/", views.login_user, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),

    # Patient Pages
    path("dashboard/", views.dashboard, name="dashboard"),
    path("predict/", views.predict, name="predict"),
    path("history/", views.history, name="history"),
    path("profile/", views.profile, name="profile"),

    # Other Pages
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path(
    "result/<int:patient_id>/",
    views.result,
    name="result"
    ),
    path(
    "download-pdf/<int:patient_id>/",
    views.download_pdf,
    name="download_pdf"
    ),

path(
    "delete-report/<int:patient_id>/",
    views.delete_report,
    name="delete_report"
),

path("edit-profile/", views.edit_profile, name="edit_profile"),

path(
    "change-password/",
    views.change_password,
    name="change_password"
),

path("forgot-password/", views.forgot_password, name="forgot_password"),

path("verify-otp/", views.verify_otp, name="verify_otp"),

path("reset-password/", views.reset_password, name="reset_password"),
]