# # Using base sqlalchemy
# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
#
# Base = declarative_base()
#
#
# class Order(Base):
#     id = Column(Integer, primary_key=True)
#
#
# class OrderLine(Base):
#     id = Column(Integer, primary_key=True)
#     sku = Column(String(250))
#     qty = Integer(String(250))
#     order_id = Column(Integer, ForeignKey('order.id'))
#     order = relationship(Order)


# Using mapper with class exist with table in database
from sqlalchemy.orm import mapper, relationship
from allocation.domain import models
from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey

metadata = MetaData()

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),
    Column("sku", String(255)),
    Column('_purchased_quantity', Integer, nullable=False),
    Column('eta', Date, nullable=True)
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    lines_mapper = mapper(models.OrderLine, order_lines)
    mapper(
        models.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper, secondary=allocations, collection_class=set
            )
        },
    )


def init_models(engine):
    metadata.create_all(bind=engine)
