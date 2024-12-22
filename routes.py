from flask_app import app, db
from flask import request, jsonify
from agents import *
from retrievers import *
from db_models import *
from llama_index.core import Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings



def initiatlize_retrievers(_styling_instructions, _doc):
    retrievers ={}
    style_index =  VectorStoreIndex.from_documents([Document(text=x) for x in _styling_instructions])
    retrievers['style_index'] = style_index
    retrievers['dataframe_index'] =  VectorStoreIndex.from_documents([Document(text=x) for x in _doc])

    return retrievers



retrievers = {}


AVAILABLE_AGENTS = {
    "data_viz_agent":data_viz_agent,
    "sk_learn_agent":sk_learn_agent,
    "statistical_analytics_agent":statistical_analytics_agent,
    "preprocessing_agent":preprocessing_agent
}

ai_system = auto_analyst(agents=list(AVAILABLE_AGENTS.values()),retrievers=retrievers)
# Get all queries
@app.route('/queries', methods=['GET'])
def get_queries():
    queries = Query.query.order_by(Query.created_at.desc()).all()
    return jsonify([query.to_json() for query in queries])

# Get query by id 
@app.route('/queries/<int:id>', methods=['GET'])
def get_query(id):
    query = Query.query.get_or_404(id)
    return jsonify(query.to_json())

# Get all responses
@app.route('/responses', methods=['GET']) 
def get_responses():
    responses = Response.query.order_by(Response.created_at.desc()).all()
    return jsonify([response.to_json() for response in responses])

# Get responses by query id
@app.route('/responses/query/<int:query_id>', methods=['GET'])
def get_responses_by_query(query_id):
    responses = Response.query.filter_by(query_id=query_id).order_by(Response.created_at.desc()).all()
    return jsonify([response.to_json() for response in responses])

# Chat with specific agent
@app.route('/chat/<agent_name>', methods=['POST'])
def chat_with_agent(agent_name):
    data = request.get_json()
    query_text = data.get('query')
    
    # Save query
    query = Query(query=query_text)
    db.session.add(query)
    db.session.commit()
    
    # Generate response using agent
    if agent_name in AVAILABLE_AGENTS:
        agent = AVAILABLE_AGENTS[agent_name]()
        response_text = agent.generate_response(query_text)
        
        # Save response
        response = Response(
            agent_name=agent_name,
            query=query_text,
            response=response_text
        )
        db.session.add(response)
        db.session.commit()
        
        return jsonify(response.to_json()), 201
    else:
        return jsonify({"error": "Agent not found"}), 404

# Chat with all agents
@app.route('/chat', methods=['POST'])
def chat_with_all():
    data = request.get_json()
    query_text = data.get('query')
    
    # Save query
    query = Query(query=query_text)
    db.session.add(query)
    db.session.commit()
    
    responses = []
    
    # Get response from each agent
    for agent_name, agent_class in AVAILABLE_AGENTS.items():
        agent = agent_class()
        response_text = agent.generate_response(query_text)
        
        # Save response
        response = Response(
            agent_name=agent_name,
            query=query_text,
            response=response_text
        )
        db.session.add(response)
        responses.append(response)
    
    db.session.commit()
    
    return jsonify([response.to_json() for response in responses]), 201





