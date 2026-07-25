from flask import redirect

def authorize():
    return redirect("/success")

def token():
    return {
        "access_token": "smartlight_token",
        "token_type": "bearer",
        "expires_in": 31536000,
        "refresh_token": "refresh_token"
    }
