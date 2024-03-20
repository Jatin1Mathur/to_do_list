
from enum import Enum 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class StatusEnum(Enum):
    PENDING = 0
    COMPLETED = 1

class databaseTodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255), nullable=True)
    checked = db.Column(db.Enum(StatusEnum), default=StatusEnum.PENDING)