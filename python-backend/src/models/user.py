from flask_sqlalchemy import SQLAlchemy
import re

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
    
    def validate(self):
        """Valida los datos del usuario"""
        errors = []
        
        if not self.username or len(self.username.strip()) < 2:
            errors.append("Username debe tener al menos 2 caracteres")
        
        if not self.email or not self._is_valid_email(self.email):
            errors.append("Email debe tener un formato válido")
            
        return errors
    
    def _is_valid_email(self, email):
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
