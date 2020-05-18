# -*- coding: UTF-8 -*-
from flask_restx import Namespace, Resource, errors, fields, abort
from app import config
from sqlalchemy.orm import sessionmaker
from sqlalchemy_filters import apply_filters
from flask import url_for, request, jsonify
from app import core as CoreLib
from app.core.utils import Utils

api = Namespace('os', description='Раздел: операционные системы')


@api.route('/', endpoint='os_list_ep')
class OsList(Resource):
    @api.doc(security='apikey')
    def get(self):  # Create GET endpoint
        """
        Получить список доступных для установки операционных систем
        """
        return config.os_list
