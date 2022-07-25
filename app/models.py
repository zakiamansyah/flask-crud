from app import db

class Employes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telp = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    
    def __init__(self, name, email, telp, address):
        self.name = name
        self.email = email
        self.telp = telp
        self.address = address