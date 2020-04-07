from app import app

@app.route('/')
def hello_world():
    return 'Hello World! ----- docker: 2'


@app.route('/complete/<server>')
def complete_install(server):
    return 'Hello %s' % server 


