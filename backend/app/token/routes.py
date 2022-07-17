from datetime import datetime, timedelta, timezone
from app.extinsions import cryptor, db

from app.token import token
from flask import current_app, jsonify, request
from sqlalchemy import exc


@token.route('/status')
def sign_status():
    update_time = datetime.utcnow().astimezone(
        timezone(offset=timedelta(hours=8))).isoformat()
    info = {"update_time": update_time,
            }
    log = {"ip": request.remote_addr, "data": info,  "api": request.path}
    current_app.logger.info(log)
    return jsonify(info), 200


@token.route('/validate', methods=['POST'])
def validate():
    request_body = request.get_json()
    sechmas = {
        "uid": request_body['account'],
        "hash_0": request_body['token'],
    }
    return jsonify(sechmas), 200
