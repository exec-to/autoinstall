# -*- coding: UTF-8 -*-
from flask import Flask, Blueprint, render_template, url_for, request, jsonify
from flask_restx import Resource, Api, reqparse, fields, errors
import logging
import os
import shutil
from app import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy_filters import apply_filters
from app import core as CoreLib


app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1.0')
api = Api(blueprint,
          version='1.0',
          title='Autoinstall API',
          description='Autoinstall API',
          authorizations=config.authorizations
)

app.register_blueprint(blueprint)
core = CoreLib.Core()


server_model = api.model('Model', {
    'id': fields.String,
    'adman_id': fields.String,
    'uri': fields.Url('api.server_configure_ep', absolute = True),
    'message': fields.String
})


logging.basicConfig(
    format=u'%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    filename="/var/log/docker-flask.log"
)

@api.route('/servers', endpoint='servers_list_ep')
class Servers(Resource):
    @api.doc(security='apikey')
    @api.marshal_with(server_model)
    def get(self):  # Create GET endpoint
        """
        returns a list of servers
        """
        headers = request.headers
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            app.logger.debug('Unauthorized, 401')
            return {"message": "Error: Unauthorized"}, 401
        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Can\'t initialize session. Error: {}'.format(str(e))
            app.logger.error(msg)
            return {"message": msg}, 500

        try:
            servers = session.query(CoreLib.Server).all()

        except Exception as e:
            msg = 'Can\'t get servers. Error: {}'.format(str(e))
            app.logger.error(msg)
            return {"message": msg}, 500

        return servers


# TODO: Check for duplicate MAC-address on many servers
@api.route('/servers/configure/<int:adman_id>', endpoint='server_configure_ep')
class ServerConfigure(Resource):
    """
    Configure server
    """
    @api.doc(security='apikey')
    def put(self, adman_id):  # Create GET endpoint
        headers = request.headers
        app.logger.debug(headers)
        auth = headers.get("X-Api-Key")
        if auth != config.auth['adman']:
            app.logger.debug('Unauthorized, 401')
            return {"message": "Error: Unauthorized"}, 401

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('mac_addr', action='append', help="List of server MAC-address")
        args = parser.parse_args()

        app.logger.debug("args: {}".format(args))

        try:
            session = sessionmaker(bind=core.engine)()
        except Exception as e:
            msg = 'Can\'t initialize session. Error: {}'.format(str(e))
            app.logger.error(msg)
            return {"message": msg}, 500

        try:
            server = session.query(CoreLib.Server).filter_by(adman_id=adman_id).first()
            if server is None:
                server = CoreLib.Server(adman_id=adman_id)
                session.add(server)
                session.commit()

            app.logger.debug("adman_id: {}".format(server.adman_id))

            if hasattr(args, 'mac_addr') and args.mac_addr is not None:
                for addr in args.mac_addr:
                    mac_exist = False
                    # query to check mac-address exist
                    filters = [
                        {'field': 'mac_addr', 'op': 'ilike', 'value': addr}
                    ]
                    macs = session.query(CoreLib.MacTable)
                    macs = apply_filters(macs, filters)
                    for mac in macs:
                        if mac.server_id == server.adman_id:
                            mac_exist = True
                        else:
                            msg = 'MAC-address already used by adman server ID: {}'.format(mac.server_id)
                            app.logger.error(msg)
                            return {"message": msg}, 500

                    if mac_exist:
                        continue

                    macaddr = CoreLib.MacTable(server_id=server.adman_id, mac_addr=addr)
                    app.logger.debug('Add MAC: {}'.format(addr))
                    session.add(macaddr)
                session.commit()

        except Exception as e:
            msg = 'Can\'t configure server. Error: {}'.format(str(e))
            app.logger.error(msg)
            return {"message": msg}, 500

        return {"server.id": server.id}



# @api.route('/start/<server>') # from adman
# @api.route('/finish/<server>') # from server



# Function to Change root directory of the process.
# def change_root_directory(path):
#     try:
#         os.chdir(path)
#         os.chroot(path)
#     except Exception as e:
#         app.logger.debug('Не могу выполнить chroot: {}'.format(str(e)))
#         pass

# @api.route('/api/v1.0/complete/<server>')
# def complete_install(server):
#     """
#     returns a list of complete
#     """
#     default = dict(
#         CHROOT_PATH='/opt/autoinst',
#         GRUB_CONF_PATH='/srv/tftp/boot/grub/conf.d',
#         TMP_GRUB_CONF_PATH='/var/grub',
#         PRESEED_CONF_PATH='',
#         SRV_NAME='s300'
#     )
#
#     real_root = os.open("/", os.O_RDONLY)
#
#     # chroot
#     change_root_directory(default['CHROOT_PATH'])
#
#     app.logger.debug('chroot path')
#     app.logger.debug(default['CHROOT_PATH'])
#
#     tmp_grub_cfg = '{path}/{file}.cfg'.format(
#         path=str(default['TMP_GRUB_CONF_PATH']),
#         file=server
#     )
#
#     # print(tmp_grub_cfg)
#     stream = os.popen('/usr/sbin/grub-mkconfig -o {}'.format(tmp_grub_cfg))
#     output = stream.read()
#     app.logger.debug(output)
#     # os.system('/usr/sbin/grub-mkconfig -o {}'.format(tmp_grub_cfg))
#
#     os.fchdir(real_root)
#     os.chroot(".")
#
#     # back to real root
#     os.close(real_root)
#
#     real_grub_cfg = '{chroot}{path}/{file}.cfg'.format(
#         chroot=str(default['CHROOT_PATH']),
#         path=str(default['TMP_GRUB_CONF_PATH']),
#         file=server
#     )
#
#     # print(real_grub_cfg)
#
#     if os.path.isfile(real_grub_cfg):
#         # print ("File exist")
#
#         grub_cfg = '{path}/{srv}/grub.cfg'.format(
#             path=str(default['GRUB_CONF_PATH']),
#             srv=server
#         )
#         os.remove(grub_cfg)
#         shutil.copy(real_grub_cfg, grub_cfg)
#
#     return '3'
