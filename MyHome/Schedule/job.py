import traceback
from django.conf import settings
import requests
import json
import random
from datetime import datetime
import sys
import os

timeZone = datetime.now()

def schedule_api():
    print('Scheduling')
    print('Now : %s' %timeZone.second)

def kafka_producer():
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    from Kafka import kafka_Producer
    producer = kafka_Producer.producer
    
    try:
        data={'messages': 'test from django'}
        response = producer.send('exam-topic', value=data).get()
        producer.flush()
        print(response)
    except:
        traceback.print_exc()