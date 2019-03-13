from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    price = Column(Integer)
    name = Column(String)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order", back_populates="products")

    def __repr__(self):
        return "<User(id='%s', price='%i', name='%s', order_id='%i')>" % (
            self.id, self.price, self.name, self.order_id)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, Sequence('order_id_seq'), primary_key=True)
    cost = Column(Integer)
    place_date = Column(Date)
    recv_date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")
    products = relationship("Product", order_by=Product.order_id, back_populates="order")

    def __repr__(self):
        return "<User(id='%s', cost='%i', place_date='%s', recv_date='%s', user_id='%i')>" % (
            self.id, self.cost, self.place_date, self.recv_date, self.user_id)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String)
    fullname = Column(String)
    address = Column(String)
    orders = relationship("Order", order_by=Order.id, back_populates="user")

    def __repr__(self):
        return "<User(id='%s', username='%s', fullname='%s', address='%s')>" % (
            self.id, self.username, self.fullname, self.address)


engine = create_engine('sqlite:///db.db')  # , echo=True)
Base.metadata.create_all(engine)


class Repository:
    def __init__(self, table):
        self.table = table
        self.session = self.__get_session__()

    def __get_session__(self):
        Session = sessionmaker(bind=engine)
        return Session()

    def create(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get(self, id=None):
        if id is None:
            return self.session.query(self.table).all()
        return self.session.query(self.table).filter(User.id.is_(id)).first()

    def delete(self, id):
        obj = self.get(id)
        if obj is None:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True

    def update(self):
        self.session.commit()


if __name__ == "__main__":
    repo = Repository(User)
    repo2 = Repository(Product)
    test_user = User(username="name", fullname="full name", address="strada")
    # repo.create(test_user)
    # print(repo.get())
    # print(repo.delete(6))
    # update_test = repo.get(8)
    # update_test.username = "updated22"
    test_order = Order(cost=5, place_date=datetime.now().date())
    test_product = Product(name="name1", price=3)
    test_product_free = Product(name="name2", price=5)
    test_order.products.append(test_product)
    test_user.orders.append(test_order)
    repo.create(test_user)
    repo2.create(test_product_free)
    # repo.update()
