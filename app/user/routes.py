import csv
import datetime
from io import StringIO

from app.config import API_BASIC_URL
from app.extinsions import cryptor, db
from app.helper import mail
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


@user.route("/list/export", methods=["GET", "POST"])
def user_export():
    @stream_with_context
    def generate():
        users = User.query.all()
        data = StringIO()
        data.seek(0)
        data.write(u'\uFEFF')
        w = csv.writer(data)
        w.writerow(("user_uuid", "user_realname", "user_nickname",
                    "phone_number", "user_addr", "user_email",
                    "country_code", "country_code", "user_register_confirmed",
                    "user_register_time", "user_level"))
        for u in users:
            w.writerow((
                u.id, u.user_realname, u.user_nickname,
                u.phone_number, u.user_addr, u.user_email,
                u.country_code, u.user_register_confirmed,
                u.user_register_time, u.user_level
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    export_time = datetime.datetime.now().isoformat(timespec='seconds')
    response = Response(generate(), mimetype='text/csv')
    response.headers.set("Content-Disposition",
                         "attachment",
                         charset='utf-8-sig',
                         filename=f'UserListExport_{export_time}.csv')
    return response, 200


@user.route("/register", methods=['POST'])
def register():
    request_body = request.get_json()
    sechmas = {
        "user_realname": "",
        "user_nickname": "",
        "phone_number": "",
        "user_addr": "",
        "user_email": "",
        "user_password": "",
        "country_code": "",
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
        message =\
            "您已經註冊會員，請點此連結進行會員認證: {basic_url}/user/confirm/{token}".format(
                basic_url=API_BASIC_URL, token=token)
        send_status = mail.send_email(mail_message=message,
                                      subject="信箱認證",
                                      to=request_body['user_email'],
                                      sync=False)
        return jsonify(status="already exist"), 200
    for key in sechmas:
        if request_body.get(key) is None:
            log["data"] = f"register sechmas not find {key}"
            current_app.logger.error(log)
            return jsonify(status=log['data']), 400
        sechmas[key] = request_body.get(key)

    if len(sechmas["user_realname"]) > 50:
        return jsonify(status="user_realname format error"), 400
    if len(sechmas["user_nickname"]) > 50:
        return jsonify(status="user_nickname format error"), 400
    if not isinstance(sechmas["phone_number"], int) and \
            len(sechmas["phone_number"]) > 20:
        return jsonify(status="phone_number format error"), 400
    if len(sechmas["user_addr"]) > 100:
        return jsonify(status="user_addr format error"), 400

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


@ user.route('/confirm/<token>', methods=['GET'])
def confirmation(token):
    user = User()
    data = user.validate_confirm_token(token)
    log = {"api": request.path, "data": data}
    if data:
        print(data)
        try:
            user = User.query.filter_by(
                user_email=data.get('user_email')).update({
                    "user_register_confirmed": True})
            db.session.commit()
            db.session.close()
            current_app.logger.warning(log)
            return jsonify(status="validate success"), 200
        except exc.SQLAlchemyError as e:
            log['sql'] = e
            current_app.logger.warning(log)
            return jsonify(status="validate fail"), 400
    else:
        current_app.logger.warning(log)
        return jsonify(status="validate fail"), 400


@ user.route('/forget/password', methods=["POST"])
def forget_password():
    user_email = request.json.get("user_email")
    phone_number = request.json.get("phone_number")
    user = User.query.filter_by(user_email=user_email).first()
    if user is None:
        return jsonify(status="Not found user"), 404
    if user.user_password == "":
        return jsonify(status="Already apply reset password"), 200
    log = {
        "user_email": user_email,
        "api": request.path
    }
    if phone_number == user.phone_number:
        # reset password
        try:
            User.query.filter_by(user_email=user_email).update(
                {"user_password": "", "user_register_confirmed": False})
            db.session.commit()
            db.session.close()
            jwt_token = create_access_token(identity=user_email)
            change_msg = "{basic_url}/password/change?jwt={token}".format(
                basic_url=API_BASIC_URL, token=jwt_token)
            mail.send_email(mail_message=change_msg,
                            subject="重製密碼", to=User.user_email)
            log['change_msg'] = change_msg
            current_app.logger.info(log)
            return jsonify(status=change_msg), 200
        except exc.SQLAlchemyError as e:
            log['sql'] = e
            current_app.logger.warning(log)
            return jsonify(status="Reset error"), 400


@ user.route('/password/change', methods=["POST"])
@ jwt_required()
def change_password():
    identity = get_jwt_identity()  # identity is email
    user = User()
    user = user.query.filter_by(user_email=identity).first()
    new_password = cryptor.generate_password_hash(
        password=request.json.get('user_password'),
        rounds=10).decode('utf-8')
    log = {"user": user.user_email, "api": request.path}
    if len(request.json.get('user_password')) < 64:
        return jsonify(status="password format error"), 403
    if user is None:
        return jsonify(status="user not found"), 404
    if user.user_password != "":
        return jsonify(status="please apply forget password"), 400

    try:
        User.query.filter_by(user_email=identity).update(
            {"user_password": new_password, "user_register_confirmed": True})
        db.session.commit()
        db.session.close()
        current_app.logger.info(log)
        return jsonify(status="change success"), 200
    except exc.SQLAlchemyError as e:
        log['sql'] = e
        current_app.logger.warning(log)
        return jsonify(status="Database error"), 500
