import requests
from flask import Response, jsonify, redirect
from server import app, zk


class Zookeeper:

    def __init__(self):
        self._zookeeper = zk

    def get_service(self, service):
        if self._zookeeper.exists("/RoomR/Services/" + service):
            data, stat = self._zookeeper.get("/RoomR/Services/" + service)
            return data.decode("utf-8")
        return None


class RequestManager:

    def __init__(self, request, service):
        self.request = request
        self.service = service


    def post(self, resource):
        try:
            response = requests.post("http://" + self.service + "/" + resource, json=self.request.get_json(), headers=self.request.headers)
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Service currently unavailable.", status=503)

    def put(self, resource):
        try: 
            response = requests.put("http://" + self.service + "/" + resource, json=self.request.get_json(), headers=self.request.headers)
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Service currently unavailable.", status=503)


    def get(self, resource):
        try:
            print(self.service, flush=True)
            response = requests.get("http://" + self.service + "/" + resource, headers=self.request.headers)
            if response.ok:
                return jsonify(response.json())
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Service currently unavailable.", status=503)


    
    def authenticate(self, **kwargs):
        headers = kwargs.get("headers", self.request.headers)
        try:
            response = requests.get("http://" + self.service + "/tenant/v1/Verify", headers=headers)
            if response.ok:
                homeownerData = response.json()
                return homeownerData["homeownerId"]
            return None
        except requests.exceptions.ConnectionError:
            return None
   


    def get_html(self, resource):
        try:
            response = requests.get("http://" + self.service + resource, headers=self.request.headers)
            print(response.status_code)
            if response.ok:
                return response.text
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Service currently unavailable.", status=503)



    def post_html(self, resource, **kwargs):
        headers = kwargs.get("headers", self.request.headers)
        try:
            
            response = requests.post("http://" + self.service + resource, data=self.request.form, headers=headers)
            if response.status_code == 201:
                return redirect("http://192.168.0.108:8080/homeowner-gateway/v1/" + response.text)
            return Response(response=response.text, status=response.status_code)
        except requests.exceptions.ConnectionError:
            return Response(response="Error: Service currently unavailable.", status=503)


