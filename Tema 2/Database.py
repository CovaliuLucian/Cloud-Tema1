from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<User(id='%s', username='%s', fullname='%s')>" % (self.id, self.username, self.fullname)


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
    test_user = User(username="name", fullname="full name")
    repo.create(test_user)
    print(repo.get())
    print(repo.delete(6))
    update_test = repo.get(8)
    update_test.username = "updated22"
    repo.update()
