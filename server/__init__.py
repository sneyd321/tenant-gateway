from flask import Flask, Response
from kazoo.client import KazooClient, KazooState

app = Flask(__name__)



zk = KazooClient()


@app.route("/")
def root():
    return "<h1>Tenant Gateway!!!</h1>"



@app.route("/Health")
def health_check():
    return Response(status=200)

def create_app(env):
    #Create app
    global app

    if env == "prod":
        zk.set_hosts('zookeeper.default.svc.cluster.local:2181')
    elif env == "dev":
        zk.set_hosts('host.docker.internal:2181')
    else:
        return None

    zk.start()
    
    #Intialize modules
    from server.api.routes import api
    app.register_blueprint(api, url_prefix="/tenant-gateway/v1")
    return app