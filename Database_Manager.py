'''
Malcolm Roddy
CECS 323 

This class handles all add, delete, selects, and list of objects in the 
database and has some feedback for the user. 
'''
from Department import Department
from Course import Course
from Section import Section

class DatabaseManager:
    # constructor 
    def __init__(self, session):
        self.session = session
    

    ##      ADD FUNCTIONS       ##


    def add_department(self):
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


    def add_course(self):
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


    def add_section(self):
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


    ##      DELETE FUNCTIONS    ##


    def delete_department(self):
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


    def delete_course(self):
      """
      Prompt the user for a course and delete it.
      :param session: The connection to the database.
      :return:        None
      """
      print("deleting a course")
      course = select_course(session)
      number_sections = session.query(Section).filter(Section.courseNumber == course.courseNumber).count()
      if number_sections > 0:
        print(f"Sorry, there are {number_sections} sections associated with that course. Delete them first, "
              "then come back here to delete the department.")
      else:
        session.delete(department)


    ##      LIST FUNCTIONS      ##


    def list_departments(self):
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


    def list_courses(self):
      """
      List all courses currently in the database.
      :param sess:    The connection to the database.
      :return:        None
      """
      # session.query returns an iterator.  The list function converts that iterator
      # into a list of elements.  In this case, they are instances of the Department class.
      courses: [Course] = sess.query(Course).order_by(Course.courseNumber)
      for course in courses:
        print(course)


    def list_department_courses(self):
        """
        List all courses in a specific department.
        :param sess:    The connection to the database.
        :return:        None
        """
        department = select_department(sess)
        dept_courses: [Course] = department.get_courses()
        print("Course for department: " + str(department))
        for dept_course in dept_courses:
            print(dept_course)


    ##      USER INPUT SELECTS      ##


    def select_department(self) -> Department:
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
        return sess.query(Department).filter(Department.abbreviation == abbreviation).first()


    def select_course(self) -> Course:
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


    def select_section(self) -> Section:
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
            section_count = session.query(Section).filter(Section.departmentAbbreviation == course.departmentAbbreviation,
                                                        Section.courseNumber == course.courseNumber, 
                                                        Section.sectionNumber == section_number).count()
            found = section_count == 1
            if not found:
                print("No section by that number for that course. Try again.")

        # otherwise found, return query
        return session.query(Section).filter(Section.departmentAbbreviation == course.departmentAbbreciation,
        Section.courseNumber == course.courseNumber, Section.sectionNumber == section_number).first()



