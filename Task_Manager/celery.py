#This is the file for the celery app
from __future__ import absolute_import
from Task_Manager import config
from celery import Celery

app = Celery()

app.config_from_object(config)

if __name__ == '__main__':
    app.start()