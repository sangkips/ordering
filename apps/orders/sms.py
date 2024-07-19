import requests
from decouple import Config
config = Config()

url = "https://api.sandbox.africastalking.com/version1/messaging"

headers = {
    "ApiKey": config("AFRICASTALKING_API_KEY"),
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
}

data = {
    "username": config("AFRICASTALKING_USERNAME"),
    "from": config("SMS_SENDER"),
    "message": "Thank you for your order. We will reach out to you shortly.",
    "to": "+254729640480",
}


def make_post_request():
    response = requests.post(url=url, headers=headers, data=data)
    return response
