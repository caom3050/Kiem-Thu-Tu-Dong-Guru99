from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Danh sách dữ liệu kiểm thử dựa trên file của bạn
testdata = [
    {"id": "DN001", "user": "1303", "pass": "Guru99", "expected": "Vào trang chủ"},
    {"id": "DN002", "user": "", "pass": "", "expected": "User-ID must not be blank, Password must not be blank"},
    {"id": "DN003", "user": "1303", "pass": "", "expected": "Password must not be blank"},
    {"id": "DN004", "user": "", "pass": "Guru99", "expected": "User-ID must not be blank"},
    {"id": "DN005", "user": "1303", "pass": "rar", "expected": "User or Password is not valid"},
    {"id": "DN006", "user": "mng", "pass": "Guru99", "expected": "User or Password is not valid"},
]

def runtest():
    # Khởi tạo trình duyệt (Chrome)
    driver = webdriver.Chrome()
    
    
    for data in testdata:
        print(f" Đang thực hiện Testcase: {data['id']}")
        driver.get("https://demo.guru99.com/V4/")
        
        # Tìm các element
        uid_field = driver.find_element(By.NAME, "uid")
        pw_field = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.NAME, "btnLogin")

        # Nhập dữ liệu
        uid_field.send_keys(data['user'])
        pw_field.send_keys(data['pass'])
        
        # Kịch bản yêu cầu bấm login
        login_btn.click()
        
        try:
            # 1. Kiểm tra nếu có Alert (Thông báo lỗi sai user/pass - DN005, DN006)
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert_text = alert.text
            print(f"Thực tế: Alert hiện ra - '{alert_text}'")
            time.sleep(5)
            
        except:
            # 2. Kiểm tra nếu có thông báo validation ngay dưới ô nhập (DN002, DN003, DN004)
            # Hoặc kiểm tra nếu đã đăng nhập thành công (DN001)
            if "manager/Managerhomepage" in driver.current_url:
                print("Thực tế: Đăng nhập thành công, đã vào trang chủ.")
            else:
                # Tìm các thông báo lỗi hiển thị trên form (label)
                labels = driver.find_elements(By.TAG_NAME, "label")
                errors = [label.text for label in labels if label.text != ""]
                print(f"Thực tế: Lỗi form - {', '.join(errors)}")

        
        
        time.sleep(7) # Nghỉ 1 chút giữa các testcase


    driver.quit()

if __name__ == "__main__":
    runtest()