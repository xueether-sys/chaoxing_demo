import sqlite3
from pathlib import Path

DB_PATH = Path("data/chaoxing.db")

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    return connection

def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        teacher TEXT,
        classroom TEXT,
        weekday INTEGER NOT NULL,
        start_period INTEGER NOT NULL,
        end_period INTEGER NOT NULL,
        weeks TEXT,
        raw_text TEXT
    );
    """)

    connection.commit()
    cursor.close()

def insert_course(course):
    """
    插入一条课程数据。
    course 是一个字典。
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   INSERT INTO courses (course_name,
                                        teacher,
                                        classroom,
                                        weekday,
                                        start_period,
                                        end_period,
                                        weeks,
                                        raw_text)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                   """, (
                       course.get("course_name"),
                       course.get("teacher"),
                       course.get("classroom"),
                       course.get("weekday"),
                       course.get("start_period"),
                       course.get("end_period"),
                       course.get("weeks"),
                       course.get("raw_text")
                   ))
    connection.commit()
    cursor.close()

def prepar_course(course_name, classroom, weekday, weeks,
                  start_period, end_period, raw_text = "",
                  teacher = ""):
    if(course_name):
        course = {"teacher": teacher,
                  "course_name": course_name,
                  "classroom": classroom,
                  "weekday": weekday,
                  "start_period": start_period,
                  "end_period": end_period,
                  "weeks": weeks,
                  "raw_text": raw_text}
    else:
        course = {"teacher": "无课",
                  "course_name": "无课",
                  "classroom": "无课",
                  "weekday": weekday,
                  "start_period": start_period,
                  "end_period": end_period,
                  "weeks": weeks,
                  "raw_text": raw_text}
    insert_course(course)

def insert_courses(courses):
    '''
    批量处理
    '''
    connection = get_connection()
    cursor = connection.cursor()

    cursor.excute(""""
    INSERT INTO courses (
        course_name,
        teacher,
        classroom,
        weekday,
        start_period,
        end_period,
        weeks,
        raw_text
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (
            i.get("course_name)"),
            i.get("teacher"),
            i.get("classroom"),
            i.get("weekday"),
            i.get("start_period"),
            i.get("end_period"),
            i.get("weeks"),
            i.get("raw_text")
        )
        for i in courses
    ])

    connection.commit()
    cursor.close()

def get_all_courses():
    """
    查询所有课程。
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, course_name, teacher, classroom,
           weekday, start_period, end_period, weeks
    FROM courses
    ORDER BY weekday, start_period
    """)

    rows = cursor.fetchall()

    connection.close()
    return rows

def get_courses_by_weekday(weekday):
    """
    按星期查询课程。
    weekday: 1=周一，2=周二，...，7=周日
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, course_name, teacher, classroom, weekday, start_period, end_period, weeks
    FROM courses
    WHERE weekday = ?
    ORDER BY start_period
    """, (weekday,))

    rows = cursor.fetchall()

    connection.close()
    return rows

def search_courses(keyword):
    """
    按关键词搜索课程名、老师、教室。
    """
    connection = get_connection()
    cursor = connection.cursor()

    like_keyword = f"%{keyword}%"

    cursor.execute("""
    SELECT id, course_name, teacher, classroom, weekday, start_period, end_period, weeks
    FROM courses
    WHERE course_name LIKE ?
       OR teacher LIKE ?
       OR classroom LIKE ?
    ORDER BY weekday, start_period
    """, (like_keyword, like_keyword, like_keyword))

    rows = cursor.fetchall()

    connection.close()
    return rows\

def clear_courses():
    """
    清空 courses 表。
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM courses")

    connection.commit()
    connection.close()


