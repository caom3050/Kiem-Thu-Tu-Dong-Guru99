from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
import time

URL = "https://demo.guru99.com/V4/index.php"
USER = "1303"
PASS = "Guru99"

driver = webdriver.Chrome()
driver.implicitly_wait(5)

def login(user, password):
    driver.get(URL)
    driver.find_element(By.NAME, "uid").send_keys(user)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "btnLogin").click()
    time.sleep(5)

def check_alert(msg):
    try:
        alert = driver.switch_to.alert
        print(msg)
        alert.accept()
        return True
    except NoAlertPresentException:
        return False

try:
    # ===== TEST 1: Truy cập thẳng Admin =====
    print("\n[BM001] Truy cập thẳng Admin")
    driver.get("https://demo.guru99.com/V4/manager/Managerhomepage.php")
    if "Managerhomepage" in driver.current_url:
        print("Không login vẫn vào được Admin")
    else:
        print("Không truy cập được")

    # ===== TEST 2: XSS =====
    print("\n[BM002] Test XSS")
    login("<script>alert('XSS')</script>", "123")
    if not check_alert("PHÁT HIỆN XSS"):
        if "Managerhomepage" in driver.current_url:
            print("XSS không thành công nhưng đã login được")
        else:
            print("XSS không hoạt động")

    # ===== TEST 3: SQL Injection =====
    print("\n[BM003] Test SQL Injection")
    driver.get("https://demo.guru99.com/V4/index.php")
    
    login("' OR '1'='1", "123456")
    
    if "Managerhomepage" in driver.current_url:
        print("Bypass SQL Injection thành công")
    else:
        if "sql" in driver.page_source.lower() or "mysql" in driver.page_source.lower():
            print("lỗi SQL")
        else:
            print("SQL Injection KHÔNG thành công")

    # ===== TEST 4: Logout + Back =====
    print("\n[BM004] Test Logout + Back")
    login(USER, PASS)
    driver.find_element(By.LINK_TEXT, "Log out").click()
    
    check_alert("Đã logout")
    driver.back()
    time.sleep(2)
    
    if "Managerhomepage" in driver.current_url:
        print("Vẫn vào được sau logout")
    else:
        print("Không vào được sau logout")

finally:
    driver.quit()