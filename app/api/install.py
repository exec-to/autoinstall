# -*- coding: UTF-8 -*-
from flask_restx import Namespace, Resource, errors, fields, abort
from app import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy_filters import apply_filters
from flask import url_for, request, jsonify
from app import core as CoreLib
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

InstallGetModel = api.model('InstallGetModel', {
    'adman_id': fields.String,
    'os': fields.String,
    'osver': fields.String,
    'ipaddr': fields.String,
    'token': fields.String,
    'diskpart': fields.String,
    'status': fields.String
})


@api.route('/run/<int:adman_id>', endpoint='server_install_run_ep')
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
            return {"message": "Error: Unauthorized", "success": False}, 401

        session = None
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg, success=False)

        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                raise Exception('NotFound', 'Не найден сервер c ID: {}. Обновите сначала его конфигурацию.'.format(adman_id))

            if server.maintenance:
                msg = 'Сервер уже находится в режиме обслуживания. Дождитесь завершения операций.'
                raise Exception('MaitenanceMode', msg)

            token = Utils.get_token()
            ipaddr = request.json['ipaddr']
            diskpart = request.json['diskpart']
            os = request.json['os'].lower()
            osver = request.json['osver'].lower()

            # api.logger.debug('req: {}'.format(request.json))
            # api.logger.debug('args: {}'.format(args))

            Utils.create_config(request.json, adman_id, token)
            if 'windows' in os:
                Utils.create_install_bat(request.json, adman_id)

            # api.logger.debug('req: {}'.format(request.json))

            install = CoreLib.Install(adman_id, os, osver, token, ipaddr, diskpart)
            session.add(install)
            session.commit()

            Utils.create_preseed_conf(adman_id, request.json, token)

            server.maintenance = True
            session.commit()

        except Exception as e:
            msg = 'Не удаётся завершить инициализацию процесса установки: {}'.format(str(e))
            api.logger.error(msg)
            return {"success": False, "message": msg}, 500

        return {"success": True, "token": token}


@api.route('/complete/<int:adman_id>', endpoint='server_install_complete_ep')
class InstallComplete(Resource):
    @api.doc(params={
        'adman_id': 'ID сервера в оборудовании adman',
        'token': 'Токен установки, генерируется при инициализации установки'
    })
    @api.doc(security='querykey')
    def get(self, adman_id):
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
            abort(500, message=msg, success=False)

        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                raise Exception('NotFound', 'Не найден сервер c ID: {}. Обновите сначала его конфигурацию.'.format(adman_id))

            # Проверить токен
            filters = [
                {'field': 'adman_id', 'op': '==', 'value': adman_id},
                {'field': 'token', 'op': '==', 'value': request.args.get('token')}
            ]
            install = session.query(CoreLib.Install)
            install = apply_filters(install, filters).first()

            if install is None:
                raise Exception('Unauthorized',
                                'Для выполнения операции требуется авторизация по токену.')

            if install.status == 1:
                raise Exception('AlreadyComplete',
                                'Операция уже была завершена ранее.')

            if install.status == 2:
                raise Exception('AlreadyBreak',
                                'Операция уже была отменена ранее.')

            Utils.create_config(args, adman_id)

            install.status = 1
            server.maintenance = False
            session.commit()

        except Exception as e:
            msg = 'Не удалось выполнить запрос на завершение установки ОС. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            return {"message": msg, "success": False}, 400

        return {"success": True}


@api.route('/break/<int:adman_id>', endpoint='server_install_break_ep')
class InstallBreak(Resource):
    @api.doc(params={
        'adman_id': 'ID сервера в оборудовании adman',
        'token': 'Токен установки, генерируется при инициализации установки'
    })
    @api.doc(security='querykey')
    def get(self, adman_id):
        """
        Сообщить об отмене установки ОС
        """
        args = {'os': 'local', 'osver': '0'}

        session = None

        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg, success=False)

        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                raise Exception('NotFound', 'Не найден сервер c ID: {}. Обновите сначала его конфигурацию.'.format(adman_id))

            # Проверить токен
            filters = [
                {'field': 'adman_id', 'op': '==', 'value': adman_id},
                {'field': 'token', 'op': '==', 'value': request.args.get('token')}
            ]
            install = session.query(CoreLib.Install)
            install = apply_filters(install, filters).first()

            if install is None:
                raise Exception('Unauthorized',
                                'Для выполнения операции требуется авторизация по токену.')

            if install.status == 1:
                raise Exception('AlreadyComplete',
                                'Операция уже была успешно завершена ранее.')

            if install.status == 2:
                raise Exception('AlreadyBreak',
                                'Операция отмены уже была завершена ранее.')

            Utils.create_config(args, adman_id)

            install.status = 2
            server.maintenance = False
            session.commit()

        except Exception as e:
            msg = 'Не удалось выполнить запрос на отмену установки ОС. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            return {"message": msg, "success": False}, 400

        return {"success": True}


@api.route('/prestart/<int:adman_id>', endpoint='server_install_prestart_ep')
class InstallPrestart(Resource):
    @api.doc(params={
        'adman_id': 'ID сервера в оборудовании adman',
        'token': 'Токен установки, генерируется при инициализации установки'
    })
    @api.doc(security='querykey')
    def get(self, adman_id):
        """
        Сообщить о запуске установки ОС
        """
        args = {'os': 'local', 'osver': '0'}

        session = None

        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg, success=False)

        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                raise Exception('NotFound', 'Не найден сервер c ID: {}. Обновите сначала его конфигурацию.'.format(adman_id))

            # Проверить токен
            filters = [
                {'field': 'adman_id', 'op': '==', 'value': adman_id},
                {'field': 'token', 'op': '==', 'value': request.args.get('token')}
            ]
            install = session.query(CoreLib.Install)
            install = apply_filters(install, filters).first()

            if install is None:
                raise Exception('Unauthorized',
                                'Для выполнения операции требуется авторизация по токену.')

            if install.status == 1:
                raise Exception('AlreadyComplete',
                                'Установка уже была успешно завершена ранее.')

            if install.status == 2:
                raise Exception('AlreadyBreak',
                                'Установка уже была отменена ранее.')

            Utils.create_config(args, adman_id)

            install.status = 3
            session.commit()

        except Exception as e:
            msg = 'Не удалось выполнить запрос на изменение конфигурации установки ОС (Pre start). Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            return {"message": msg, "success": False}, 400

        return {"success": True}


@api.route('/', endpoint='install_list_ep')
class InstallList(Resource):
    @api.doc(security='apikey')
    @api.marshal_list_with(InstallGetModel)
    def get(self):  # Create GET endpoint
        """
        Получить список операций установки ОС
        """
        session = None

        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            api.logger.debug('Unauthorized, 401')
            abort(401, success=False)
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg, success=False)

        installs = None
        try:
            installs = session.query(CoreLib.Install).all()

        except Exception as e:
            msg = 'Не удаётся получить список установок. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            abort(400, message=msg, success=False)

        return installs


@api.route('/<int:adman_id>', endpoint='server_install_ep')
class Install(Resource):
    @api.doc(params={
        'adman_id': 'ID сервера в оборудовании adman',
        'token': 'Токен установки, генерируется при инициализации установки'
    })
    @api.doc(security='querykey')
    @api.marshal_with(InstallGetModel)
    def get(self, adman_id):
        """
        Получить информацию по операции установки ОС
        """

        session = None

        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg, success=False)

        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                raise Exception('NotFound', 'Не найден сервер c ID: {}. Обновите сначала его конфигурацию.'.format(adman_id))

            # Проверить токен
            filters = [
                {'field': 'adman_id', 'op': '==', 'value': adman_id},
                {'field': 'token', 'op': '==', 'value': request.args.get('token')}
            ]
            install = session.query(CoreLib.Install)
            install = apply_filters(install, filters).first()

            if install is None:
                raise Exception('Unauthorized',
                                'Для выполнения операции требуется авторизация по токену.')

        except Exception as e:
            msg = 'Не удалось получить данные по операции установки ОС. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            return {"message": msg, "success": False}, 400

        return install

# TODO: GET OS List
