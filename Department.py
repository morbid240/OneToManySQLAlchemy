from orm_base import Base
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine
from sqlalchemy import Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from typing import List  # Use this for the list of courses offered by the department
from constants import START_OVER, INTROSPECT_TABLES, REUSE_NO_INTROSPECTION
import DepartmentClass as DC

# Find out whether we're introspecting or recreating.
introspection_type = IntrospectionFactory().introspection_type

if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:  
    class Department(Base):
        __tablename__ = DC.__tablename__
        name: Mapped[str] = DC.name
        abbreviation: Mapped[str] = DC.abbreviation
        courses: Mapped[List["Course"]] = DC.courses
        __table_args__ = DC.__table_args__
        def __init__(self, abbreviation: str, name: str):
            self.init(self, abbreviation, name)
elif introspection_type == INTROSPECT_TABLES:
    class Department(Base):
        # Creating the Table object does the introspection.  Basically, __table__
        # allows SQLAlchemy to copy the metadata from the Table object into Base.metadata.
        __table__ = Table(DC.__tablename__, Base.metadata, autoload_with=engine)
        # The courses list will not get created just from introspecting the database, so I'm doing that here.
        courses: Mapped[List["Course"]] = DC.courses
        abbreviation: Mapped[str] = column_property(__table__.c.abbreviation)

        def __init__(self, abbreviation: str, name: str):
            self.init(self, abbreviation, name)




setattr(Department, 'add_course', DC.add_course)
setattr(Department, 'remove_course', DC.remove_course)
setattr(Department, 'get_courses', DC.get_courses)

setattr(Department, 'init', DC.init)
setattr(Department, '__str__', DC.__str__)
