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

"""Methods for manipulating department objects. List is defined outside in main
I am wary of imports. """
def add_department(session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_abbreviation: bool = False
    name: str = ''
    abbreviation: str = ''
    while not unique_abbreviation or not unique_name:
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        name_count: int = session.query(Department).filter(Department.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a department by that name.  Try again.")
        if unique_name:
            abbreviation_count = session.query(Department). \
                filter(Department.abbreviation == abbreviation).count()
            unique_abbreviation = abbreviation_count == 0
            if not unique_abbreviation:
                print("We already have a department with that abbreviation.  Try again.")
    new_department = Department(abbreviation, name)
    session.add(new_department)


def select_department(session) -> Department:
    """
    Prompt the user for a specific department by the department abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = session.query(Department). \
            filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    # return queried department
    return session.query(Department).filter(Department.abbreviation == abbreviation).first()


def delete_department(session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
            "then come back here to delete the department.")
    else:
        session.delete(department)





setattr(Department, 'add_course', DC.add_course)
setattr(Department, 'remove_course', DC.remove_course)
setattr(Department, 'get_courses', DC.get_courses)

setattr(Department, 'init', DC.init)
setattr(Department, '__str__', DC.__str__)
