from flask_app import db


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_name = db.Column(db.String(255))
    query = db.Column(db.String(255))
    response = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_json(self):
        return {
        "id":self.id,
        "agent_name":self.agent_name,
        "query":self.query,
        "response":self.response,
        "created_at":self.created_at
        }

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.now())

    def to_json(self):
        return {
            "id":self.id,
            "query":self.query,
            "created_at":self.created_at
        }

