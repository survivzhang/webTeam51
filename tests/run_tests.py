"""
CalTrack Test Suite Runner

This script allows you to run different types of tests for the CalTrack application.

Usage:
------
1. Run all tests:
   python -m tests.run_tests

2. Run specific test categories:
   - Unit tests (including calorie tracking tests):
     python -m tests.run_tests unit
   
   - All Selenium tests:
     python -m tests.run_tests selenium

3. Run individual Selenium tests:
   - Login page test:
     python -m tests.run_tests login_page
   
   - Login success test:
     python -m tests.run_tests login_success
   
   - Login failure test:
     python -m tests.run_tests login_failure
   
   - Registration test:
     python -m tests.run_tests registration
   
   - Track exercise test:
     python -m tests.run_tests track_exercise
   
   - View profile test:
     python -m tests.run_tests view_profile
     
   - Sharing functionality test:
     python -m tests.run_tests sharing

Notes:
------
- Unit tests are fast and don't require a browser
- Selenium tests run in Chrome and test the full UI functionality
- Selenium tests use random ports to avoid conflicts when running multiple tests
"""

import unittest
import sys
import os

# Add parent directory to path to import app package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from tests.unitTest import CalTrackUnitTests, CalorieTrackingTests
from tests.seleniumTest import (
    TestLoginPage, 
    TestLoginSuccess, 
    TestLoginFailure, 
    TestRegistration, 
    TestTrackExercise, 
    TestViewProfile,
    TestSharing
)

def run_unit_tests():
    """Run all unit tests including calorie tracking tests"""
    print("\n=== Running Unit Tests ===")
    # Create a test suite with all unit test classes
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CalTrackUnitTests))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(CalorieTrackingTests))
    unittest.TextTestRunner(verbosity=2).run(suite)

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

def run_selenium_sharing_test():
    """Run only the sharing functionality test"""
    print("\n=== Running Sharing Functionality Test ===")
    unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestSharing))

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
        TestViewProfile,
        TestSharing
    ]
    
    # Run each test class individually
    for test_class in test_classes:
        print(f"\n--- Running {test_class.__name__} ---")
        suite = loader.loadTestsFromTestCase(test_class)
        unittest.TextTestRunner(verbosity=2).run(suite)

def run_all_tests():
    """Run all tests"""
    print("\n=== Running All Tests ===")
    
    # Run unit tests (including calorie tracking tests)
    run_unit_tests()
    
    # Run selenium tests one by one
    run_all_selenium_tests()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print(__doc__)
            sys.exit(0)
        elif sys.argv[1] == 'unit':
            run_unit_tests()
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
        elif sys.argv[1] == 'sharing':
            run_selenium_sharing_test()
        else:
            print("Unknown test suite.")
            print("Available options: unit, selenium, login_page, login_success, login_failure, registration, track_exercise, view_profile, sharing")
            print("Use -h or --help for more information.")
    else:
        run_all_tests()