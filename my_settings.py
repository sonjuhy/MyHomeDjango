import os
from dotenv import load_dotenv

# load .local_env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.local_env'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}
SECRET_KEY = os.getenv('SECRET_KEY')
