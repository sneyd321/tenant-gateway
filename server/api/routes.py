from . import api
from flask import request, Response, jsonify
import requests, uuid, pika, json




def get_house_service():
    return "http://house-service.default.svc.cluster.local:8082/house/v1/"
   
def get_tenant_service():
    return "http://tenant-service.default.svc.cluster.local:8083/tenant/v1/"


def handle_post(url, request):
    try:
        response = requests.post(url, json=request.get_json(), headers=request.headers)
        return Response(response=response.text, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)

def handle_put(url, request):
    try: 
        response = requests.put(url, json=request.get_json(), headers=request.headers)
        return Response(response=response.text, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)


def handle_get(url, request):
    try:
        response = requests.get(url, headers=request.headers)
        if response.ok:
            return jsonify(response.json())
        return Response(response=response.text, status=response.status_code)
    except requests.exceptions.ConnectionError:
        return Response(response="Error: Service currently unavailable.", status=503)

def authenticate_tenant(request):
    try:
        response = requests.get(get_tenant_service() + "Tenant", headers=request.headers)
        if response.ok:
            return True
        return False
    except requests.exceptions.ConnectionError:
        return False
   


#############################################################

@api.route("House/<int:houseId>")
def get_house(houseId):
    tenantData = authenticate_tenant(request)
    if tenantData:
        url = get_house_service() + "House/" + str(houseId)
        return handle_get(url, request)
    return Response(response="Not Authorized", status=401)

#############################################################

@api.route("/", methods=["GET", "POST"])
def create_tenant_account():
    if request.method == "GET":
        try:
            response = requests.get(get_tenant_service() + "SignUp", headers=request.headers)
            if response.ok:
                return response.text
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Service currently unavailable.", status=503)

    if request.method == "POST":
        print(request.form, flush=True)
        try:
            response = requests.post(get_tenant_service() + "SignUp", data=request.form, headers=request.headers)
            if response.ok:
                return response.text
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Service currently unavailable.", status=503)



@api.route("Tenant", methods=["GET"])
def get_tenant():
    tenantData = authenticate_tenant(request)
    if tenantData:
        url = get_tenant_service() + "Tenant"
        return handle_get(url, request)
    return Response(response="Not Authorized", status=401)

##########################################################

@api.route("Login")
def login_tenant():
    url = get_tenant_service() + "Login"
    return handle_post(url, request)


####################################################

@api.route("Problem", methods=["POST"])
def create_problem():
    tenantData = authenticate_tenant(request)
    if tenantData:
        url = get_house_service() + "Problem"
        image = request.files["image"]
        data = request.form['data']
        dataToDict = json.loads(data)
        files = {
            "image": (image.filename, image.read(), "image/jpg"),
            "data": ("data", json.dumps(dataToDict), "application/json")
        }
        try:
            response = requests.post(url, files=files)
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Service currently unavailable.", status=503)
    return Response(response="Not Authorized", status=401)

@api.route("House/<int:houseId>/Problem")
def get_problems(houseId):
    tenantData = authenticate_tenant(request)
    if tenantData:
        url = get_house_service() + "House/" + str(houseId) + "/Problem"
        return handle_get(url, request)
    return Response(response="Not Authorized", status=401)



