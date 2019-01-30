from rq import get_current_job
from flask import current_app
from scraper_interface import initialize_databases, fetch_all_odds


def launch_task(func_name, *args, **kwargs):
    rq_job = current_app.task_queue.enqueue('app.tasks.' + func_name, *args, **kwargs)
    return rq_job


def fetch_odds():
    job = get_current_job()
    job.save_meta()  # needed?
    client, db = initialize_databases()
    job.meta['status'] = 'fetching'
    print 'fetching'
    fetch_all_odds(db)
    print 'waiting'
    job.meta['status'] = 'waiting'
