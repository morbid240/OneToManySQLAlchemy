import logging
# My option lists for
from menu_definitions import menu_main, debug_select
from IntrospectionFactory import IntrospectionFactory
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Section import Section
from Option import Option
from Menu import Menu
# Poor man's enumeration of the two available modes for creating the tables
from constants import START_OVER, INTROSPECT_TABLES, REUSE_NO_INTROSPECTION
from sqlalchemy import inspect  # map from column name to attribute name


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


def add_course(session):
    """
    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(sess)
    unique_number: bool = False
    unique_name: bool = False
    number: int = -1
    name: str = ''
    while not unique_number or not unique_name:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        name_count: int = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation,
                                                       Course.name == name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            number_count = session.query(Course). \
                filter(Course.departmentAbbreviation == department.abbreviation,
                       Course.courseNumber == number).count()
            unique_number = number_count == 0
            if not unique_number:
                print("We already have a course in this department with that number.  Try again.")
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    course = Course(department, number, name, description, units)
    session.add(course)

def add_section(session):
    """
    Prompt user for adding a new section. Checks input for Uniqueness contraints
    of {year, semester, schedule, start_time, building, room}
    and {year, semester, scheudle, strt_time, instructor}
    """
    print("Which course are you adding this section?")
    course: Course = select_course(session)
    unique_room: bool = False
    unique_instructor: bool = False

    section_year: int = -1
    semester: str = ''
    schedule: str = ''
    start_time: Time = "2:00:00"

    # When is the section
    semester = input("Section semester-->")
    section_year = input("Section year-->")
    schedule = input("Section schedule-->")
    start_time = input("Section start time as HH:MM::SS-->")
    # Check uniqueness constraints, match to when 
    while not unique_room or not unique_instructor:
        building = input("Building-->")
        room = int(input("Room-->"))
        room_count: int = session.query(Section).filter(Section.semester == semester, Section.sectionYear == section_year, 
                                                        Section.schedule == schedule, Section.startTime == start_time,
                                                        Section.building == building, Section.room==room).count()
        unique_room = room_count == 0
        if not unique_room:
            print("We already have a section in that room, try again.")
        if unique_room:
            instructor = input("Instructor-->")
            instructor_count = session.query(Section).filter(Section.semester == semester, Section.sectionYear == section_year, 
                                                        Section.schedule == schedule, Section.startTime == start_time,
                                                        Section.instructor == instructor).count()
            unique_instructor = instructor_count == 0
            if not unique_instructor:
                print("That instructor is already teaching another section at that time. Try again.")
            if unique_instructor:
                section_number = input("Section number with leading 0-->")

    section = Section(course, section_number, semester, section_year, building, room, schedule, start_time, instructor)
    session.add(section)



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
    # return queried department
    return sess.query(Department).filter(Department.abbreviation == abbreviation).first()


def select_course(session) -> Course:
    '''
    Selects a course based on department and course number
    Uses select_department
    :param sess:    The connection to the database.
    :return:        The selected course.
    '''
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department = select_department(session)
        course_number = int(input("Course Number--> "))
        name_count: int = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation,
                                                    Course.courseNumber == course_number).count()
        found = name_count == 1
        if not found:
            print("No course by that number in that department.  Try again.")
    # return query with selected values
    return session.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                       Course.courseNumber == course_number).first()


def select_section(session) -> Section:
    '''
    Selects a section by combo of department abbreviation, 
    course number, and section number
    :param sess:    The connection to the database.
    :return:        The selected section.
    '''
    found: bool = False
    sectionNumber: int =-1
    while not found:
        course = select_course(session)
        section_number = input("Section number-->")
        section_count = session.query(Section).filter(Section.departmentAbbreviation == course.departmentAbbreciation,
                                                      Section.courseNumber == course.courseNumber, 
                                                      Section.sectionNumber = section_number).count()
        found = section_count == 1
        if not found:
            print("No section by that number for that course. Try again.")

    # otherwise found, return query
    return session.query(Section).filter(Section.departmentAbbreviation == course.departmentAbbreciation,
    Section.courseNumber == course.courseNumber, Section.sectionNumber == section_number).first()
        
        

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

def delete_course(session):
    """
    Prompt the user for a course and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a course")
    course = select_course(session)
    number_sections = session.query(Section).filter(Section.courseNumber == course.courseNumber).count()
    if number_sections > 0 
        print(f"Sorry, there are {number_sections} sections associated with that course. Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)
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


def list_courses(sess):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = sess.query(Course).order_by(Course.courseNumber)
    for course in courses:
        print(course)


def list_department_courses(sess):
    department = select_department(sess)
    dept_courses: [Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)


if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    # Prompt the user for whether they want to introspect the tables or create all over again.
    introspection_mode: int = IntrospectionFactory().introspection_type
    if introspection_mode == START_OVER:
        print("starting over")
        # create the SQLAlchemy structure that contains all the metadata, regardless of the introspection choice.
        metadata.drop_all(bind=engine)  # start with a clean slate while in development

        # Create whatever tables are called for by our "Entity" classes that we have imported.
        metadata.create_all(bind=engine)
    elif introspection_mode == INTROSPECT_TABLES:
        print("reusing tables")
        # The reflection is done in the imported files that declare the entity classes, so there is no
        # reflection needed at this point, those classes are loaded and ready to go.
    elif introspection_mode == REUSE_NO_INTROSPECTION:
        print("Assuming tables match class definitions")

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
