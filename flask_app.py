from flask import Flask
# Remove flask-cors import since it's not installed
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# from agents import *
# import retrievers 
# import memory_agents
# import marketing_analytics_agents
# import pandas as pd
from dotenv import load_dotenv
import os
# from routes import *

load_dotenv()



app = Flask(__name__)
# Remove CORS initialization
cors = CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///response.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")



db = SQLAlchemy(app)

with app.app_context():
  db.create_all()

if __name__ == '__main__':
    print("Starting Flask App")
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(debug=True, port=5000)
