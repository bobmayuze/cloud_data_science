from celery import Celery, Task 
from pymongo import MongoClient
from bson.objectid import ObjectId
import time

import config
import task_inventory

app = Celery('task')
app.config_from_object(config)

db_connection = MongoClient("mongodb://application_user:application_user_pass@mongo_result_backend:27017/?authSource=TMS_DB", connect=False)['TMS_DB']
class CallbackTask(Task):
    def __init__(self):
        self.db = db_connection
    
    def on_success(self, retval, task_id, args, kwargs):
        print("TASK {} SUCCEEDED".format(task_id))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print("TASK {} FAILED".format(task_id))


        

# different callback functions for each task
@app.task(base=CallbackTask)
def sample_task(num_of_digist):
    r = task_inventory.print_pi(num_of_digist)
    time.sleep(5)
    return r

