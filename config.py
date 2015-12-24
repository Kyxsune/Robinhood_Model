from __future__ import absolute_import
from pytz import timezone
from celery.schedules import crontab

# Celery Config File

## Broker settings.
BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('Task_Manager.DataGather.Data_func', )

## Using the database to store task state and results.
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_RESULT_PERSISTENT = True

#Use Eastern Timezone
CELERY_TIMEZONE = timezone('US/Eastern').zone

#Celery Beat Scheduler

CELERYBEAT_SCHEDULE = {
    'Query-Yahoo':{
        'task':'Task_Manager.DataGather.Data_func.post_daily_collection',
        'schedule': crontab(
            hour='9-16',
            day_of_week='mon-fri'
        ),
        'args': ("stox"), # Have to determine DB name
    },
    'Update-History':{
        'task':'Task_Manager.DataGather.Data_func.Historical_table',
        'schedule': crontab(
            hour='9-16',
            day_of_week='mon-fri',
            minute='*/10',
        ),
        'args': ("stox"), # Have to determine DB name
    },
    'Update Stock Table':{
        'task':'Task_Manager.DataGather.Data_func.update_stock_table',
        'schedule': crontab(
            hour='9-16',
            day_of_week='mon-fri'
        ),
        'args': ("stox"), # Have to determine DB name
    },
    'Clear Daily Table':{
        'task':'Data_func.clear_daily_collection',
        'schedule': crontab(
            day_of_week='mon-fri',
            minute=0,
            hour=9,
        ),
        'args': ("stox"), # Have to determine DB name
    },
}

# Error Emails
CELERY_SEND_TASK_ERROR_EMAILS = False



