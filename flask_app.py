from flask import Flask, request, jsonify
# Remove flask-cors import since it's not installed
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# from agents import *
# import retrievers 
# import memory_agents
# import marketing_analytics_agents
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()



app = Flask(__name__)
# Remove CORS initialization
cors = CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///response.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")



db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
