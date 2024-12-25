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
import routes

load_dotenv()



app = Flask(__name__)
# Remove CORS initialization
# cors = CORS(app, origins='*')

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///response.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")



db = SQLAlchemy(app)

with app.app_context():
  db.create_all()

if __name__ == '__main__':
    print("Starting Flask App")
    # print(app.config['SQLALCHEMY_DATABASE_URI'])
    # os.environ['FLASK_APP'] = 'flask_app.py'
    app.run(debug=True, port=5000)


    # Set the Flask application environment variable
    

    # You can now run the app using:
    # flask run --port 5000
    # Or with debug mode:
    # flask run --debug --port 5000
