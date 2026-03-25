from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# --- THÔNG TIN TÀI KHOẢN (Thay bằng acc của bạn để DN001 chạy đúng) ---
USER_LOGIN = "1303" 
PASS_LOGIN = "Guru99"

# Danh sách dữ liệu kiểm thử dựa trên file của bạn
testdata = [
    {"id": "DN001", "user": USER_LOGIN, "pass": PASS_LOGIN, "expected": "Vào trang chủ"},
    {"id": "DN002", "user": "", "pass": "", "expected": "Bỏ trống cả User và Pass"},
    {"id": "DN003", "user": "1303", "pass": "", "expected": "Bỏ trống Password"},
    {"id": "DN004", "user": "", "pass": "Guru99", "expected": "Bỏ trống User-ID"},
    {"id": "DN005", "user": "1303", "pass": "rar", "expected": "Sai mật khẩu"},
    {"id": "DN006", "user": "mng", "pass": "Guru99", "expected": "Sai User-ID"},
]

def runtest():
    # Khởi tạo trình duyệt Chrome
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(5) # Đợi tối đa 5s để tìm các ô nhập liệu

    for data in testdata:
        print(f"\n[+] Đang thực hiện Testcase: {data['id']}")
        driver.get("https://demo.guru99.com/V4/")

        # 1. Tìm các thành phần trên trang
        uid_field = driver.find_element(By.NAME, "uid")
        pw_field = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.NAME, "btnLogin")

        # 2. Nhập dữ liệu từ danh sách testdata
        uid_field.send_keys(data['user'])
        pw_field.send_keys(data['pass'])

        # 3. Bấm nút Login
        login_btn.click()
        
        # Đợi 3 giây để trang web kịp load (Quan trọng để DN001 không bị lỗi)
        time.sleep(3) 
     # --- BƯỚC 4: KIỂM TRA KẾT QUẢ ---
        time.sleep(4)  # Tăng lên 4s cho chắc chắn trang đã load xong
        
        # Lấy URL hiện tại và chuyển hết về chữ thường để so sánh cho dễ
        current_url = driver.current_url.lower()
        print(f"DEBUG: URL hiện tại là -> {current_url}") # Dòng này để bạn tự kiểm tra

        # 1. Kiểm tra xem trong URL có chữ "manager" không (Dấu hiệu vào trang chủ)
        if "manager" in current_url:
            print("Thực tế: Đăng nhập thành công, đã vào trang chủ.")
            
        else:
            try:
                # 2. Nếu không vào trang chủ, check xem có Alert báo lỗi không
                alert = driver.switch_to.alert
                print(f"Thực tế: Xuất hiện Alert -> '{alert.text}'")
                alert.accept()
            except:
                # 3. Nếu không có Alert, tìm lỗi chữ đỏ trên Form
                try:
                    # Lấy text từ các ID thông báo lỗi của Guru99
                    err_u = driver.find_element(By.ID, "message23").text
                    err_p = driver.find_element(By.ID, "message18").text
                    thong_bao = (err_u + " " + err_p).strip()
                    
                    if thong_bao:
                        print(f"Thực tế: Lỗi form -> '{thong_bao}'")
                    else:
                        # Nếu vào đây tức là URL không có 'manager' mà form cũng không có lỗi
                        print("Thực tế: Không xác định được trạng thái (Kiểm tra lại URL hoặc kết nối)")
                except:
                    print("Thực tế: Lỗi hệ thống khi tìm phần tử.")

        time.sleep(1) # Nghỉ 1 giây trước khi sang Case tiếp theo

    driver.quit()
    print("\n>>> Hoàn thành chạy tất cả Testcase.")

if __name__ == "__main__":
    runtest()