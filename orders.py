from db import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_marshmallow import Marshmallow
import marshmallow as ma
from datetime import datetime
from product_order_association import product_order_association_table
from products import Products




class Orders(db.Model):
  __tablename__ = 'Orders'
  order_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
  user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
  order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  ship_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
  order_total_price = db.Column(db.Float(), nullable=False)
  order_completed = db.Column(db.Boolean(), nullable=False)
  
  product = db.relationship('Products', secondary=product_order_association_table, back_populates='order')

  def __init__(self, user_id, order_total_price,order_completed):
    self.user_id = user_id
    self.order_total_price = order_total_price
    self.order_completed = order_completed
    


class OrdersSchema(ma.Schema):
  product = ma.fields.Nested('ProductsSchema', many=True, only=['product_id', 'product_name'])
  class Meta:
    fields = ['order_id', 'user_id', 'order_date', 'ship_date', 'order_total_price', 'order_completed', 'product']


order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)