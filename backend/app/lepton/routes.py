import base64
import json
from datetime import datetime, timedelta, timezone

import cv2
import numpy as np
from app.extinsions import cryptor, db
from app.lepton import lepton
from app.lepton.models import Lepton
from flask import current_app, jsonify, request
from sqlalchemy import exc, text


@lepton.route('/realtime', methods=['GET'])
def get_lepton():
    raw_sql = '''
    SELECT base64_temperature
    FROM lepton
    ORDER BY create_time DESC
    LIMIT 1
    '''
    log = {
        "api": request.path
    }
    current_app.logger.info(log)
    res = db.engine.execute(raw_sql)
    img = [row[0] for row in res][0]
    if len(img) > 0:
        return jsonify(image=img), 200
    return jsonify(status="DB error"), 500


@lepton.route('/raw_insert', methods=['POST'])
def insert_raw_lepton():
    request_body = request.get_json()
    raw_img = request_body['raw_data']
    raw_img = json.loads(raw_img)
    img = np.reshape(raw_img, (60, 80))*20
    img = np.uint8(img)
    heatmap = cv2.applyColorMap(img, cv2.COLORMAP_JET)
    my_base64_jpgData = base64.b64encode(
        cv2.imencode('.jpg', heatmap)[1]).decode()
    sechmas = {
        "base64_temperature": my_base64_jpgData,
        "create_time": datetime.now(timezone(timedelta(hours=+8)))
    }
    log = {
        "api": request.path
    }
    lepton = Lepton(**sechmas)
    # current_app.logger.info(log)
    try:
        db.session.add(lepton)
        db.session.commit()
        db.session.close()
        # current_app.logger.info(log)
        return jsonify(status=True), 200
    except exc.SQLAlchemyError as e:
        log['sql'] = e
        current_app.logger.warning(log)
        return jsonify(status=f"register fail {log}"), 400


@lepton.route('/insert', methods=['POST'])
def insert_lepton():
    request_body = request.get_json()
    sechmas = {
        "base64_temperature": request_body['base64_temperature'],
        "create_time": datetime.now(timezone(timedelta(hours=+8)))
    }
    log = {
        "api": request.path
    }
    lepton = Lepton(**sechmas)
    current_app.logger.info(log)
    try:
        db.session.add(lepton)
        db.session.commit()
        db.session.close()
        current_app.logger.info(log)
        return jsonify(status=True), 200
    except exc.SQLAlchemyError as e:
        log['sql'] = e
        current_app.logger.warning(log)
        return jsonify(status=f"register fail {log}"), 400
