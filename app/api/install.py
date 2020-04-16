# -*- coding: UTF-8 -*-
from flask_restx import Namespace, Resource, errors, fields, abort
from app import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy_filters import apply_filters
from flask import url_for, request, jsonify
from app import core as CoreLib
from app.core.grub import Grub
from app.core.utils import Utils

api = Namespace('install', description='Раздел: операции установки ОС')
core = CoreLib.Core()

InstallModel = api.model('InstallModel', {
    'os': fields.String,
    'osver': fields.String,
    'ipaddr': fields.String,
    'passwdhash': fields.String,
    'diskpart': fields.String
})


@api.route('/run/<int:adman_id>', endpoint='server_install_ep')
class InstallRun(Resource):
    @api.doc(security='apikey')
    @api.doc(params={'adman_id': 'ID сервера в оборудовании adman'})
    @api.expect(InstallModel)
    def put(self, adman_id):  # Create PUT endpoint
        """
        Создать конфигурацию для запуска установки ОС
        """
        headers = request.headers
        api.logger.debug(headers)
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            api.logger.debug('Unauthorized, 401')
            return {"message": "Error: Unauthorized"}, 401

        session = None
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg)

        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                raise Exception('NotFound', 'Не найден сервер c ID: {}. Обновите сначала его конфигурацию.'.format(adman_id))

            if server.maintenance:
                msg = 'Сервер уже находится в режиме обслуживания. Дождитесь завершения операций.'
                raise Exception('MaitenanceMode', msg)

            api.logger.debug(request.json)
            Grub.update_template(request.json)
            Grub.mkconfig(adman_id)

            # + TODO: Создать токен установки, сохранить в БД.
            # + TODO: Получить параметры из заказа: IP-адрес/маску/шлюз/DNS, ОС, пароль, разметка диска
            # TODO: Сгенерировать шаблон и сохранить
            # TODO: Реализовать проверку токена
            # TODO: Создать каталог и шаблоны файлов preseed

            token = Utils.get_token()
            ipaddr = request.json['ipaddr']
            passwdhash = request.json['passwdhash']
            diskpart = request.json['diskpart']
            os = request.json['os']
            osver = request.json['osver']

            install = CoreLib.Install(adman_id, os, osver, token, ipaddr, passwdhash, diskpart)
            session.add(install)
            session.commit()

            Utils.create_preseed_conf(adman_id, request.json, token)

            server.maintenance = True
            session.commit()

        except Exception as e:
            msg = 'Не удаётся завершить инициализацию процесса установки: {}'.format(str(e))
            api.logger.error(msg)
            return {"message": msg}, 500

        return {"success": True}


@api.route('/complete/<int:adman_id>/<string:token>', endpoint='server_install_complete_ep')
class InstallComplete(Resource):
    @api.doc(params={
        'adman_id': 'ID сервера в оборудовании adman',
        'token': 'Токен установки, генерируется при инициализации установки'
    })
    def get(self, adman_id, token):
        """
        Сообщить о завершении установки ОС
        """
        args = {'os': 'local', 'osver': '0'}

        session = None

        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg)

        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                raise Exception('NotFound', 'Не найден сервер c ID: {}. Обновите сначала его конфигурацию.'.format(adman_id))

            # Проверить токен
            filters = [
                {'field': 'adman_id', 'op': '==', 'value': adman_id},
                {'field': 'status', 'op': '==', 'value': 0},
                {'field': 'token', 'op': '==', 'value': token}
            ]
            install = session.query(CoreLib.Install)
            install = apply_filters(install, filters).first()

            if install is None:
                raise Exception('Unauthorized',
                                'Для выполнения операции требуется авторизация по токену.')

            Grub.update_template(args)
            Grub.mkconfig(adman_id)

            install.status = True
            server.maintenance = False
            session.commit()

        except Exception as e:
            msg = 'Не удалось выполнить запрос на завершение установки ОС. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            return {"message": msg}, 500

        return {"success": True}