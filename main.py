import contextlib
import sqlite3
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = webdriver.ChromeOptions()
linkedin_chrome_webdriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

db = sqlite3.connect('sqlite.db')
cur = db.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS python_data (number INTEGER PRIMARY KEY AUTOINCREMENT, position TEXT (200) , company_name TEXT (200), location TEXT (200), benefits TEXT (200))")

# maximize window
linkedin_chrome_webdriver.maximize_window()
url = 'https://in.linkedin.com/jobs/search?keywords=Python%20Developer&location=Ahmedabad%2C%20Gujarat%2C%20India&geoId=104990346&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

linkedin_chrome_webdriver.get(url)

my_scroll_height = linkedin_chrome_webdriver.execute_script('return document.body.scrollHeight;')

scroll_times = 1
previous_scroll_height = None
while previous_scroll_height != my_scroll_height:
    previous_scroll_height = my_scroll_height
    linkedin_chrome_webdriver.execute_script(f'window.scrollTo(0, {my_scroll_height});')
    time.sleep(3)
    scroll_times += 1
    next_scroll_height = linkedin_chrome_webdriver.execute_script('return document.body.scrollHeight;')
    my_scroll_height = next_scroll_height  # print(scroll_times, next_scroll_height, "scroll height")
try:
    jobs = linkedin_chrome_webdriver.find_elements(By.XPATH, ".//div[@class='base-search-card__info']")
except Exception as e:
    print(f"Error :{e}")

count_jobs = linkedin_chrome_webdriver.execute_script(
    "return document.querySelectorAll('.base-search-card__info').length;")

while previous_scroll_height == my_scroll_height:
    with contextlib.suppress(NoSuchElementException):
        search_completed = linkedin_chrome_webdriver.find_element(By.CLASS_NAME,
                                                                  'px-1\.5.flex.inline-notification.text-color-signal-positive.see-more-jobs__viewed-all')  # print(search_completed, "searchhhhhhhhhhhh", type(search_completed.is_displayed()))

    if search_completed.is_displayed():
        break
    try:
        # button will be visible if page is scrolled to its limit and can be scrolled further
        see_more_jobs_button = linkedin_chrome_webdriver.find_element(By.CLASS_NAME,
                                                                      'infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible')
        see_more_jobs_button.click()
        time.sleep(3)
        new_scroll_height_after_click = linkedin_chrome_webdriver.execute_script('return document.body.scrollHeight;')
        linkedin_chrome_webdriver.execute_script(f'window.scrollTo(0, {new_scroll_height_after_click});')
        previous_scroll_height = my_scroll_height = new_scroll_height_after_click

    except NoSuchElementException as no_such_element:
        print("except.......................................")
        print(f"Exception : {no_such_element}. May be you have completed scrolling.")

expected_conditions.visibility_of_element_located(
    (By.CLASS_NAME, 'infinite-scroller__show-more-button infinite-scroller__show-more-button--visible'))

count_jobs = linkedin_chrome_webdriver.execute_script(
    "return document.querySelectorAll('.base-search-card__info').length;")
print("The job count is", count_jobs)


def inner(parent, strategy, locator, default='None'):
    get_company = None
    with contextlib.suppress(NoSuchElementException):
        get_company = parent.find_element(strategy, locator).text
    return get_company or default


try:
    jobs = linkedin_chrome_webdriver.find_elements(By.XPATH, ".//div[@class='base-search-card__info']")
    for job in jobs:
        try:
            position = job.find_element(By.XPATH, ".//h3[@class='base-search-card__title']")
            position_text = position.text
            company = inner(job, By.XPATH, ".//a[@class='hidden-nested-link']")
            company_text = company
            location = job.find_element(By.XPATH, ".//span[@class='job-search-card__location']")
            location_text = location.text
            benefits_text = inner(job, By.XPATH, ".//span[@class='result-benefits__text']")
            time_ = job.find_element(By.XPATH, ".//time[starts-with(@class, 'job-search-card__listdate')]")
            time_text = time_.text
            cur.execute(
                "INSERT INTO python_data (position, company_name, location, benefits) VALUES (?, ?, ?, ?)",
                (position_text, company_text, location_text, benefits_text))
            db.commit()
        except Exception as e:
            print(f"Error :{e}")
            print("error in operation")
            db.rollback()
    db.close()
except Exception as e:
    print(f"Error :{e}")
