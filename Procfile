web: newrelic-admin run-program gunicorn odds_scraper:app
worker: rq worker -u $REDIS_URL odds-tasks