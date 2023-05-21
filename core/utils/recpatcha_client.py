import requests
from google.oauth2.credentials import Credentials


def verify_recaptcha(response_token: str, secret_key: str) -> bool:
    # Define the reCAPTCHA API endpoint URL
    recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"

    # Verify the reCAPTCHA response token using the reCAPTCHA API
    try:
        data = {
            "secret": secret_key,
            "response": response_token
        }
        response = requests.post(recaptcha_url, data=data)
        response.raise_for_status()
        result = response.json()
        if result["success"] and result["score"] >= 0.5:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False