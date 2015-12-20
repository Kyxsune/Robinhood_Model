#This is the file for the celery app
from __future__ import absolute_import
from flask import Flask
from celery import Celery
app = Flask(__name__)
celery = Celery(app.name)
celery.config_from_object('config')

if __name__ == '__main__':
    celery.start()