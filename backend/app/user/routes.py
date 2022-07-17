
import secrets
from datetime import datetime, timedelta, timezone

from app import config
from app.extinsions import cryptor, db
from app.token.models import Token
from app.user import user
from app.user.models import User
from flask import current_app, request
from flask.json import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from sqlalchemy import exc


@user.route("/login", methods=["POST"])
def login():
    account = request.json.get("account")
    user = User.query.filter_by(account=account).first()
    if user is None:
        return jsonify(status="user not found"), 404
    if len(request.json.get('password')) != 64:
        return jsonify(status="password not hash"), 403
    if user.password == "":
        return jsonify(status="please reset your password"), 403

    validate = cryptor.check_password_hash(
        user.password, request.json.get('password'))
    token = secrets.token_urlsafe(32)
    log = {
        "api": request.path,
        "validate": validate,
        "token": token
    }
    current_app.logger.info(log)
    if validate:
        sechmas = {
            "account_id": user.id,
            "token": token,
            "phase": 1
        }
        db_token = Token(**sechmas)
        db.session.add(db_token)
        db.session.commit()
        db.session.close()
        return jsonify(token=token), 200
    else:
        current_app.logger.info(log)
        return jsonify(status="password error"), 403


@user.route('/status', methods=["GET", "POST"])
def status():
    request_body = request.get_json()
    print(request_body)
    return jsonify(request_body), 200


@user.route("/info", methods=["GET", "POST"])
def user_info():
    request_body = request.get_json()
    db_token = Token.query.filter_by(
        token=request_body['token'], phase=2).first()
    if db_token is None:
        return jsonify(status="Token not found"), 404
    user = User.query.filter_by(id=db_token.account_id).first()
    current_app.logger.info(
        {"account": user.account, "api": request.path})
    if db_token.account_id == user.id:
        sechmas = {
            "account": user.account,
            "email": user.email,
            "nickname": user.nickname,
            "last_login": user.last_login,
            "register_time": user.register_time,
        }

        return jsonify(sechmas), 200
    return jsonify(status="something error"), 500


@user.route("/register", methods=['POST'])
def register():
    request_body = request.get_json()
    sechmas = {
        "account": "",
        "nickname": "",
        "password": "",
        "email": "",
    }
    log = {
        "api": request.path,
        "email": request_body['email']
    }
    user = User.query.filter_by(
        email=request_body.get('email')).first()
    if user is not None:
        log['error'] = "already exist"
        current_app.logger.info(log)
        return jsonify(status="already exist"), 200
    for key in sechmas:
        if request_body.get(key) is None:
            log["data"] = f"register sechmas not find {key}"
            current_app.logger.error(log)
            return jsonify(status=log['data']), 400
        sechmas[key] = request_body.get(key)

    if len(sechmas["nickname"]) > 50:
        return jsonify(status="user_nickname format error"), 400

    password = cryptor.generate_password_hash(
        password=request_body['password'], rounds=config.BCRYPT_LOG_ROUNDS)
    sechmas['password'] = password.decode("utf-8", "ignore")
    sechmas['last_login'] = datetime.now(timezone(timedelta(hours=+8)))
    sechmas['register_time'] = datetime.now(timezone(timedelta(hours=+8)))
    print(sechmas)
    user = User(**sechmas)
    current_app.logger.warning(log)
    try:
        db.session.add(user)
        db.session.commit()
        db.session.close()
        current_app.logger.info(log)
        return jsonify(status=True), 200
    except exc.SQLAlchemyError as e:
        log['sql'] = e
        current_app.logger.warning(log)
        return jsonify(status=f"register fail {log}"), 400
