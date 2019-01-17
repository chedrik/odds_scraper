from flask import render_template, current_app, request
from app.errors import bp
from flask_login import current_user


@bp.app_errorhandler(404)
def not_found_error(error):
    if current_user.is_authenticated:
        str = current_user.email
    else:
        str = 'Anonymous user'
    current_app.logger.info(str + ' attempted to access the following URL and failed: ' + request.url)
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    # db session rollback? TODO: see about this in pymongo
    return render_template('errors/500.html'), 500

