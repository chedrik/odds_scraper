import time
from rq import get_current_job
from flask import current_app


def example(seconds):
    job = get_current_job()
    print('Starting task')
    for i in range(seconds):
        job.meta['progress'] = 100.0 * i / seconds
        job.save_meta()
        print(i)
        time.sleep(1)
    job.meta['progress'] = 100
    job.save_meta()
    print('Task completed')


def launch_task(func_name, *args, **kwargs):
    rq_job = current_app.task_queue.enqueue('app.tasks.' + func_name, *args, **kwargs)
    return rq_job