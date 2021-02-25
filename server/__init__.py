from flask import Flask

app = Flask(__name__)

@app.route("/")
def root():
    return "<h1>Tenant Gateway!!!</h1>"

def create_app():
    #Create app
    global app
    
    
    #Intialize modules
    from server.api.routes import api
    app.register_blueprint(api, url_prefix="/tenant-gateway/v1")
    return app