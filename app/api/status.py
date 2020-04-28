# -*- coding: UTF-8 -*-
from flask_restx import Namespace, Resource, errors, fields, abort
from app import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy_filters import apply_filters
from flask import url_for, request, jsonify
from app import core as CoreLib
from app.core.grub import Grub
from app.core.utils import Utils

api = Namespace('status', description='Раздел: Статус системы')
core = CoreLib.Core()

@api.route('/', endpoint='server_status_ep')
class ServerStatus(Resource):
    @api.doc(params={
        'token': 'Токен авторизации'
    })
    @api.doc(security='querykey')
    def get(self):
        """
        Проверка работы системы
        """
        if request.args.get('token') != 'zabbix-status':
            msg = 'Для выполнения операции требуется авторизация по токену.'
            return {"message": msg, "success": False}, 401

        session = None

        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg, success=False)

        try:
            session.query(CoreLib.Server).all()

        except Exception as e:
            msg = 'Не удалось выполнить запрос к базе данных. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            return {"message": msg, "success": False}, 400

        return 1
