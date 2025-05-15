# This file has been replaced by individual test files:
# - test_login_page.py
# - test_login_success.py
# - test_login_failure.py
# - test_registration.py
# - test_track_exercise.py
# - test_view_profile.py
#
# The common setup code has been moved to selenium_base.py
#
# Please use the individual test files instead of this file.
# You can run individual tests using:
#   python -m tests.run_tests login_page
#   python -m tests.run_tests login_success
#   python -m tests.run_tests login_failure
#   python -m tests.run_tests registration
#   python -m tests.run_tests track_exercise
#   python -m tests.run_tests view_profile
#
# Or run all selenium tests using:
#   python -m tests.run_tests selenium
#
# This file is kept for reference only and should not be used.

import unittest
import time
import sys
import os
import random
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from threading import Thread
import socket

# Add parent directory to path to import app package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, ExerciseType
from config import TestingConfig
from werkzeug.security import generate_password_hash

def wait_for_port_to_free(port, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(("localhost", port))
            if result != 0:
                return
        time.sleep(0.5)
    raise RuntimeError(f"Port {port} is still in use after {timeout} seconds")


# Test data
def add_test_data_to_db():
    # Create a test user
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash=generate_password_hash('Password123'),
        height=175.0,
        weight=70.0,
        is_verified=True
    )
    db.session.add(user)
    
    # 添加运动类型数据 - 添加必需的name字段
    exercise_types = [
        ExerciseType(id=1, name='running', display_name='Running'),
        ExerciseType(id=2, name='swimming', display_name='Swimming'),
        ExerciseType(id=3, name='cycling', display_name='Cycling'),
        ExerciseType(id=4, name='weightlifting', display_name='Weightlifting'),
        ExerciseType(id=5, name='yoga', display_name='Yoga'),
        ExerciseType(id=6, name='walking', display_name='Walking'),
        ExerciseType(id=7, name='hiit', display_name='HIIT'),
        ExerciseType(id=8, name='pilates', display_name='Pilates')
    ]
    
    for exercise_type in exercise_types:
        db.session.add(exercise_type)
    
    db.session.commit()


class SeleniumBaseTest(unittest.TestCase):
    
    def setUp(self):
        # 使用固定端口5000
        PORT = 5000
        self.base_url = f"http://localhost:{PORT}/"

        self.testApp = create_app(TestingConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        add_test_data_to_db()

        wait_for_port_to_free(PORT)
        self.server_thread = Thread(target=self.testApp.run, kwargs={"port": PORT, "use_reloader": False})
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Give the server a second to ensure it's up
        time.sleep(1)
        
        # Set up the Chrome WebDriver
        chrome_options = Options()
        # Uncomment for headless testing
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.base_url)
    
    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class TestLoginPage(SeleniumBaseTest):
    
    def test_login_page(self):
        """Test that the login page loads correctly"""
        self.assertIn("Welcome to CalTrack", self.driver.page_source)
        self.assertTrue(self.driver.find_element(By.ID, "email").is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, "password").is_displayed())


class TestLoginSuccess(SeleniumBaseTest):
    
    def test_login_success(self):
        """Test successful login with valid credentials"""
        # Enter login details
        self.driver.find_element(By.ID, "email").send_keys("test@example.com")
        self.driver.find_element(By.ID, "password").send_keys("Password123")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        
        # Wait for redirect to home page
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/home")
        )
        
        # Check we're on the home page
        self.assertIn("Your Calorie Tracking Overview", self.driver.page_source)


class TestLoginFailure(SeleniumBaseTest):
    
    def test_login_failure(self):
        """Test login failure with invalid credentials"""
        # Enter incorrect login details
        self.driver.find_element(By.ID, "email").send_keys("test@example.com")
        self.driver.find_element(By.ID, "password").send_keys("WrongPassword")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        
        # Check we're redirected back to login with error
        WebDriverWait(self.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Invalid email/username or password')]"))
        )
        self.assertIn("Invalid email/username or password", self.driver.page_source)


class TestRegistration(SeleniumBaseTest):
    
    def test_registration(self):
        """Test user registration process"""
        # 确保页面加载完成
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "show-register"))
        )
        
        # 使用JavaScript点击按钮，避免元素被遮挡的问题
        show_register_btn = self.driver.find_element(By.ID, "show-register")
        try:
            show_register_btn.click()
        except Exception as e:
            print(f"Regular click failed: {str(e)}, trying JavaScript click")
            self.driver.execute_script("arguments[0].click();", show_register_btn)

        # 等待注册表单出现
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.ID, "register-form"))
        )

        register_form = self.driver.find_element(By.ID, "register-form")

        # 等待 email 字段可点击，防止动画未结束
        WebDriverWait(register_form, 5).until(
            EC.element_to_be_clickable((By.ID, "email"))
        )

        # 填写基本注册信息
        username_input = register_form.find_element(By.ID, "username")
        email_input = register_form.find_element(By.ID, "email")
        
        username_input.clear()
        email_input.clear()
        
        username_input.send_keys("newuser")
        email_input.send_keys("newuser@example.com")
        
        # 确保验证码按钮可点击
        send_btn = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "send-verification-btn"))
        )

        # 在测试环境中，我们使用固定的验证码
        fixed_code = "123456"
        
        # 发送验证码
        send_btn.click()

        # 等待验证码消息出现
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Verification code has been sent')]"))
            )
            print("Verification code message appeared")
        except Exception as e:
            print(f"Warning: Verification message not found: {str(e)}")
        
        # 等待后端写入验证码
        time.sleep(3)
        
        # 使用固定的验证码 - 不再尝试修改数据库或会话
        code = fixed_code
        print(f"Using verification code: {code}")

        # 填写密码和验证码
        register_form.find_element(By.ID, "reg-password").send_keys("NewPassword123")
        register_form.find_element(By.ID, "reg-confirm-password").send_keys("NewPassword123")
        register_form.find_element(By.ID, "verification_code").send_keys(code)

        # 提交表单 - 使用JavaScript执行点击，避免元素被遮挡的问题
        submit_btn = register_form.find_element(By.XPATH, "//button[contains(text(), 'Create Account')]")
        try:
            # 尝试常规点击
            submit_btn.click()
        except Exception as e:
            print(f"Regular click failed: {str(e)}, trying JavaScript click")
            # 使用JavaScript执行点击
            self.driver.execute_script("arguments[0].click();", submit_btn)

        # 验证成功提示
        # 等待跳转到 /complete-profile 页面
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/complete-profile")
            )
            print("Successfully redirected to complete-profile page")
        except Exception as e:
            print(f"Error waiting for redirect: {str(e)}")
            print("Current URL:", self.driver.current_url)
            print("Page source:", self.driver.page_source[:500])
            raise

        # 再断言页面是否含有期望关键词
        self.assertIn("Complete Your Profile", self.driver.page_source)


class TestTrackExercise(SeleniumBaseTest):
    
    def test_track_exercise(self):
        """Test adding exercise tracking"""
        # 先登录
        self.driver.find_element(By.ID, "email").send_keys("test@example.com")
        self.driver.find_element(By.ID, "password").send_keys("Password123")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()

        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/home")
        )
        
        # 导航到上传页面
        self.driver.get("http://localhost:5000/upload")

        # 等待页面加载并确保下拉菜单可用
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "exercise-type"))
        )
        
        # 等待下拉菜单选项加载完成
        time.sleep(2)
        
        # 现在应该可以直接使用下拉菜单选择选项，因为我们已经在数据库中添加了运动类型
        select = Select(self.driver.find_element(By.ID, "exercise-type"))
        select.select_by_value("1")  # 选择"Running"
        
        # 填入 duration（或 calories）
        self.driver.find_element(By.ID, "duration").send_keys("30")

        # 点击提交按钮
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Add Exercise')]").click()

        # 等待页面刷新或重定向
        time.sleep(2)
        
        # 验证是否成功（检查URL或页面内容）
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "recent-entries"))
        )
        
        # 打印页面源代码以便调试
        print("Page source after exercise submission:", self.driver.page_source[:500])
        
        # 检查是否没有错误消息
        self.assertNotIn("Invalid exercise type", self.driver.page_source)


class TestViewProfile(SeleniumBaseTest):
    
    def test_view_profile(self):
        """Test viewing user profile"""
        # Login first
        # Enter login details
        self.driver.find_element(By.ID, "email").send_keys("test@example.com")
        self.driver.find_element(By.ID, "password").send_keys("Password123")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
        
        # Wait for redirect to home page
        WebDriverWait(self.driver, 5).until(
            EC.url_contains("/home")
        )
        
        # Navigate to profile page
        self.driver.find_element(By.LINK_TEXT, "Profile").click()
        
        # Check profile information is displayed
        WebDriverWait(self.driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Profile')]"))
        )
        self.assertIn("testuser", self.driver.page_source)
        self.assertIn("test@example.com", self.driver.page_source)


# 用于运行单个测试的辅助函数
def run_specific_test(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == "__main__":
    # 如果有命令行参数，运行指定的测试
    if len(sys.argv) > 1:
        test_name = sys.argv[1]
        if test_name == "login_page":
            run_specific_test(TestLoginPage)
        elif test_name == "login_success":
            run_specific_test(TestLoginSuccess)
        elif test_name == "login_failure":
            run_specific_test(TestLoginFailure)
        elif test_name == "registration":
            run_specific_test(TestRegistration)
        elif test_name == "track_exercise":
            run_specific_test(TestTrackExercise)
        elif test_name == "view_profile":
            run_specific_test(TestViewProfile)
        else:
            print(f"未知的测试: {test_name}")
            print("可用的测试: login_page, login_success, login_failure, registration, track_exercise, view_profile")
    else:
        # 否则运行所有测试
        unittest.main()
