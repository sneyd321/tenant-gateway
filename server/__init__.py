from flask import Flask, Response
from kazoo.client import KazooClient, KazooState

app = Flask(__name__)



zk = KazooClient(hosts='host.docker.internal:2181')
zk.start()

@app.route("/")
def root():
    return "<h1>Tenant Gateway!!!</h1>"



@app.route("/Health")
def health_check():
    return Response(status=200)

def create_app():
    #Create app
    global app
    
    
    #Intialize modules
    from server.api.routes import api
    app.register_blueprint(api, url_prefix="/tenant-gateway/v1")
    return app