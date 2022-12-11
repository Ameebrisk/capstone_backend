from db import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_marshmallow import Marshmallow
import marshmallow as ma
from product_category_association import product_category_association_table
from product_order_association import product_order_association_table



class Products(db.Model):
  __tablename__ = 'Products'
  product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  product_name = db.Column(db.String(), unique=True, nullable=False)
  product_description = db.Column(db.String(), unique=True)
  product_total_price = db.Column(db.Float(), unique=True, nullable=False)
  active = db.Column(db.Boolean(), nullable=False)
  
  category = db.relationship('Categories', secondary=product_category_association_table, back_populates='product')
  order = db.relationship('Orders', secondary=product_order_association_table, back_populates='product')

  def __init__(self, product_name, product_description, product_total_price, active):
    self.product_name = product_name
    self.product_description = product_description
    self.product_total_price = product_total_price
    self.active = active
    


class ProductsSchema(ma.Schema):
  category = ma.fields.Nested('CategoriesSchema', many=True, only=['category_id', 'name'])
  order = ma.fields.Nested('OrdersSchema', many=True, only=['order_id', 'user_id', 'order_date', 'order_completed'])

  class Meta:
    fields = ['product_id', 'product_name', 'product_description', 'product_total_price', 'active', 'category', 'order']


product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)