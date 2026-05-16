from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def open_edge_chaoxing():
    # 打开网页链接
    driver = webdriver.Edge()
    driver.get("https://i.chaoxing.com")

    # 账号登录
    username = driver.find_element(By.ID, "phone")
    username.send_keys("我是账号")
    password = driver.find_element(By.ID, "pwd")
    password.send_keys("我是密码")

    # 方式二选一
    password.send_keys(Keys.ENTER)
    # login_btn = driver.find_element(By.CLASS_NAME, "btns-box")
    # login_btn.click()

    # 显式等待并进入课表
    wait = WebDriverWait(driver, 5)
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "frame_content")))

    print("已进入课表")
    return driver

