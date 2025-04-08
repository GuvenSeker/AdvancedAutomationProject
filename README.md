# Web Automation Test Project

This is a simple test framework developed for automated testing of websites. It is built using Python and Selenium.

## Project Purpose

With this project, you can:
- Test if websites work correctly in different browsers (Chrome, Firefox)
- Automatically capture screenshots when tests fail
- View detailed test results

## Installation

1. Make sure you have Python installed on your computer (Python 3.9 or higher)

2. Download the project to your computer:
```bash
git clone https://github.com/yourusername/web-automation-framework.git
cd web-automation-framework
```

3. Install required programs:
```bash
pip install -r requirements.txt
```

## Project Structure

The project consists of these files:
- `pages/`: Files containing page operations
- `tests/`: Test files
- `screenshots/`: Screenshots of failed tests
- `requirements.txt`: List of required programs

## Running Tests

To run all tests:
```bash
python -m unittest tests.test_web_automation.WebTestFramework.execute_all_browsers()
```

To run a specific test:
```bash
python -m unittest tests.test_check_advanced_automation_path.CareerPortalAutomation
```

## Test Results

- If a test fails, a screenshot is automatically saved in the `screenshots/` folder
- Test results are displayed in the console
