'''
Malcolm Roddy
CECS 323 

This class handles all add, delete, and list of objects in the 
database and has some feedback for the user. 
'''


class DatabaseManager:
    # constructor 
    def __init__(self, session):
        self.session = session

  
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
