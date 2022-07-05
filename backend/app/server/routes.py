from app.server import server
from flask import jsonify
from app.server.check_service import check_database
from datetime import datetime, timedelta, timezone
from flask import current_app, request


@server.route('/info')
def server_status():
    """Get DB and email status

    Returns:
        json: {
            update_time:UTC+8 ISO 8601
            data:service,isAlive,description
        }
    """

    database = check_database()
    update_time = datetime.utcnow().astimezone(
        timezone(offset=timedelta(hours=8))).isoformat()
    info = {"update_time": update_time,
            "data": [database]
            }
    log = {"ip": request.remote_addr, "data": info,  "api": request.path}
    current_app.logger.info(log)
    return jsonify(info), 200
