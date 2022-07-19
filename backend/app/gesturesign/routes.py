import email
import secrets
from datetime import datetime, timedelta, timezone
import json
from app.gesturesign import gsign
from app.gesturesign.models import Gsign
from app.extinsions import cryptor, db
from app.token.models import Token
from app.user.models import User
from flask import current_app, jsonify, request
from app.gesturesign import signProcess
from app.gesturesign import sign_validate
@gsign.route('/2fa', methods=['POST'])
def mfa():
    request_body = request.get_json()
    # print(request_body['token'], request_body['landmark'])
    db_token = Token.query.filter_by(
        token=request_body['token'], phase=1).first()
    if db_token is None:
        return jsonify(status="token not found"), 404
    target_id = -1
    
    token = secrets.token_urlsafe(32)
    email = User.query.filter(User.id == db_token.account_id).first().email
    with open('./app/gesturesign/info.json') as dist_file:
        user_list = json.load(dist_file)
    for index,key in enumerate(user_list.values()):
        if(key['email'] == email):
            target_id = index
    login_sign = signProcess.convert(request_body['landmark'],target_id)
    validate = sign_validate.sign_validate(login_sign, target_id)
    print(validate)

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
    return jsonify({"status": "sign rejected."}), 403
