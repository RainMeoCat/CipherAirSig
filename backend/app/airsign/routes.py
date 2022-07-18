import secrets
from datetime import datetime, timedelta, timezone

from app.airsign import airsign
from app.airsign.models import Airsign
from app.extinsions import cryptor, db
from app.token.models import Token
from app.user.models import User
from flask import current_app, jsonify, request
from sqlalchemy import exc
from app.cr.models import CR


@airsign.route('/2fa', methods=['POST'])
def mfa():
    request_body = request.get_json()
    cr_token = CR.query.filter_by(
        cr_token=request_body['cr_token']).first()
    if cr_token is None:
        return jsonify(status="CR token not found"), 404
    validate = True
    token = secrets.token_urlsafe(32)

    log = {
        "api": request.path,
        "validate": validate,
        "token": token,
        "symbol": cr_token.symbol
    }
    current_app.logger.info(log)
    if validate:
        user = User.query.filter(User.id == cr_token.account_id).first()
        sechmas = {
            "account_id": user.id,
            "token": token,
            "phase": 2
        }
        User.query.filter(User.id == cr_token.account_id).update(
            {"last_login": datetime.now(timezone(timedelta(hours=+8)))}
        )
        CR.query.filter(CR.cr_token == cr_token.cr_token).update(
            {"status": 1})
        db_token = Token(**sechmas)
        db.session.add(db_token)
        db.session.commit()
        db.session.close()
    return jsonify(sechmas), 200


@airsign.route('/serarch', methods=['POST'])
def serarch():
    pass


@airsign.route('/insert', methods=['POST'])
def insert_sign():
    request_body = request.get_json()
    sechmas = {
        "account_id": request_body['uid'],
        "hash_0": request_body['hash_0'],
        "symbol_code": request_body['symbol_code'],
        "create_time": datetime.now(timezone(timedelta(hours=+8)))
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
