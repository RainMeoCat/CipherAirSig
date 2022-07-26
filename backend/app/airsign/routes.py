import imp
import json
import secrets
from datetime import datetime, timedelta, timezone

from app.airsign import airsign
from app.airsign.models import Airsign
from app.airsign.predict import airsign_predict
from app.cr.models import CR
from app.extinsions import cryptor, db
from app.token.models import Token
from app.user.models import User
from flask import current_app, jsonify, request
from sqlalchemy import exc, text
from collections import Counter


@airsign.route('/2fa', methods=['POST'])
def mfa():
    validate = False
    request_body = request.get_json()
    landmark = request_body["landmark"]
    cr_token = CR.query.filter_by(
        cr_token=request_body['cr_token']).first()
    if cr_token is None:
        return jsonify(status="CR token not found"), 404
    lepton_raw_sql = '''
    SELECT predict_class
    FROM lepton
    ORDER BY create_time DESC
    LIMIT 10
    '''
    lepton_res = db.engine.execute(lepton_raw_sql)
    predict_class = [row[0] for row in lepton_res]
    predict = Counter(predict_class)
    print("predict_class", predict)

    hash_0 = airsign_predict(landmark)
    print(hash_0)
    tolerance = 4
    account_id = cr_token.account_id
    symbol_code = cr_token.symbol_code
    raw_sql = text(f'''
    SELECT account_id,xor_hash_0,symbol_code
    FROM(
    SELECT id,account_id, BIT_COUNT(hash_0^{hash_0}) AS 'xor_hash_0',symbol_code
    FROM airsign
    ) AS R1
    WHERE xor_hash_0<{tolerance} AND account_id={account_id} AND symbol_code={symbol_code}
    ORDER BY xor_hash_0
    limit 1
    ''')
    res = db.engine.execute(raw_sql)
    sign_hash = [row[0] for row in res]
    if len(sign_hash) > 0:
        validate = True
    token = secrets.token_urlsafe(32)
    log = {
        "api": request.path,
        "validate": validate,
        "token": token,
        "symbol": cr_token.symbol,
    }
    # current_app.logger.info(log)
    if predict[1] < predict[2] and predict[0] < predict[2]:
        return jsonify(status="forbidden"), 403

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
    else:
        return jsonify(status="forbidden"), 403


@airsign.route('/search', methods=['POST'])
def serarch():
    request_body = request.get_json()
    hash_0 = request_body['hash_0']
    account_id = request_body['account_id']
    print(hash_0)
    tolerance = 2
    # with open("./app/airsign/hash_example.json", "r") as f:
    #     landmark = json.loads(f.read())
    raw_sql = text(f'''
    SELECT account_id,xor_hash_0,symbol_code
    FROM(
    SELECT id,account_id, BIT_COUNT(hash_0^{hash_0}) AS 'xor_hash_0',symbol_code
    FROM airsign
    ) AS R1
    WHERE xor_hash_0<{tolerance} AND account_id={account_id}
    ORDER BY xor_hash_0
    limit 1
    ''')
    res = db.engine.execute(raw_sql)
    sign_hash = [row[0] for row in res]
    if len(sign_hash) > 0:
        return jsonify(status="airsign_pass"), 200
    return jsonify(status="forbidden"), 403


@airsign.route('/insert', methods=['POST'])
def insert_sign():
    request_body = request.get_json()
    sechmas = {
        "account_id": request_body['account_id'],
        "hash_0": request_body['hash_0'],
        "symbol_code": request_body['symbol_code'],
        "create_time": datetime.now(timezone(timedelta(hours=+8)))
    }
    log = {
        "api": request.path,
        "symbol_code": request_body['symbol_code']
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
