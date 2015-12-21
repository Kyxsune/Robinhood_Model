#This is the file for the celery app
from __future__ import absolute_import
from celery import Celery
app = Celery('Task_Manager')
app.config_from_object('config')

if __name__ == '__main__':
    app.start()