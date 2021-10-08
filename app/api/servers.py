# -*- coding: UTF-8 -*-
from flask_restx import Namespace, Resource, errors, fields, abort
from app import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy_filters import apply_filters
from flask import url_for, request, jsonify
from app import core as CoreLib
from app.core.utils import Utils

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
    'maintenance': fields.String,
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
            abort(401, success=False)
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg, success=False)

        server = None
        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                raise Exception('NotFound', 'Не найден сервер c ID: {}'.format(adman_id))

            server.mac_list = session.query(CoreLib.MacTable).filter_by(server_id=server.id).all()

        except Exception as e:
            msg = 'Не удаётся получить сервер. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            abort(400, message=msg, success=False)

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
            abort(401, success=False)
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg, success=False)

        servers = None
        try:
            servers = session.query(CoreLib.Server).all()

            for server in servers:
                server.mac_list = session.query(CoreLib.MacTable).filter_by(server_id=server.id).all()

        except Exception as e:
            msg = 'Не удаётся получить список серверов. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            abort(400, message=msg, success=False)

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
#        api.logger.debug(headers)
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            api.logger.debug('Unauthorized, 401')
            abort(401, success=False)

#        api.logger.debug(request.json)
#        api.logger.debug("--- 0 ---")
        session = None
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg, success=False)

#        api.logger.debug("--- 1 ---")

        server = None
        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
#            api.logger.debug("--- 2 ---")
            if server is None:
                server = CoreLib.Server(adman_id=adman_id)
                session.add(server)
                session.commit()
	
#            api.logger.debug("--- 3 ---")
            if server.maintenance:
                msg = 'Сервер находится в режиме обслуживания. Внесение настроек заблокировано.'
                abort(400, message=msg, success=False)

            Utils.create_server_dir(server.adman_id)

#            api.logger.debug("--- 4 ---")
            # Проверяем, используются ли MAC-адреса другими серверами
            for item in request.json:
                filters = [
                    {'field': 'mac_addr', 'op': 'ilike', 'value': item['mac_addr'].lower()}
                ]
                macs = session.query(CoreLib.MacTable)
                macs = apply_filters(macs, filters).all()
                
#                api.logger.debug("--- 5 ---")
                # Проверяем, используются ли MAC-адреса другими серверами
                for mac in macs:
                    if not mac.mac_addr:
                        continue

                    api.logger.debug(mac.mac_addr)
                    if mac.server_id != server.id:
                        msg = 'MAC-адрес {} уже используется сервером с ID: {}'.format(mac.mac_addr, mac.server_id)
                        api.logger.error(msg)
                        raise Exception('MacIsInUse', msg)
                        # abort(400, message=msg)

            # Удаляем MAC-адреса из БД и символьные ссылки из файловой системы
            filters = [
                {'field': 'server_id', 'op': '==', 'value': server.id}
            ]
#            api.logger.debug("--- 6 ---")
            macs = session.query(CoreLib.MacTable)
            macs = apply_filters(macs, filters).all()
#            api.logger.debug("--- 7 ---")
            for mac in macs:
#                api.logger.debug("XXXAS_mac: {}".format(mac.mac_addr))
                Utils.remove_symbol_link(mac.mac_addr)
                session.delete(mac)

            session.commit()
#            api.logger.debug("--- 8 ---")
            # Добавляем MAC-адреса в БД и создаём символьные ссылки.
            for item in request.json:
                macaddr = CoreLib.MacTable(server_id=server.id, mac_addr=item['mac_addr'].lower())
#                api.logger.debug("0XFFF__mac: {}".format(macaddr))
                session.add(macaddr)
                Utils.create_symbol_link(server.adman_id, item['mac_addr'].lower())
#            api.logger.debug("--- 9 ---")
            session.commit()
	    #api.logger.debug("REQ_COMMIT")
            #Создаём начальный конфиг
            args = {'os': 'local', 'osver': '0', 'diskpart': '0'}
            Utils.create_config(args, server.adman_id)

        except Exception as e:
            msg = 'Не удаётся настроить сервер. Ошибка: {}'.format(str(e))
            api.logger.error(msg)
            abort(400, message=msg, success=False)

        return {"success": True} 


@api.route('/purge/<int:adman_id>', endpoint='server_purge_ep')
class Server(Resource):
    @api.doc(params={'adman_id': 'ID сервера в оборудовании adman'})
    @api.doc(security='apikey')
    @api.marshal_with(ServerModel, skip_none=True)
    def put(self, adman_id):  # Create GET endpoint
        """
        Очисть конфигурацию сервера и установок
        """
        session = None

        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            abort(401, success=False)
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Не удаётся инициализировать соединение с БД: {}'.format(str(e))
            api.logger.error(msg)
            abort(500, message=msg, success=False)

        server = None
        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                raise Exception('NotFound', 'Не найден сервер c ID: {}'.format(adman_id))

            # remove server mac address
            macs = session.query(CoreLib.MacTable).filter_by(server_id=server.id).all()
            for mac in macs:
                Utils.remove_symbol_link(mac.mac_addr)
                session.delete(mac)
            
            # remove installs 
            installs = session.query(CoreLib.Install).filter_by(adman_id=adman_id).all()
            for install in installs:        
                session.delete(install)
            
            # remove server
            Utils.remove_symbol_link("s{adman_id}".format(adman_id=adman_id))
            session.delete(server)

            session.commit()

        except Exception as e:
            msg = 'Не удаётся выполнить операцию. Error: {}'.format(str(e))
            api.logger.error(msg)
            abort(400, message=msg, success=False)

        return server