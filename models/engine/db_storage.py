#!/usr/bin/python3
""" New engine DBStorage """
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ SQLAlchemy  Configuration"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """return a dictionary: (like FileStorage)"""

        dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for q in query:
                key = "{}.{}".format(type(q).__name__, q.id)
                dict[key] = q
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for clase in classes:
                query = self.__session.query(clase)
                for q in query:
                    key = "{}.{}".format(type(q).__name__, q.id)
                    dict[key] = q
        return (dict)

    def new(self, obj):
        """add a new element in the table
        """
        self.__session.add(obj)

    def save(self):
        """save changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete an object"""
        if obj:
            self.session.delete(obj)

    def reload(self):
        """reload the db maybe like cache"""
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """ calls remove()
        """
        self.__session.close()
