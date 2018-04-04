#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps
from libpurecoollink.dyson import DysonAccount

app = Flask(__name__)
api = Api(app)


class Login(Resource):
    def post(self):
        Email = request.json['email']
        Password = request.json['password']
        Language = request.json['language']
        dyson_account = DysonAccount(
            Email, Password, Language)
        logged = dyson_account.login()
        if not logged:
            return {'success': False, 'message': 'Unable to login to Dyson account'}
        # List devices available on the Dyson account
        devices = dyson_account.devices()
        # Connect using discovery to the first device
        connected = devices[0].auto_connect()
        if not connected:
            return {'success': False, 'message': 'Successfully authenticated but unable to connect to your first device : ' + devices[0]}
        return jsonify(devices[0].state)


api.add_resource(Login, '/login')  # Route_3

if __name__ == '__main__':
    app.run()
