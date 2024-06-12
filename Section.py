'''
Malcolm Roddy
CECS 323 Section 01
Simple one to many SQLAlchemy
This defines the Section table and its 
relationship to Course along with its constraints
'''
# todo: define 


from orm_base import Base
from db_connection import engine
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy import String, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import Table
from Course import Course #import only course which is parent
from constants import START_OVER, REUSE_NO_INTROSPECTION, INTROSPECT_TABLES


table_name: str = "sections"  # The physical name of this table
# Find out whether the user is introspecting or starting over
introspection_type = IntrospectionFactory().introspection_type
if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
    '''
        If starting from scratch this class creates the table and initializes it
        Or, reuse the tables that are in the schema without using SQLAlchemy to define 
        the class
    '''
    class Section(Base):
        __tablename__ = table_name  # Give SQLAlchemy the name of the table.
        # PRIMARY KEYS
        departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', primary_key=True)
        courseNumber: Mapped[int] = mapped_column('course_number',                                               
                                                            primary_key=True)
        sectionNumber: Mapped[int] = mapped_column('section_number', Integer,
                                                  nullable=False, primary_key=True)
        semester: Mapped[str] = mapped_column('semester', String(10), nullable=False,
                                                            primary_key=True)
        sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False,
                                                            primary_key=True)
        # Rest of columns (Non primary)
        building: Mapped[str] = mapped_column('building', String(6), nullable=False)
        room: Mapped[int] = mapped_column('room', Integer, nullable=False)
        schedule: Mapped[str] = mapped_column('schedule', String(6)) # Not mandatory?
        startTime: Mapped[Time] = mapped_column('start_time', Time) # Not mandatory either?
        instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

        # Define relationships - corrected this shit
        course: Mapped["Course"] = relationship(back_populates="sections")
        # Constraints
        __table_args__ = (
            # Canidate key 1: room cannot be occupied by more than one section at the same time, 
            # Canidate key 2: instructor can't teach two sections at same time
            UniqueConstraint("section_year", "semester", "schedule", "start_time", "building", "room", name="section_uk_01"),
            UniqueConstraint("section_year", "semester", "schedule", "start_time", "instructor", name="section_uk_02"), 
            # Ensure valid input
            CheckConstraint(semester.in_(["Fall", "Spring", "Winter", "Summer I", "Summer II"])),
            CheckConstraint(schedule.in_(["MW", "TuTh", "MWF", "F", "S"])),
            CheckConstraint(building.in_(["VEC", "ECS", "EN2", "EN3", "EN4", "ET", "SSPA"])),
            # Course (Parent) contains two primary keys. Referencing mapped_column and not attribute here
            ForeignKeyConstraint([departmentAbbreviation, courseNumber], [Course.departmentAbbreviation, Course.courseNumber])
        )
        
        # "Constructor" for Section
        def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int,  
         building: str, room: int, schedule: str, startTime: Time, instructor: str ):
            # Helper function, init does actual work
            self.init(course, sectionNumber, semester, sectionYear, building, room, schedule, startTime, instructor)


elif introspection_type == INTROSPECT_TABLES:
    '''
        When choosing option 3, introspect the tables which find tables in the 
        schema and use them to define the class
    '''
    class Section(Base):
        __table__ = Table(table_name, Base.metadata, autoload_with=engine)
        # Otherwise, this property will be named department_abbreviation
        departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
        # This back_populates will not be created by the introspection.
        department: Mapped["Department"] = relationship(back_populates="courses")
        # Otherwise, this property will be named course_number
        courseNumber: Mapped[int] = column_property(__table__.c.course_number)

        def __init__(self, department: Department, courseNumber: int, name: str, description: str, units: int):
            self.init(department, courseNumber, name, description, units)


'''
    Functions below are not subject to options. Init is the constructor
    that is called from the classes that call it from either introspect or 
    not instrospect options. Essnetially a helper function
    Str method is how we get info out from the class
'''
# Accepts a new course without uniqueness constraints
def set_course(self, course: Course):
    self.course = course
    self.courseNumber = course.courseNumber


# initalize the table
def init(self, course: Course, sectionNumber: int, semester: str, sectionYear: int,  
         building: str, room: int, schedule: str, startTime: Time, instructor: str ):
    self.set_course(course)
    self.sectionNumber = sectionNumber
    self.semester = semester
    self.sectionYear = sectionYear
    self.building = building
    self.room = room
    self.schedule = schedule
    self.startTime = startTime
    self.instructor = instructor

# Return variables I guess that are within the class. 
# Im not sure how it knows this if its outside of class/scope
def __str__(self):
    return f"Section number: {self.sectionNumber}"


"""Add the two instance methods to the class, regardless of whether we introspect or not."""
setattr(Course, 'init', init)
setattr(Course, 'set_course', set_course)
setattr(Course, '__str__', __str__)
