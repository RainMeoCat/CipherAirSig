import secrets
from datetime import datetime, timedelta, timezone

from app.airsign import airsign
from app.airsign.models import Airsign
from app.extinsions import cryptor, db
from app.token.models import Token
from app.user.models import User
from flask import current_app, jsonify, request
from sqlalchemy import exc


@airsign.route('/status')
def sign_status():
    update_time = datetime.utcnow().astimezone(
        timezone(offset=timedelta(hours=8))).isoformat()
    info = {"update_time": update_time,
            }
    log = {"ip": request.remote_addr, "data": info,  "api": request.path}
    current_app.logger.info(log)
    return jsonify(info), 200


@airsign.route('/2fa', methods=['POST'])
def mfa():
    request_body = request.get_json()
    print(request_body['token'], request_body['landmark'])
    db_token = Token.query.filter_by(
        token=request_body['token'], phase=1).first()
    if db_token is None:
        return jsonify(status="token not found"), 404

    validate = True
    token = secrets.token_urlsafe(32)
    log = {
        "api": request.path,
        "validate": validate,
        "token": token
    }
    current_app.logger.info(log)
    if validate:
        user = User.query.filter(User.id == db_token.account_id).first()
        sechmas = {
            "account_id": user.id,
            "token": token,
            "phase": 2
        }
        User.query.filter(User.id == db_token.account_id).update(
            {"last_login": datetime.now(timezone(timedelta(hours=+8)))}
        )
        db_token = Token(**sechmas)
        db.session.add(db_token)
        db.session.commit()
        db.session.close()
    return jsonify(sechmas), 200


@airsign.route('/insert', methods=['POST'])
def insert_sign():
    request_body = request.get_json()
    sechmas = {
        "account_id": request_body['uid'],
        "hash_0": request_body['hash_0'],

    }
    log = {
        "api": request.path,
        "user_email": request_body['uid']
    }
    airsign = Airsign(**sechmas)
    current_app.logger.warning(log)
    try:
        db.session.add(airsign)
        db.session.commit()
        db.session.close()
        current_app.logger.info(log)
        return jsonify(status=True), 200
    except exc.SQLAlchemyError as e:
        log['sql'] = e
        current_app.logger.warning(log)
        return jsonify(status=f"register fail {log}"), 400
