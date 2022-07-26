import secrets
from datetime import datetime, timedelta, timezone

from app.cr import cr
from app.cr.models import CR
from app.extinsions import cryptor, db
from app.token.models import Token
from app.user.models import User
from flask import current_app, jsonify, request
from sqlalchemy import exc
import random


@cr.route('/symbol', methods=['POST'])
def cr():
    symbol = ["ant", "ham", "$"]
    request_body = request.get_json()

    db_token = Token.query.filter_by(
        token=request_body['token'], phase=1).first()
    if db_token is None:
        return jsonify(status="token not found"), 404

    choice_symbol = random.randint(0, int(len(symbol)))
    cr_token = secrets.token_urlsafe(32)
    sechmas = {
        "account_id": db_token.account_id,
        "cr_token": cr_token,
        "symbol": symbol[choice_symbol],
        "symbol_code": choice_symbol,
        "create_time": datetime.now(timezone(timedelta(hours=+8))),
        "status": 0
    }
    log = {
        "api": request.path
    }
    cr = CR(**sechmas)
    try:
        db.session.add(cr)
        db.session.commit()
        db.session.close()
        current_app.logger.info(sechmas)
        res = {"symbol": symbol[choice_symbol],
               "cr_token": cr_token}
        return jsonify(res), 200
    except exc.SQLAlchemyError as e:
        log['sql'] = e
        current_app.logger.warning(log)
        return jsonify(status=f"register fail {log}"), 400
