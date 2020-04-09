from flask import Flask, Blueprint, render_template, url_for, request, jsonify
from flask_restx import Resource, Api, reqparse, fields
import logging
import os
import shutil

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1.0')
api = Api(blueprint, version='1.0', title='Autoinstall API', description='Autoinstall API')
app.register_blueprint(blueprint)

model = api.model('Model', {
    'task': fields.String,
    'uri': fields.Url('api.hello', absolute = True)
    # 'uri': fields.Url('api.hello_ep') relation 0xff00
})

class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'

logging.basicConfig(
    format=u'%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    filename="/var/log/docker-flask.log"
)

# Function to Change root directory of the process.
def change_root_directory(path):
    try:
        os.chdir(path)
        os.chroot(path)
    except Exception as e:
        app.logger.debug('Не могу выполнить chroot: {}'.format(str(e)))
        pass

#@api.route('/hello', endpoint='hello_ep' [default 'hello']) relation 0xff00
@api.route('/hello')
@api.doc(params={'rate': 'Rate limit'})
class Hello(Resource):  # Create a RESTful resource
    @api.marshal_with(model)
    def get(self):  # Create GET endpoint
        """
        returns a list of hello
        """
        return TodoDao(todo_id='my_todo', task='Remember the rate: {}'.format(5))

    def put(self):  # Create PUT endpoint
        """
        put method with arguments
        """
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('rate', type=int, help='Rate to charge for this resource', required=True)
        parser.add_argument('foo', type=int, required=True)
        parser.add_argument('bar', type=int, required=True)
        args = parser.parse_args()

        return args.rate
    # return render_template('hello.html', message="Hello World!")


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
