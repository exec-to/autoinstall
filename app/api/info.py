# -*- coding: UTF-8 -*-
from flask_restx import Namespace, Resource, errors, fields, abort
from flask import url_for, request, jsonify, Response
from app.core.utils import Utils

api = Namespace('info', description='Раздел: Информация о конфигурации')


@api.route('/netplan/<string:ip_addr>', endpoint='network_config_ep')
class NetplanConfig(Resource):
    def get(self, ip_addr):
        """
        Генерация конфигурации сети для бездисковой загрузки.
        """

        gw, _, pr = Utils.get_network_settings(ip_addr)
        # /etc/netplan/01-netcfg.yaml
        network_template = """# This file describes the network interfaces available on your system
# For more information, see netplan(5).
network:
  version: 2
  renderer: networkd
  ethernets:
    enp6s0:
      dhcp4: yes
  vlans:
    vlan.1:
      id: 1
      optional: true
      dhcp4: false
      dhcp6: false
      link: enp6s0
      addresses: [ "{0}/{1}" ]
      gateway4: {2}
      nameservers:
          addresses:
              - "8.8.8.8"
"""
        return Response(network_template.format(ip_addr, pr, gw), mimetype='text/plain')
