from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import os
import json
from datetime import datetime
from modul.mongo import MongoDBClient

mongo_client = MongoDBClient()

class DeleteData(Resource):
    def post(self):
        start = datetime.now()
        try:
            payload = json.loads(request.data.decode('utf-8'))
            filter_criteria = payload['filter_criteria']
            mongo_client.delete_data(filter_criteria)
            return jsonify({
                "success": True,
                "data": "Data deleted successfully",
                "elapsed_time": str(datetime.now() - start)
            })
        except Exception as e:
            result = {
                "success": False,
                "data": str(e)
            }
            return result