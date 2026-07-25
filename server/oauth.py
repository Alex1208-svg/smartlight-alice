from flask import request, redirect, jsonify

def authorize():
    redirect_uri = request.args.get("redirect_uri")
    state = request.args.get("state")

    return redirect(f"{redirect_uri}?code=123456&state={state}")

def token():
    return jsonify({
        "access_token": "token123",
        "token_type": "bearer",
        "expires_in": 31536000
    })
