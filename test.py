from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login_chaoxing import open_edge_chaoxing
from db import (init_db, clear_courses, insert_courses,
                insert_course, get_all_courses, get_courses_by_weekday,
                search_courses, clear_courses, prepar_course)
import time
import re


'''
def parse_schedule_table(driver):
    # 获取当前教学周
    try:
        week_elem = driver.find_element(By.CSS_SELECTOR, ".selectWeek .week")
        week_text = week_elem.text.strip()
        # 提取数字11
        current_week = int(re.search(r'\d+', week_text).group())
    except Exception:
        current_week = -999

    # 获取表头（星期几和日期）
    head_table = driver.find_element(By.ID, "scheduleHead")
    head_cells = head_table.find_elements(By.CSS_SELECTOR, "th.th")
    week_list = []  # [星期名称, 日期, 星期数字]
    weekday_map = {"周一": 1, "周二": 2, "周三": 3, "周四": 4,
                   "周五": 5, "周六": 6, "周日": 7}
    for th in head_cells:
        weekday_name = th.find_element(By.CLASS_NAME, "week").text.strip()
        weekdate = th.find_element(By.CLASS_NAME, "weekdate").text.strip()
        weekday_num = weekday_map.get(weekday_name, 1)
        week_list.append([weekday_name, weekdate, weekday_num])
    day_count = len(week_list)

    # 获取课体表格
    table = driver.find_element(By.ID, "scheduleTable")
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    # 初始化辅助矩阵，用于处理 rowspan 占位（标记已被上方行占用的列）
    max_periods = 13
    occupied = [[False for _ in range(day_count)] for _ in range(max_periods)]

    # 初始化数据库：清空旧数据（可选），创建表
    init_db()
    clear_courses()

    # ---------- 第一阶段：仅提取课程基本信息，不点击弹窗 ----------
    # 存储每个非空课程的信息，后续再获取教师
    temp_courses = []
    # 注意：需要先获取所有课程div（用于后续点击），但不能在循环中立即点击
    all_course_divs = driver.find_elements(By.CSS_SELECTOR, "#scheduleTable .tddiv.color")
    div_index = 0

    for row_idx, tr in enumerate(rows):
        tds = tr.find_elements(By.TAG_NAME, "td")
        if not tds:
            continue
        try:
            period_text = tds[0].find_element(By.CLASS_NAME, "sIndex").text.strip()
            if not period_text.isdigit():
                continue
            period = int(period_text) - 1
            if period >= max_periods:
                continue
        except:
            continue

        col = 0
        while col < day_count and occupied[period][col]:
            col += 1
        if col >= day_count:
            continue

        for td in tds[1:]:
            while col < day_count and occupied[period][col]:
                col += 1
            if col >= day_count:
                break

            rowspan = int(td.get_attribute("rowspan") or 1)
            # 提取课程名和教室
            course_name = ""
            classroom = ""
            try:
                div = td.find_element(By.CLASS_NAME, "tddiv")
                cname_elem = div.find_element(By.CLASS_NAME, "courseName")
                course_name = cname_elem.text.strip()
                try:
                    loc_elem = div.find_element(By.CLASS_NAME, "courseLoc")
                    classroom = loc_elem.text.strip()
                except:
                    classroom = ""
            except:
                pass

            if course_name:
                weekday_num = week_list[col][2]
                for r in range(rowspan):
                    start_period = period + r + 1
                    end_period = start_period
                    # 暂存，先不插入数据库（因为还没有教师信息）
                    temp_courses.append({
                        "teacher": "",
                        "course_name": course_name,
                        "classroom": classroom,
                        "weekday": weekday_num,
                        "start_period": start_period,
                        "end_period": end_period,
                        "weeks": current_week,
                        "raw_text": f"{course_name} {classroom}".strip(),
                        "div_index": div_index   # 记录对应的课程div索引，用于点击获取教师
                    })
                div_index += 1

            # 标记占用
            for r in range(rowspan):
                r_idx = period + r
                if r_idx < max_periods:
                    occupied[r_idx][col] = True
            col += 1

    # ---------- 第二阶段：逐个点击获取教师信息 ----------
    # 重新获取所有课程div（避免 stale 问题）
    course_divs = driver.find_elements(By.CSS_SELECTOR, "#scheduleTable .tddiv.color")
    main_window = driver.current_window_handle

    for course in temp_courses:
        idx = course["div_index"]
        if idx < len(course_divs):
            div = course_divs[idx]
            try:
                div.click()
                WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
                new_window = [w for w in driver.window_handles if w != main_window][0]
                driver.switch_to.window(new_window)
                # 获取教师信息
                try:
                    teacher_elem = driver.find_element(By.CSS_SELECTOR, ".listItem.gray.teacherName label")
                    teacher = teacher_elem.text.strip()
                    print(teacher)
                except:
                    teacher = ""
                driver.close()
                driver.switch_to.window(main_window)
                course["teacher"] = teacher

            except Exception as e:
                print(f"获取教师信息失败: {e}")
                course["teacher"] = ""

        # 插入数据库
        insert_course(course)
    inserted_count = len(temp_courses)
    print(f"解析完成，共插入 {inserted_count} 条课程记录")
    return inserted_count
'''


def parse_schedule_table(driver):
    # 获取当前教学周
    try:
        week_elem = driver.find_element(By.CSS_SELECTOR, ".selectWeek .week")
        week_text = week_elem.text.strip()
        # 提取数字11
        current_week = int(re.search(r'\d+', week_text).group())
    except Exception:
        current_week = -999

    # 获取表头（星期几和日期）
    head_table = driver.find_element(By.ID, "scheduleHead")
    head_cells = head_table.find_elements(By.CSS_SELECTOR, "th.th")
    week_list = []  # [星期名称, 日期, 星期数字]
    weekday_map = {"周一": 1, "周二": 2, "周三": 3, "周四": 4,
                   "周五": 5, "周六": 6, "周日": 7}
    for th in head_cells:
        weekday_name = th.find_element(By.CLASS_NAME, "week").text.strip()
        weekdate = th.find_element(By.CLASS_NAME, "weekdate").text.strip()
        weekday_num = weekday_map.get(weekday_name, 1)
        week_list.append([weekday_name, weekdate, weekday_num])
    day_count = len(week_list)

    # 获取课体表格
    table = driver.find_element(By.ID, "scheduleTable")
    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
    # 初始化辅助矩阵，用于处理 rowspan 占位（标记已被上方行占用的列）
    max_periods = 13
    occupied = [[False for _ in range(day_count)] for _ in range(max_periods)]

    # 初始化数据库：清空旧数据（可选），创建表
    init_db()
    clear_courses()

    temp_courses = []
    all_course_divs = driver.find_elements(By.CSS_SELECTOR, "#scheduleTable .tddiv.color")
    div_index = 0

    for row_idx, tr in enumerate(rows):
        tds = tr.find_elements(By.TAG_NAME, "td")
        if not tds:
            continue
        try:
            period_text = tds[0].find_element(By.CLASS_NAME, "sIndex").text.strip()
            if not period_text.isdigit():
                continue
            period = int(period_text) - 1
            if period >= max_periods:
                continue
        except:
            continue

        col = 0
        while col < day_count and occupied[period][col]:
            col += 1
        if col >= day_count:
            continue

        for td in tds[1:]:
            while col < day_count and occupied[period][col]:
                col += 1
            if col >= day_count:
                break

            rowspan = int(td.get_attribute("rowspan") or 1)
            # 提取课程名和教室
            course_name = ""
            classroom = ""
            try:
                div = td.find_element(By.CLASS_NAME, "tddiv")
                cname_elem = div.find_element(By.CLASS_NAME, "courseName")
                course_name = cname_elem.text.strip()
                try:
                    loc_elem = div.find_element(By.CLASS_NAME, "courseLoc")
                    classroom = loc_elem.text.strip()
                except:
                    classroom = ""
            except:
                pass

            if course_name:
                weekday_num = week_list[col][2]
                for r in range(rowspan):
                    start_period = period + r + 1
                    end_period = start_period
                    # 不插入数据库（因为还没有教师）
                    temp_courses.append({
                        "teacher": "",
                        "course_name": course_name,
                        "classroom": classroom,
                        "weekday": weekday_num,
                        "start_period": start_period,
                        "end_period": end_period,
                        "weeks": current_week,
                        "raw_text": f"{course_name} {classroom}".strip(),
                        "div_index": div_index   # 记录对应的课程div，用于点击获取教师
                    })
                div_index += 1

            # 标记占用
            for r in range(rowspan):
                r_idx = period + r
                if r_idx < max_periods:
                    occupied[r_idx][col] = True
            col += 1

    teachers = []

    def get_teacher_info(driver):
        main_handle = driver.current_window_handle
        elems = driver.find_elements(By.CSS_SELECTOR, "div[class*='tddiv'][class*='color']")
        elems_count = len(elems)
        for i in range(elems_count):
            driver.switch_to.default_content()
            wait = WebDriverWait(driver, 5)
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "frame_content")))

            cells = driver.find_elements(By.CSS_SELECTOR, "div[class*='tddiv'][class*='color']")
            cell = cells[i]
            if cell.text.strip() == "":
                continue
            orgin_window = driver.window_handles
            # cell.click()
            driver.execute_script("arguments[0].click();", cell)
            WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
            new_windows = driver.window_handles
            new_window = [w for w in new_windows if w != orgin_window[0]]
            driver.switch_to.window(new_window[0])

            teacher_elem = WebDriverWait(driver, 8).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".listItem.gray.teacherName label"))
            )
            teacher = teacher_elem.text.strip()
            print(f"教师: '{teacher}'")

            teachers.append(teacher)
            driver.close()
            driver.switch_to.window(main_handle)

    # 调用函数，获取所有教师信息（顺序与非空课程div顺序一致）
    get_teacher_info(driver)

    # 将获取到的教师信息赋值给 temp_courses 中对应的课程条目
    for course in temp_courses:
        idx = course["div_index"]
        if idx < len(teachers):
            course["teacher"] = teachers[idx]
        else:
            course["teacher"] = ""

    # 插入数据库
    for course in temp_courses:
        insert_course(course)

    inserted_count = len(temp_courses)
    print(f"解析完成，共插入 {inserted_count} 条课程记录")
    return inserted_count




driver = open_edge_chaoxing()
a = parse_schedule_table(driver)
b = get_all_courses()
for course in b:
    print(course)

print("已退出课表")
input("回车退出")
driver.quit()

