import csv
import datetime
from io import StringIO

from app.config import API_BASIC_URL
from app.extinsions import cryptor, db
from app.user import user
from app.user.models import User
from flask import Response, current_app, request, stream_with_context
from flask.json import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from sqlalchemy import exc


@user.route("/login", methods=["POST"])
def login():
    user_email = request.json.get("user_email")
    user = User.query.filter_by(user_email=user_email).first()
    if user is None:
        return jsonify(status="user not found"), 404
    if len(request.json.get('user_password')) != 64:
        return jsonify(status="password not hash"), 403
    if user.user_password == "":
        return jsonify(status="please reset your password"), 403

    validate = cryptor.check_password_hash(
        user.user_password, request.json.get('user_password'))
    log = {
        "api": request.path,
        "user_email": user_email,
        "validate": validate
    }
    if validate:
        jwt_token = create_access_token(identity=user_email)
        log["jwt_token"] = jwt_token
        current_app.logger.info(log)
        return jsonify(token=jwt_token), 200
    else:
        current_app.logger.info(log)
        return jsonify(status="password error"), 403


@user.route("/info", methods=["GET", "POST"])
@jwt_required()
def user_info():
    identity = get_jwt_identity()  # identity is email
    user = User.query.filter_by(user_email=identity).first()
    sechmas = {
        "user_realname": user.user_realname,
        "user_nickname": user.user_nickname,
        "phone_number": user.phone_number,
        "user_addr": user.user_addr,
        "user_email": user.user_email,
        "country_code": user.country_code,
        "user_register_confirmed": user.user_register_confirmed,
        "user_register_time": user.user_register_time,
        "user_level": user.user_level
    }
    current_app.logger.info(
        {"user_email": identity, "api": request.path})
    return jsonify(sechmas), 200



@user.route("/register", methods=['POST'])
def register():
    request_body = request.get_json()
    sechmas = {
        "user_nickname": "",
        "user_password": "",
    }
    log = {
        "api": request.path,
        "user_email": request_body['user_email']
    }
    user = User.query.filter_by(
        user_email=request_body.get('user_email')).first()
    if user is not None:
        log['error'] = "already exist"
        current_app.logger.info(log)
        token = user.create_confirm_token()
        return jsonify(status="already exist"), 200
    for key in sechmas:
        if request_body.get(key) is None:
            log["data"] = f"register sechmas not find {key}"
            current_app.logger.error(log)
            return jsonify(status=log['data']), 400
        sechmas[key] = request_body.get(key)

    if len(sechmas["user_nickname"]) > 50:
        return jsonify(status="user_nickname format error"), 400

    password = cryptor.generate_password_hash(
        password=request_body['user_password'], rounds=10)
    sechmas['user_password'] = password.decode("utf-8", "ignore")
    user = User(**sechmas)

    token = user.create_confirm_token()
    message = "點此連結進行會員認證: {basic_url}/user/confirm/{token}".format(
        basic_url=API_BASIC_URL, token=token)
    send_status = mail.send_email(mail_message=message,
                                  subject="信箱認證",
                                  to=request_body['user_email'], sync=False)
    if send_status is False:
        log["send_status"] is False
        current_app.logger.warning(log)
        return jsonify(status="Validation email send error"), 400

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
