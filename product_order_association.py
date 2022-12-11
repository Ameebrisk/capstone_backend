from db import db 
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma


product_order_association_table = db.Table(
  "ProductOrderAssociation",
  db.Model.metadata,
  db.Column('product_id', db.ForeignKey('Products.product_id'), primary_key=True),
  db.Column('order_id', db.ForeignKey('Orders.order_id'), primary_key=True),
  db.Column ('quantity',db.Integer())
)


class ProductOrderAssociationSchema(ma.Schema):
  class Meta:
    fields = ['product_id', 'order_id', 'quanitity']


product_association_schema = ProductOrderAssociationSchema()
products_association_schema = ProductOrderAssociationSchema(many=True)