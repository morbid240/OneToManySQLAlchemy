from Section import Section
from Course import Course
from Course_Query import select_course
def add_section(session):
    """
    Prompt the user for the information for a new section and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_room = False
    print("Adding a new section")
    course = select_course(session)
    section_year = int(input("Section Year --> "))
    semester = input("Semester --> ")
    schedule = input("Schedule --> ")
    start_time = Time(input("Start Time (HH:MM:SS) --> "))
    while not unique_room or not unique_instructor:
        building = input("Building --> ")
        room = int(input("Room --> "))
        room_count = session.query(Section).filter(Section.departmentAbbreviation == course.departmentAbbreviation,
                                      Section.courseNumber == course.courseNumber, Section.sectionYear==section_year,
                                      Section.semester == semester, Section.start_time == start_time,
                                      Section.building == building, Section.room == room).count()
        unique_room = room_count == 0
        if not unique_room:
          print("There is already a section using that room at that time. Try again.")
        else:
          instructor = input("Instructor --> ")
          instructor_count = session.query(Section).filter(Section.departmentAbbreviation == course.departmentAbbreviation,
                                      Section.courseNumber == course.courseNumber, Section.sectionYear==section_year,
                                      Section.semester == semester, Section.start_time == start_time,
                                      Section.instructor == instructor).count()
          unique_instructor = instructor_count == 0
          if not unique_instructor:
            print("There is already an instructor teaching at that time. Try again.")
          section_number = int(input("Section Number --> "))
    # Otherwise we all good with values
    new_section = Section(department.abbreviation, course.courseNumber, section_number,
                          semester, section_year, building, room,
                          schedule, start_time, instructor)
    session.add(new_section)

def delete_section(session):
    """
    Prompt the user to select a section by its attributes, then delete it.
    :param session: The connection to the database.
    :return: None
    """
    print("Deleting a section")
    section = select_section(session)
    session.delete(section)


def select_section(sess):
    """
    Select a section by its attributes.
    :param sess: The connection to the database.
    :return: The selected section.
    """
    found = False
    while not found:
        department_abbreviation = input("Department Abbreviation --> ")
        course_number = int(input("Course Number --> "))
        section_number = int(input("Section Number --> "))
        semester = input("Semester --> ")
        section_year = int(input("Section Year --> "))

        count = sess.query(Section).filter(Section.departmentAbbreviation == department_abbreviation,
                   Section.courseNumber == course_number,
                   Section.sectionNumber == section_number,
                   Section.semester == semester,
                   Section.sectionYear == section_year).count()
        found = count == 1
        if not found:
          print("No section found with that information. Please try again.")
    # Otherwise its been found
    return sess.query(Section).filter(Section.departmentAbbreviation == department_abbreviation,
            Section.courseNumber == course_number, Section.sectionNumber == section_number,
           Section.semester == semester, Section.sectionYear == section_year).first()

