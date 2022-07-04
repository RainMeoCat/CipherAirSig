import uuid

from app.extinsions import db
from flask import current_app
from itsdangerous import (BadSignature, SignatureExpired,
                          TimedJSONWebSignatureSerializer)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_nickname = db.Column(db.String(50),  nullable=False)
    user_realname = db.Column(db.String(50),  nullable=False)
    phone_number = db.Column(db.Unicode(20), nullable=False)
    country_code = db.Column(db.Unicode(8), nullable=False, default="TW")
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_level = db.Column(db.String(10), nullable=False, default="guest")
    user_addr = db.Column(db.String(100), nullable=False)
    user_password = db.Column(db.String(75), nullable=False)
    user_register_time = db.Column(
        db.DateTime, default=func.now(),  nullable=False)
    user_register_confirmed = db.Column(db.Boolean, default=False)

    def create_confirm_token(self, expires_in=3600):
        """
        利用itsdangerous來生成令牌，透過current_app來取得目前flask參數['SECRET_KEY']的值
        :param expiration: 有效時間，單位為秒
        :return: 回傳令牌，參數為該註冊用戶的id
        """
        s = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_email': self.user_email}).decode("utf-8")

    def validate_confirm_token(self, token):
        """
        驗證回傳令牌是否正確，若正確則回傳True
        :param token:驗證令牌
        :return:回傳驗證是否正確，正確為True
        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)  # 驗證
        except SignatureExpired:
            #  當時間超過的時候就會引發SignatureExpired錯誤
            return False
        except BadSignature:
            #  當驗證錯誤的時候就會引發BadSignature錯誤
            return False
        return data
