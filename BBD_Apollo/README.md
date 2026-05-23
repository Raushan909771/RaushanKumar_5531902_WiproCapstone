# Bbd_Project - Behave BDD Automation Framework

This project is created in BDD format using Selenium, Behave, Page Object Model, logging, screenshots, and Allure reporting.

## Folder Structure

```text
Bbd_Project
├── config
│   └── config.ini
├── data
│   ├── login_data.csv
│   └── shop_by_category_data.csv
├── features
│   ├── login.feature
│   ├── shop_by_category.feature
│   ├── environment.py
│   └── steps
│       ├── login_steps.py
│       └── shop_steps.py
├── locators
│   ├── login_locators.py
│   └── shop_locators.py
├── logs
├── pages
│   ├── base_page.py
│   ├── login_page.py
│   ├── signup_page.py
│   └── shop_by_category_page.py
├── reports
│   ├── allure-results
│   └── screenshots
├── utils
│   ├── config_reader.py
│   ├── csv_reader.py
│   ├── logger.py
│   ├── screenshot_util.py
│   └── waits.py
├── behave.ini
├── requirements.txt
└── runtests.py