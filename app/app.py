# -*- coding: UTF-8 -*-
from flask import Flask
from app.api import blueprint as api
import logging

app = Flask(__name__)
app.register_blueprint(api)

logging.basicConfig(
    format=u'%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    filename="/var/log/docker-flask.log"
)
