from sqlalchemy import UniqueConstraint
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List  # Use this for the list of courses offered by the department

"""This is the guts of the department class that needs to be defined
regardless whether we introspect or not."""
__tablename__ = "departments"  # Give SQLAlchemy th name of the table.
abbreviation: Mapped[str] = mapped_column('abbreviation', String,
                                          nullable=False, primary_key=True)
courses: Mapped[List["Course"]] = relationship(back_populates="department")
name: Mapped[str] = mapped_column('name', String(50), nullable=False)
# __table_args__ can best be viewed as directives that we ask SQLAlchemy to
# send to the database.  In this case, that we want two separate uniqueness
# constraints (candidate keys).
__table_args__ = (UniqueConstraint("name", name="departments_uk_01"),)


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

def select_department(sess) -> Department:
    """
    Prompt the user for a specific department by the department abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = sess.query(Department). \
            filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    return_student: Department = sess.query(Department). \
        filter(Department.abbreviation == abbreviation).first()
    return return_student


def list_departments(session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)

def add_course(self, course):
    if course not in self.courses:
        self.courses.add(course)  # I believe this will update the course as well.


def remove_course(self, course):
    if course in self.courses:
        self.courses.remove(course)


def get_courses(self):
    return self.courses


def __str__(self):
    return f"Department abbreviation: {self.abbreviation} name: {self.name} number course offered: {len(self.courses)}"
