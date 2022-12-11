from db import db 
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma


product_category_association_table = db.Table(
  "ProductCategoryAssociation",
  db.Model.metadata,
  db.Column('product_id', db.ForeignKey('Products.product_id'), primary_key=True),
  db.Column('category_id', db.ForeignKey('Categories.category_id'), primary_key=True)
)

class ProductCategoryAssociationSchema(ma.Schema):
  class Meta:
    fields = ['product_id', 'category_id']


product_association_schema = ProductCategoryAssociationSchema()
products_association_schema = ProductCategoryAssociationSchema(many=True)