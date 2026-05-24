import os
from dotenv import load_dotenv

# load .local_env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.local_env'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME') or 'myhomedb',
        'USER': os.getenv('DATABASE_USER') or 'root',
        'PASSWORD': os.getenv('DATABASE_PASSWORD') or 'password',
        'HOST': os.getenv('DATABASE_HOST') or '192.168.0.254',
        'PORT': os.getenv('DATABASE_PORT') or '3306',
    }
}
SECRET_KEY = os.getenv('SECRET_KEY') or 'django-insecure-your-secret-key-here'
