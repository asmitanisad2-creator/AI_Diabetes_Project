# GlucoSense social login setup

The login page now uses django-allauth for Google, GitHub, and LinkedIn.
Successful social authentication is sent directly to `/dashboard/`. Google is configured to show the account chooser before completing sign-in.

## Google

The supplied `db.sqlite3` already contains the Google SocialApp used by this v3 project. In Google Cloud, the local callback must match:

`http://127.0.0.1:8000/accounts/google/login/callback/`

The project also requests `prompt=select_account` so the Google account chooser is shown.

## GitHub

Create an OAuth app and use this callback:

`http://127.0.0.1:8000/accounts/github/login/callback/`

Set these environment variables before starting Django:

`GITHUB_CLIENT_ID=...`

`GITHUB_CLIENT_SECRET=...`

## LinkedIn

GlucoSense uses LinkedIn's current OpenID Connect provider through django-allauth. The callback is:

`http://127.0.0.1:8000/accounts/oidc/linkedin/login/callback/`

Set:

`LINKEDIN_CLIENT_ID=...`

`LINKEDIN_CLIENT_SECRET=...`

For production, replace `127.0.0.1:8000` with the real HTTPS domain and register the matching callback URL with each provider.
