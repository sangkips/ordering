### Ordering APP

VERSIONS:

PYTHON 3.12

Prerequisites:
1. Make sure you have postgresql installed on your machine

2. Create a database that you will replace it on the .env

How To Run:
1. Download all requirements from the requirements.txt file
    ``` pip install -r requirements.txt```

2. Copy contents of .env.example to your .env file and replace with the respective details
    ``` cp .env.example .env```


3. Run migrations per app

- For auth_app app

    ``` python manage.py makemigrations auth_app```

    ``` python manage.py migrate auth_app```

 - Orders app

    ``` python manage.py makemigrations orders```

    ``` python manage.py migrate orders```

- Run migrations for the whole app to apply database changes for other installed apps

    ``` python manage.py migrate```

- Create superuser account

    ``` python manage.py createsuperuser```
4. Run the server locally

    ```python manage.py runserver```

#### To view Api endpoints:

On Your browser enter

[127.0.0.1:8000/developer/docs](http://127.0.0.1:8000/developer/docs)


To run tests:

```python manage.py test```
or

```make test```

Or run specific app tests:

```python manage.py test app_name```

HOW TO TEST STEP-BY-STEP:

1. Use this endpoint to register as a user in the platform
- ```http://127.0.0.1:8000/api/account/create/customer/```
   
2. Use the credentials you created above to obtain access token to allow you access the API services.

- ```http://127.0.0.1:8000/auth/jwt/create/```


3. Copy the access token and paste on the authorization button with Prefix "Bearer .....".

4. Once logged in start by creating the Item using the following endpoint

- ```http://127.0.0.1:8000/api/order/products/```

5. Create the Order by associating with the customer

- ```http://127.0.0.1:8000/api/order/orders/```

6. Lastly create and order line, contains the details of the order

- ```http://127.0.0.1:8000/api/order/orders/detail```

### Test SMS delivery with Africastalking API

To simulate sending SMS using Africastalking API, you need to have an account, follow the following steps to create one

1. Go to the following link and create the account
- ```https://account.africastalking.com/auth/login?next=%2F```

2. Request api key by following this guide
```https://help.africastalking.com/en/articles/1361037-how-do-i-generate-an-api-key```

3. Go to sandbox environment
- SMS
- Create shortcodes
4. To see your sms in action use `Launch simulator` and insert your phone number.
5. Use ngrok or local tunnel to simulate production environment as you will not be able to send an sms on a local environment.

Example of what to have in order to send sms
```
AFRICASTALKING_USERNAME=sandbox
AFRICASTALKING_API_KEY= your api key
SMS_SENDER= your shortcode
SMS_RECIPIENT= your phone number
```





 

