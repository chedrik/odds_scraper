import time
from rq import get_current_job
from flask import current_app
from scraper_interface import initialize_databases, fetch_all_odds
import os


def launch_task(func_name, *args, **kwargs):
    """
    Wrapper for queueing a rq task
    :param func_name: string name of function to pass to rq worker
    :param args: args
    :param kwargs: kwargs
    :return: rq_job ptr
    """
    rq_job = current_app.task_queue.enqueue('app.tasks.' + func_name, *args, **kwargs)
    return rq_job


def fetch_odds():
    """
    Wrapper for entire odds fetching and pausing, to run in background worker during server uptime.
    :return: void
    """
    try:
        while True:
            job = get_current_job()
            job.save_meta()  # needed?
            client, db = initialize_databases(os.environ.get('MONGODB_URI')or None)
            job.meta['status'] = 'fetching'
            print 'fetching'
            fetch_all_odds(db)
            print 'waiting'
            job.meta['status'] = 'waiting'
            time.sleep(float(os.environ.get('FETCH_TIME') or 300.0))
    except Exception as e: print(e)
        # app.logger.error('Unhandled exception in RQ', exc_info=sys.exc_info())  # TODO: figure out how to get app context
