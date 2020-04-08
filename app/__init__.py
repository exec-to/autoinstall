from flask import Flask
app = Flask(__name__)
from app import views
import logging

logging.basicConfig(
    format=u'%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    filename="/var/log/docker-flask.log"
)