from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from typing import List  # Use this for the list of courses offered by the department
from sqlalchemy import String, Integer
"""This is the guts of the Course class that needs to be defined
regardless whether we introspect or not."""


# Table name
__tablename__ = "courses"  

# Primary keys
departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', primary_key=True)
courseNumber: Mapped[int] = mapped_column('course_number', Integer, nullable=False, primary_key=True)
name: Mapped[str] = mapped_column('name', String(50), nullable=False)

# Other attributes
description: Mapped[str] = mapped_column('description', String(500), nullable=False)
units: Mapped[int] = mapped_column('units', Integer, nullable=False)

# Relationship to department(parent)
sections: Mapped[List["Section"]] = relationship(back_populates="course")

# Constraints 
__table_args__ =(
    UniqueConstraint("department_abbreviation", "name", name="courses_uk_01"),
    ForeignKeyConstraint([departmentAbbreviation],
    [Department.abbreviation])
)


def __str__(self):
    return f"Department abbreviation: {self.abbreviation} name: {self.name} number course offered: {len(self.courses)}"
