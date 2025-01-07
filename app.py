from dotenv import load_dotenv
import sys
sys.dont_write_bytecode = True
load_dotenv()

from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from endpoint.Chat import Chat
from endpoint.InsertData import InsertData
from endpoint.UpdateData import UpdateData
from endpoint.DeleteData import DeleteData

app = Flask(__name__)

debug = True
CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

api.add_resource(Chat, '/chat')
api.add_resource(InsertData, '/insert')
api.add_resource(UpdateData, '/update')
api.add_resource(DeleteData, '/delete')

if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0')
