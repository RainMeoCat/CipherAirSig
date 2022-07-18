import secrets
from datetime import datetime, timedelta, timezone

from app.gesturesign import gsign
from app.gesturesign.models import Gsign
from app.extinsions import cryptor, db
from app.token.models import Token
from app.user.models import User
from flask import current_app, jsonify, request


@gsign.route('/2fa', methods=['POST'])
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
