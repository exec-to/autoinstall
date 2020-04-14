# -*- coding: UTF-8 -*-
from flask_restx import Namespace, Resource, errors, fields
from app import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy_filters import apply_filters
from flask import url_for, request, jsonify
import os
from app import core as CoreLib
from app.core.grub import Grub

api = Namespace('servers', description='Server related operations')
core = CoreLib.Core()

# TODO: добавить MAC-адреса к выводу
ServerModel = api.model('Model', {
    'id': fields.String,
    'adman_id': fields.String,
    'uri': fields.Url('api.server_ep', absolute = True),
    'message': fields.String
})

MacAddressModel = api.model('MacAddressModel', {
    'id': fields.String,
    'mac_addr': fields.String
})

MacListModel = api.model('MacListModel', {
    'mac_list': fields.List(fields.Nested(MacAddressModel))
})


@api.route('/<int:adman_id>', endpoint='server_ep')
class Server(Resource):
    @api.doc(security='apikey')
    @api.marshal_with(ServerModel, skip_none=True)
    def get(self, adman_id):  # Create GET endpoint
        """
        Получить информацию по серверу
        """
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            api.logger.debug('Unauthorized, 401')
            return {"message": "Error: Unauthorized"}, 401
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Can\'t initialize session. Error: {}'.format(str(e))
            api.logger.error(msg)
            return {"message": msg}, 500

        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                api.logger.debug('None server with id 200:1')
                raise Exception('NotFound', 'Не найден сервер c ID: {}'.format(adman_id))

        except Exception as e:
            msg = 'Can\'t get server. Error: {}'.format(str(e))
            api.logger.error(msg)
            return {"id": None, "adman_id": adman_id, "uri": "", "message": msg}, 500

        return server


@api.route('/', endpoint='servers_list_ep')
class ServerList(Resource):
    @api.doc(security='apikey')
    @api.marshal_list_with(ServerModel)
    def get(self):  # Create GET endpoint
        """
        returns a list of servers
        """
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            api.logger.debug('Unauthorized, 401')
            return {"message": "Error: Unauthorized"}, 401
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Can\'t initialize session. Error: {}'.format(str(e))
            api.logger.error(msg)
            return {"message": msg}, 500

        try:
            servers = session.query(CoreLib.Server).all()

        except Exception as e:
            msg = 'Can\'t get servers. Error: {}'.format(str(e))
            api.logger.error(msg)
            return {"message": msg}, 500

        return servers


# @api.route('/configure/<int:adman_id>', endpoint='server_configure_ep')
# class ServerConfigure(Resource):
#     @api.doc(security='apikey')
#     @api.expect(MacListModel)
#     def put(self, adman_id, server_config):  # Create GET endpoint
#         """
#         Configure server
#         """
#         headers = request.headers
#         api.logger.debug(headers)
#         auth = headers.get("X-Api-Key")
#         if auth != config.auth['adman']:
#             api.logger.debug('Unauthorized, 401')
#             return {"message": "Error: Unauthorized"}, 401

        # parser = reqparse.RequestParser(bundle_errors=True)
        # parser.add_argument('mac_addr', action='append', help="List of server MAC-address")
        # args = parser.parse_args()

        # app.logger.debug("args: {}".format(server_config))

        # try:
        #     session = sessionmaker(bind=core.engine)()
        # except Exception as e:
        #     msg = 'Can\'t initialize session. Error: {}'.format(str(e))
        #     api.logger.error(msg)
        #     return {"message": msg}, 500
        #
        # try:
        #     server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
        #     if server is None:
        #         server = CoreLib.Server(adman_id=adman_id)
        #         session.add(server)
        #         session.commit()
        #
        #     # app.logger.debug("adman_id: {}".format(server.adman_id))
        #
        #     if hasattr(args, 'mac_addr') and args.mac_addr is not None:
        #         for addr in args.mac_addr:
        #             mac_exist = False
        #             # query to check mac-address exist
        #             filters = [
        #                 {'field': 'mac_addr', 'op': 'ilike', 'value': addr}
        #             ]
        #             macs = session.query(CoreLib.MacTable)
        #             macs = apply_filters(macs, filters)
        #             for mac in macs:
        #                 if mac.server_id == server.adman_id:
        #                     mac_exist = True
        #                 else:
        #                     msg = 'MAC-address already used by adman server ID: {}'.format(mac.server_id)
        #                     api.logger.error(msg)
        #                     return {"message": msg}, 500
        #
        #             if mac_exist:
        #                 continue
        #
        #             macaddr = CoreLib.MacTable(server_id=server.adman_id, mac_addr=addr)
        #             api.logger.debug('Add MAC: {}'.format(addr))
        #             session.add(macaddr)
        #         session.commit()
        #
        # except Exception as e:
        #     msg = 'Can\'t configure server. Error: {}'.format(str(e))
        #     api.logger.error(msg)
        #     return {"message": msg}, 500

        # return {"server.id": server.id}


# # server_install_put_parser = reqparse.RequestParser(bundle_errors=True)
# # server_install_put_parser.add_argument('os', help="Family of installing operating system", required=True)
# # server_install_put_parser.add_argument('osver', help="OS release version", required=True)
#
#
# @api.route('/install/<int:adman_id>', endpoint='server_install_ep')
# class ServerInstall(Resource):
#     @api.doc(security='apikey')
#     @api.doc(params={'adman_id': 'ID сервера в оборудовании ADMAN'})
#     # @api.expect(server_install_put_parser)
#     def put(self, adman_id):  # Create PUT endpoint
#         """
#         Install OS on server
#         """
#         headers = request.headers
#         api.logger.debug(headers)
#         auth = headers.get("X-Api-Key")
#         if auth != config.auth['adman']:
#             api.logger.debug('Unauthorized, 401')
#             return {"message": "Error: Unauthorized"}, 401
#
#         # args = server_install_put_parser.parse_args()
#         args = None
#
#         try:
#             session = sessionmaker(bind=core.engine)()
#         except Exception as e:
#             msg = 'Can\'t initialize session. Error: {}'.format(str(e))
#             api.logger.error(msg)
#             return {"message": msg}, 500
#
#         try:
#             server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
#             if server is None:
#                 raise Exception('NotFound', 'Server with ID: {} not found. Run configure server first.'.format(adman_id))
#
#             Grub.update_template(args)
#             Grub.mkconfig(adman_id)
#
#         except Exception as e:
#             msg = 'Can\'t run server install process. Error: {}'.format(str(e))
#             api.logger.error(msg)
#             return {"message": msg}, 500
#
#         return {"message": "success"}


# @api.route('/complete/<int:adman_id>/<string:token>', endpoint='server_install_complete_ep')
# class ServerInstallComplete(Resource):
#     @api.doc(params={
#         'adman_id': 'ID сервера в оборудовании ADMAN',
#         'token': 'Токен установки, генерируется при инициализации установки'
#     })
#     def get(self, adman_id, token):
#         """
#         Сообщить о завершении установки ОС
#         """
#         # args = InstallParams(os='local', osver='0')
#
#         try:
#             session = sessionmaker(bind=core.engine)()
#         except Exception as e:
#             msg = 'Can\'t initialize session. Error: {}'.format(str(e))
#             api.logger.error(msg)
#             return {"message": msg}, 500
#
#         try:
#             server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
#             if server is None:
#                 raise Exception('NotFound', 'Server with ID: {} not found. Run configure server first.'.format(adman_id))
#
#             # Проверить токен
#             # return {"message": "Error: Unauthorized"}, 401
#
#             # Grub.update_template(args)
#             # Grub.mkconfig(adman_id)
#
#         except Exception as e:
#             msg = 'Can\'t execute finish installation. Error: {}'.format(str(e))
#             api.logger.error(msg)
#             return {"message": msg}, 500
#
#         return {"message": "success"}