#This is the file for the celery app
from __future__ import absolute_import
from celery import Celery

celery = Celery(include=[
			 'Task_Manager.DataGather.Data_func'])
celery.config_from_object('config')

if __name__ == '__main__':
    celery.start()
