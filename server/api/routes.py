from . import api
from flask import request, Response, jsonify
import requests, uuid, pika, json
from server.api.RequestManager import Zookeeper, RequestManager

zookeeper = Zookeeper()


   
    
@api.route("FormComplete")
def form_complete():
    return Response(status=204)

#############################################################


@api.route("Document/<int:houseId>/Tenant")
def get_tenant_documents(houseId):
    tenantService = zookeeper.get_service("tenant-service")
    if not tenantService:
        return Response(response="Error: Tenant Service Currently Unavailable", status=503)

    tenantManager = RequestManager(request, tenantService)
    tenantId = tenantManager.authenticate()
    if not tenantId:
        return Response(response="Not Authorized", status=401)

    documentService = zookeeper.get_service("document-service")
    if not documentService:
        return Response(response="Error: Document Service Currently Unavailable", status=503)

    documentManager = RequestManager(request, documentService)
    return documentManager.get("document/v1/Document/" + str(houseId) + "/Tenant")

    
    

@api.route("House/<int:houseId>")
def get_house(houseId):
    tenantService = zookeeper.get_service("tenant-service")
    if not tenantService:
        return Response(response="Error: Tenant Service Currently Unavailable", status=503)

    tenantManager = RequestManager(request, tenantService)
    tenantId = tenantManager.authenticate()
    if not tenantId:
        return Response(response="Not Authorized", status=401)

    houseService = zookeeper.get_service("house-service")
    if not houseService:
        return Response(response="Error: House Service Currently Unavailable", status=503)

    houseManager = RequestManager(request, houseService)
    return houseManager.get("house/v1/House/" + str(houseId) + "/Tenant")
    
    



@api.route("/RentDetails/<int:houseId>")
def get_rent_details(houseId):
    tenantService = zookeeper.get_service("tenant-service")
    if not tenantService:
        return Response(response="Error: Tenant Service Currently Unavailable", status=503)

    tenantManager = RequestManager(request, tenantService)
    tenantId = tenantManager.authenticate()
    if not tenantId:
        return Response(response="Not Authorized", status=401)

    leaseService = zookeeper.get_service("lease-service")
    if not leaseService:
        return Response(response="Error: Rent Service Currently Unavailable", status=503)

    leaseManager = RequestManager(request, leaseService)
    return leaseManager.get("lease/v1/RentDetails/" + str(houseId) + "/Tenant")

    
   

@api.route("/Homeowner/<int:houseId>")
def get_homeowner(houseId):
    tenantService = zookeeper.get_service("tenant-service")
    if not tenantService:
        return Response(response="Error: Tenant Service Currently Unavailable", status=503)

    tenantManager = RequestManager(request, tenantService)
    tenantId = tenantManager.authenticate()
    if not tenantId:
        return Response(response="Not Authorized", status=401)

    houseService = zookeeper.get_service("house-service")
    if not houseService:
        return Response(response="Error: House Service Currently Unavailable", status=503)

    houseManager = RequestManager(request, houseService)
    houseResponse = houseManager.get("house/v1/House/" + str(houseId) + "/Tenant")
    houseData = houseResponse.get_json()
    homeownerId = houseData["homeownerId"]
    if not homeownerId:
        return Response(response="Error: Homeowner Not Found", status=404)

    homeownerService = zookeeper.get_service("homeowner-service")
    if not homeownerService:
        return Response(response="Error: Homeowner Service Currently Unavailable", status=503)

    homeownerManager = RequestManager(request, homeownerService)
    return homeownerManager.get("homeowner/v1/Homeowner/" + str(homeownerId))

    

    
 

#############################################################

@api.route("/")
def get_tenant_account():
    service = zookeeper.get_service("tenant-service")
    if not service:
        return Response(response="Error: Tenant Service Currently Unavailable", status=503)
    manager = RequestManager(request, service)
    return manager.get_html("/tenant/v1/")
    


@api.route("/", methods=["POST"])
def create_tenant_account():
    service = zookeeper.get_service("tenant-service")
    if not service:
        return Response(response="Error: Tenant Service Currently Unavailable", status=503)
    manager = RequestManager(request, service)
    return manager.post_html("/tenant/v1/")


        



@api.route("Tenant", methods=["GET"])
def get_tenant():
    tenantService = zookeeper.get_service("tenant-service")
    if not tenantService:
        return Response(response="Error: Homeowner Not Available", status=503)

    tenantManager = RequestManager(request, tenantService)
    tenantId = tenantManager.authenticate()
    if not tenantId:
        return Response(response="Not Authorized", status=401)

    return tenantManager.get("tenant/v1/Tenant")
    


##########################################################

@api.route("Login", methods=["POST"])
def login_tenant():
    service = zookeeper.get_service("tenant-service")
    if not service:
        return Response(response="Error: Zookeeper down", status=503)
    manager = RequestManager(request, service)
    return manager.post("tenant/v1/Login")
    
   


####################################################

@api.route("Problem", methods=["POST"])
def create_problem():
    tenantService = zookeeper.get_service("tenant-service")
    if not tenantService:
        return Response(response="Error: Tenant Service  Currently Unavailable", status=503)

    tenantManager = RequestManager(request, tenantService)
    tenantId = tenantManager.authenticate()
    if not tenantId:
        return Response(response="Not Authorized", status=401)

    problemService = zookeeper.get_service("problem-service")
    if not problemService:
        return Response(response="Error: Problem Service Currently Unavailable", status=503)

    problemManager = RequestManager(request, problemService)
    return problemManager.post_problem()
    
    
    

@api.route("House/<int:houseId>/Problem")
def get_problems(houseId):
    tenantService = zookeeper.get_service("tenant-service")
    if not tenantService:
        return Response(response="Error: Tenant Service Currently Unavailable", status=503)

    tenantManager = RequestManager(request, tenantService)
    tenantId = tenantManager.authenticate()
    if not tenantId:
        return Response(response="Not Authorized", status=401)

    problemService = zookeeper.get_service("problem-service")
    if not problemService:
        return Response(response="Error: Problem Service Currently Unavailable", status=503)

    problemManager = RequestManager(request, problemService)
    return problemManager.get("problem/v1/House/" + str(houseId) + "/Problem")

    
    




@api.route("Tenant/Profile", methods=["POST"])
def tenantProfile():
    tenantService = zookeeper.get_service("tenant-service")
    if not tenantService:
        return Response(response="Error: Homeowner Not Available", status=503)

    tenantManager = RequestManager(request, tenantService)
    tenantId = tenantManager.authenticate()
    if not tenantId:
        return Response(response="Not Authorized", status=401)

    imageUploadService = zookeeper.get_service("image-upload-service")
    if not imageUploadService:
        return Response(response="Error: Image Upload Not Available", status=503)

    imageUploadManager = RequestManager(request, imageUploadService)
    return imageUploadManager.post_profile(tenantId)
    
    
    
    