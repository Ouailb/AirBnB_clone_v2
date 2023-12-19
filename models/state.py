#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        """Returns the list of City objects linked to the current state."""
        cities = models.storage.all()
        cl = [c for c in cities.
              values() if isinstance(c, models.c) and c.state_id == self.id]
        return cl
