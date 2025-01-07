from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from modul.mongo import MongoDBClient
import os
import json
from datetime import datetime
from modul.llm import LLMClient

llm_client = LLMClient()
mongo_client = MongoDBClient()

class Chat(Resource):
    def post(self):
        start = datetime.now()
        stream = False
        try:
            payload = json.loads(request.data.decode('utf-8'))
            question = payload['prompt']
            if 'stream' in payload:
                stream = payload['stream']
            
            context = mongo_client.vector_search(question, "sample_mflix", "embedded_movies")
            response = llm_client.chat(question, context, stream, 0)
            return jsonify({
                "success": True,
                "data": response,
                "elapsed_time": str(datetime.now() - start)
            })
        except Exception as e:
            result = {
                "success": False,
                "data": str(e)
            }
            return result

