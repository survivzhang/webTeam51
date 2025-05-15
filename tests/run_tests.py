import unittest
import sys
import os

# Add parent directory to path to import app package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from tests.unitTest import CalTrackUnitTests
from tests.test_calorie_tracking import CalorieTrackingTests
from tests.seleniumTest import (
    TestLoginPage, 
    TestLoginSuccess, 
    TestLoginFailure, 
    TestRegistration, 
    TestTrackExercise, 
    TestViewProfile
)

def run_unit_tests():
    """Run only unit tests"""
    print("\n=== Running Unit Tests ===")
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CalTrackUnitTests))

def run_calorie_tracking_tests():
    """Run only calorie tracking tests"""
    print("\n=== Running Calorie Tracking Tests ===")
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CalorieTrackingTests))

def run_selenium_login_page_test():
    """Run only the login page test"""
    print("\n=== Running Login Page Test ===")
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestLoginPage))

def run_selenium_login_success_test():
    """Run only the login success test"""
    print("\n=== Running Login Success Test ===")
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestLoginSuccess))

def run_selenium_login_failure_test():
    """Run only the login failure test"""
    print("\n=== Running Login Failure Test ===")
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestLoginFailure))

def run_selenium_registration_test():
    """Run only the registration test"""
    print("\n=== Running Registration Test ===")
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestRegistration))

def run_selenium_track_exercise_test():
    """Run only the track exercise test"""
    print("\n=== Running Track Exercise Test ===")
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestTrackExercise))

def run_selenium_view_profile_test():
    """Run only the view profile test"""
    print("\n=== Running View Profile Test ===")
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestViewProfile))

def run_all_selenium_tests():
    """Run all Selenium tests"""
    print("\n=== Running All Selenium Tests ===")
    # Use TestLoader to discover and run tests sequentially
    # This avoids port conflicts by running one test class at a time
    loader = unittest.TestLoader()
    
    # Create a list of test classes to run
    test_classes = [
        TestLoginPage,
        TestLoginSuccess,
        TestLoginFailure,
        TestRegistration,
        TestTrackExercise,
        TestViewProfile
    ]
    
    # Run each test class individually
    for test_class in test_classes:
        print(f"\n--- Running {test_class.__name__} ---")
        suite = loader.loadTestsFromTestCase(test_class)
        unittest.TextTestRunner(verbosity=2).run(suite)

def run_all_tests():
    """Run all tests"""
    print("\n=== Running All Tests ===")
    
    # Run unit tests
    print("\n--- Running Unit Tests ---")
    unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(CalTrackUnitTests)
    )
    
    # Run calorie tracking tests
    print("\n--- Running Calorie Tracking Tests ---")
    unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(CalorieTrackingTests)
    )
    
    # Run selenium tests one by one
    run_all_selenium_tests()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == 'unit':
            run_unit_tests()
        elif sys.argv[1] == 'calorie':
            run_calorie_tracking_tests()
        elif sys.argv[1] == 'selenium':
            run_all_selenium_tests()
        elif sys.argv[1] == 'login_page':
            run_selenium_login_page_test()
        elif sys.argv[1] == 'login_success':
            run_selenium_login_success_test()
        elif sys.argv[1] == 'login_failure':
            run_selenium_login_failure_test()
        elif sys.argv[1] == 'registration':
            run_selenium_registration_test()
        elif sys.argv[1] == 'track_exercise':
            run_selenium_track_exercise_test()
        elif sys.argv[1] == 'view_profile':
            run_selenium_view_profile_test()
        else:
            print("Unknown test suite. Available options: unit, calorie, selenium, login_page, login_success, login_failure, registration, track_exercise, view_profile")
    else:
        run_all_tests() 