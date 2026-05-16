from db import *

clear_courses()
courses = get_all_courses()
for course in courses:
    print(course)