from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import os
import json
from datetime import datetime
from modul.mongo import MongoDBClient

mongo_client = MongoDBClient()

class InsertData(Resource):
    def post(self):
        start = datetime.now()
        try:
            payload = json.loads(request.data.decode('utf-8'))
            data = payload['data']
            mongo_client.insert_data(data)
            return jsonify({
                "success": True,
                "data": "Data inserted successfully",
                "elapsed_time": str(datetime.now() - start)
            })
        except Exception as e:
            result = {
                "success": False,
                "data": str(e)
            }
            return result
