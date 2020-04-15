# -*- coding: UTF-8 -*-
from flask import Blueprint
from flask_restx import Api
from .servers import api as ns1
from .install import api as ns2
from app import config

blueprint = Blueprint('api', __name__, url_prefix='/api/v1.0')
api = Api(blueprint,
          version='1.0',
          title='Autoinstall API',
          description='API для установки операционных систем на выделенные серверы',
          authorizations=config.authorizations
          )

api.add_namespace(ns1, path='/servers')
api.add_namespace(ns2, path='/install')
