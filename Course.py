
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint

from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property

from orm_base import Base
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine

from sqlalchemy import Table
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from typing import List  # Use this for the list of courses offered by the department
from constants import START_OVER, INTROSPECT_TABLES, REUSE_NO_INTROSPECTION
from sqlalchemy import Table

from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES
from typing import List  # Use this for the list of sections by course

import CourseClass as CC

introspection_type = IntrospectionFactory().introspection_type

if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
    class Course(Base):
        __tablename__ = CC.__tablename__ 
        departmentAbbreviation: Mapped[str] = CC.departmentAbbreviation
        department: Mapped["Department"] = CC.department
        courseNumber: Mapped[int] = CC.courseNumber
        name: Mapped[str] = CC.name
        description: Mapped[str] = CC.description
        units: Mapped[int] = CC.units
        sections: Mapped[List["Section"]] = CC.sections

        __table_args__ = CC.__table_args__

        def __init__(self, department: Department, courseNumber: int, name: str, description: str, units: int):
            """This is a hack.  I found that I could not add __init__ to the class from outside the
            class definition block.  But I did not want to write the code for the __init__ twice.  So
            I created this helper function that I just called init, and call that in __init__ to do
            the actual work.  init only gets written once, saving me the worry of redundant code
            between __init__ for the two different introspection approaches.
            :param      department:     The Department instance that owns the new course.
            :param      courseNumber:   The number of the new course.
            :param      description:    Textual narrative of the course contents.
            :param      units:          The number of academic hours awarded for a passing grade.
            :return:                    None"""
            self.init(department, courseNumber, name, description, units)

elif introspection_type == INTROSPECT_TABLES:
    class Course(Base):
        __table__ = Table(CC.table_name, Base.metadata, autoload_with=engine)
        # Otherwise, this property will be named department_abbreviation
        departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
        # This back_populates will not be created by the introspection.
        department: Mapped["Department"] = CC.department
        # Otherwise, this property will be named course_number
        courseNumber: Mapped[int] = column_property(__table__.c.course_number)

        def __init__(self, department: Department, courseNumber: int, name: str, description: str, units: int):
            self.init(department, courseNumber, name, description, units)


def set_department(self, department: Department):
    """
    Accept a new department without checking for any uniqueness.
    I'm going to assume that either a) the caller checked that first
    and/or b) the database will raise its own exception.
    :param department:  The new department for the course.
    :return:            None
    """
    self.department = department
    self.departmentAbbreviation = department.abbreviation


def init(self, department: Department, courseNumber: int, name: str, description: str, units: int):
    self.set_department(department)
    self.courseNumber = courseNumber
    self.name = name
    self.description = description
    self.units = units


def __str__(self):
    return f"Department abbrev: {self.departmentAbbreviation} number: {self.courseNumber} name: {self.name} units: {self.units}"


"""Add the two instance methods to the class, regardless of whether we introspect or not."""
setattr(Course, 'init', init)
setattr(Course, 'set_department', set_department)
setattr(Course, '__str__', __str__)
