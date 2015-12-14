#This is the file for the celery app
from __future__ import absolute_import

from celery import Celery

app = Celery('Task_Manager',
             broker="amqp://",
             backend='amqp://',
             include=['DataGather.Data_func'])

#app.conf.update(
    # This is where configureations go
#)

if __name__ == '__main__':
    app.start()