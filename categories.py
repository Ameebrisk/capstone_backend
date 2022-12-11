from db import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_marshmallow import Marshmallow
import marshmallow as ma
from datetime import datetime
from product_category_association import product_category_association_table



class Categories(db.Model):
  __tablename__ = 'Categories'
  category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  name = db.Column(db.String(), unique=True, nullable=False)
  category_description = db.Column(db.String(), unique=True, nullable=False)
  active = db.Column(db.Boolean(), nullable=False)
  
  product = db.relationship('Products', secondary=product_category_association_table, back_populates='category')

  def __init__(self, category_id, name, category_description, active):
    self.category_id = category_id
    self.name = name
    self.category_description = category_description
    self.active = active
    
    


class CategoriesSchema(ma.Schema):
  product = ma.fields.Nested('ProductsSchema', many=True, only=['product_id', 'product_name', 'order'])
  categories = ma.fields.Nested('Categories', many=True, only=['name']) 
  class Meta:
    fields = ['category_id', 'name', 'category_description', 'active', 'product']


category_schema = CategoriesSchema()
categories_schema = CategoriesSchema(many=True)