from db import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_marshmallow import Marshmallow
import marshmallow as ma



class Users(db.Model):
  __tablename__ = 'Users'
  user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  first_name = db.Column(db.String(), nullable=False)
  last_name = db.Column(db.String(), nullable=False)
  phone = db.Column(db.String(), nullable=False)
  email = db.Column(db.String(), nullable=False)
  street_address = db.Column(db.String(), nullable=False)
  city = db.Column(db.String(), nullable=False)
  state = db.Column(db.String(), nullable=False)
  postal_code = db.Column(db.String(), nullable=False)
  active = db.Column(db.Boolean(), default=False, nullable=False)
  # pet_info = db.relationship('PetInformation', back_populates='owner_info')

  def __init__(self, first_name, last_name, phone, email, street_address, city, state, postal_code, active):
    self.first_name = first_name
    self.last_name = last_name
    self.phone = phone
    self.email = email
    self.street_address = street_address
    self.city = city
    self.state = state
    self.postal_code = postal_code
    self.active = active


class UsersSchema(ma.Schema):
  # categories = ma.fields.Nested('Categories', many=True, only=['name']) 
  class Meta:
    fields = ['user_id', 'first_name', 'last_name', 'phone', 'email', 'street_address', 'city', 'state', 'postal_code', 'active']
# class UsersCategoriesSchema(ma.Schema):
#     fields = ['name']

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

# user_category_schema = UsersCategoriesSchema()
# users_category_schema = UsersCategoriesSchema(many = True)