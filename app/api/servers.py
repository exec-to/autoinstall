# -*- coding: UTF-8 -*-
from flask_restx import Namespace, Resource, errors, fields, abort
from app import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy_filters import apply_filters
from flask import url_for, request, jsonify
from app import core as CoreLib
from app.core.grub import Grub

api = Namespace('servers', description='Раздел: операции с серверами')
core = CoreLib.Core()


MacAddressModel = api.model('MacAddressModel', {
    # 'id': fields.String,
    'mac_addr': fields.String
})

MacListModel = api.model('MacListModel', {
    'mac_list': fields.List(fields.Nested(MacAddressModel))
})

ServerModel = api.model('ServerModel', {
    'id': fields.String,
    'adman_id': fields.String,
    'uri': fields.Url('api.server_ep', absolute = True),
    'message': fields.String,
    'mac_list': fields.List(fields.Nested(MacAddressModel))
})

@api.route('/<int:adman_id>', endpoint='server_ep')
class Server(Resource):
    @api.doc(params={'adman_id': 'ID сервера в оборудовании adman'})
    @api.doc(security='apikey')
    @api.marshal_with(ServerModel, skip_none=True)
    def get(self, adman_id):  # Create GET endpoint
        """
        Получить информацию по указанному серверу
        """
        session = None

        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            abort(401)
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg)

        server = None
        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                raise Exception('NotFound', 'Не найден сервер c ID: {}'.format(adman_id))

            server.mac_list = session.query(CoreLib.MacTable).filter_by(server_id=server.id).all()

        except Exception as e:
            msg = 'Не удаётся получить сервер. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            abort(400, message=msg)

        return server


@api.route('/', endpoint='servers_list_ep')
class ServerList(Resource):
    @api.doc(security='apikey')
    @api.marshal_list_with(ServerModel)
    def get(self):  # Create GET endpoint
        """
        Получить список настроенных серверов
        """
        session = None

        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            api.logger.debug('Unauthorized, 401')
            abort(401)
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg)

        servers = None
        try:
            servers = session.query(CoreLib.Server).all()

            for server in servers:
                server.mac_list = session.query(CoreLib.MacTable).filter_by(server_id=server.id).all()

        except Exception as e:
            msg = 'Не удаётся получить список серверов. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            abort(400, message=msg)

        return servers


@api.route('/configure/<int:adman_id>', endpoint='server_configure_ep')
class ServerConfigure(Resource):
    @api.doc(params={'adman_id': 'ID сервера в оборудовании adman'})
    @api.doc(security='apikey')
    @api.expect([MacAddressModel])
    def put(self, adman_id):  # Create PUT endpoint
        """
        Обновить конфигурацию указанного сервера
        """
        headers = request.headers
        api.logger.debug(headers)
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            api.logger.debug('Unauthorized, 401')
            abort(401)

        # api.logger.debug(request.json)
        session = None
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg)

        server = None
        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                server = CoreLib.Server(adman_id=adman_id)
                session.add(server)
                session.commit()

            if server.maintenance:
                msg = 'Сервер находится в режиме обслуживания. Внесение настроек заблокировано.'
                abort(400, message=msg)

            Grub.create_server_dir(server.adman_id)

            # Проверяем, используются ли MAC-адреса другими серверами
            for item in request.json:
                filters = [
                    {'field': 'mac_addr', 'op': 'ilike', 'value': item['mac_addr'].lower()}
                ]
                macs = session.query(CoreLib.MacTable)
                macs = apply_filters(macs, filters).all()

                # Проверяем, используются ли MAC-адреса другими серверами
                for mac in macs:
                    if mac.server_id != server.id:
                        msg = 'MAC-адрес {} уже используется сервером с ID: {}'.format(mac.mac_addr, mac.server_id)
                        api.logger.error(msg)
                        raise Exception('MacIsInUse', msg)
                        # abort(400, message=msg)

            # Удаляем MAC-адреса из БД и символьные ссылки из файловой системы
            filters = [
                {'field': 'server_id', 'op': '==', 'value': server.id}
            ]
            macs = session.query(CoreLib.MacTable)
            macs = apply_filters(macs, filters).all()

            for mac in macs:
                api.logger.debug("mac: {}".format(mac.mac_addr))
                Grub.remove_symbol_link(mac.mac_addr)
                session.delete(mac)

            session.commit()

            # Добавляем MAC-адреса в БД и создаём символьные ссылки.
            for item in request.json:
                macaddr = CoreLib.MacTable(server_id=server.id, mac_addr=item['mac_addr'].lower())
                session.add(macaddr)
                Grub.create_symbol_link(server.adman_id, item['mac_addr'].lower())

            session.commit()

        except Exception as e:
            msg = 'Не удаётся настроить сервер. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            abort(400, message=msg)

        return {"success": True}
