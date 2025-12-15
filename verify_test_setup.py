#!/usr/bin/env python
"""
Verify test setup for dj-paynow
Run this to check if everything is configured correctly
"""
import sys
import os

def check_imports():
    """Check if required packages are installed"""
    print("Checking imports...")
    required = {
        'django': 'Django',
        'rest_framework': 'Django REST Framework',
        'pytest': 'pytest',
        'requests': 'requests',
    }
    
    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            missing.append(name)
    
    return len(missing) == 0

def check_paynow():
    """Check if paynow package is installed"""
    print("\nChecking paynow package...")
    try:
        import paynow
        print(f"  ✓ paynow installed (version {paynow.__version__})")
        return True
    except ImportError:
        print("  ✗ paynow package not found")
        print("    Run: pip install -e .")
        return False

def check_test_dependencies():
    """Check if test dependencies are installed"""
    print("\nChecking test dependencies...")
    test_deps = {
        'pytest': 'pytest',
        'pytest_django': 'pytest-django',
        'pytest_cov': 'pytest-cov (optional)',
    }
    
    for module, name in test_deps.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")

def check_django_setup():
    """Check if Django can be configured"""
    print("\nChecking Django configuration...")
    try:
        from django.conf import settings
        from django.core.management import call_command
        import django
        
        # Configure Django
        if not settings.configured:
            settings.configure(
                DEBUG=True,
                SECRET_KEY='test-key',
                DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                        'NAME': ':memory:',
                    }
                },
                INSTALLED_APPS=[
                    'django.contrib.contenttypes',
                    'django.contrib.auth',
                    'paynow',
                ],
            )
            django.setup()
        
        print("  ✓ Django configured")
        
        # Try to run migrations
        call_command('migrate', '--run-syncdb', verbosity=0, interactive=False)
        print("  ✓ Migrations successful")
        
        return True
    except Exception as e:
        print(f"  ✗ Django setup failed: {e}")
        return False

def check_test_files():
    """Check if test files exist"""
    print("\nChecking test files...")
    test_files = [
        'conftest.py',
        'test_models.py',
        'test_views.py',
        'test_api.py',
        'test_utils.py',
        'test_client.py',
        'test_signals.py',
    ]
    
    tests_dir = 'tests'
    if not os.path.exists(tests_dir):
        print(f"  ✗ {tests_dir}/ directory not found")
        return False
    
    missing = []
    for filename in test_files:
        filepath = os.path.join(tests_dir, filename)
        if os.path.exists(filepath):
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} - NOT FOUND")
            missing.append(filename)
    
    return len(missing) == 0

def run_sample_test():
    """Try to run a simple test"""
    print("\nRunning sample test...")
    try:
        import subprocess
        result = subprocess.run(
            ['pytest', 'tests/test_utils.py::UtilsTest::test_generate_payment_id_default', '-v'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("  ✓ Sample test passed")
            return True
        else:
            print("  ✗ Sample test failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("  ✗ Test timed out")
        return False
    except Exception as e:
        print(f"  ✗ Could not run test: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("dj-paynow Test Setup Verification")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", check_imports()))
    results.append(("PayNow Package", check_paynow()))
    results.append(("Test Dependencies", check_test_dependencies()))
    results.append(("Django Setup", check_django_setup()))
    results.append(("Test Files", check_test_files()))
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\n" + "=" * 60)
        print("✓ All checks passed! You can now run tests:")
        print("  pytest")
        print("  pytest --cov=paynow")
        print("  ./run_tests.sh")
        print("=" * 60)
        return 0
    else:
        print("\n" + "=" * 60)
        print("✗ Some checks failed. Please fix the issues above.")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())