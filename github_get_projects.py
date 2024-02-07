import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException

chrome_options  = Options()
driver          = webdriver.Chrome(options=chrome_options)
USERNAME        = 'YOUR_USERNAME'
PASSWORD        = 'YOUR_PASSWORD'
URL             = 'https://github.com/login'
URL_REPOS       = f"https://github.com/{USERNAME}?tab=repositories"
file_path       = './README.md'

def login():
    driver.get(URL)
    username_field = driver.find_element(By.ID, 'login_field')
    username_field.send_keys(USERNAME)

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(PASSWORD)

    password_field.send_keys(Keys.RETURN)
    time.sleep(30)

def get_repositories():
    driver.get(URL_REPOS)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[data-filterable-for="your-repos-filter"]')))

    repos           = driver.find_elements(By.CSS_SELECTOR, 'ul[data-filterable-for="your-repos-filter"] li[itemprop="owns"]')
    repositories    = []

    for repo in repos:
        name_element                = repo.find_element(By.CSS_SELECTOR, 'a[itemprop="name codeRepository"]')
        name                        = name_element.text
        repo_url                    = name_element.get_attribute('href')

        try:
            description_element     = repo.find_element(By.CSS_SELECTOR, 'p[itemprop="description"]')
            description             = description_element.text
        except:
            description = "No description"

        try:
            language_element        = repo.find_element(By.CSS_SELECTOR, 'span[itemprop="programmingLanguage"]')
            language                = language_element.text
        except:
            language = "Not specified"

        try:
            update_element          = repo.find_element(By.CSS_SELECTOR, 'relative-time')
            iso_datetime_str        = update_element.get_attribute('datetime')
            datetime_obj            = datetime.strptime(iso_datetime_str, '%Y-%m-%dT%H:%M:%SZ')
            last_updated_formatted  = datetime_obj.strftime('%d/%m/%Y %H:%M')
        except:
            last_updated_formatted  = "Not available"
        
        repositories.append({
            'name'          : name,
            'description'   : description,
            'language'      : language,
            'url'           : repo_url,
            'last_updated'  : last_updated_formatted
        })

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"# {USERNAME} Github repositories.\n")
        file.write(f'<a href="https://github.com/{USERNAME}?tab=repositories">https://github.com/{USERNAME}?tab=repositories</a> \n')

        for i, repo in enumerate(repositories, start=1):
            file.write(f"## _{i}. Nombre repositorio: {repo['name']}._ \n")
            file.write(f"Descripción: {repo['description']}.\n")
            file.write(f"Lenguaje: {repo['language']}.\n")
            file.write(f'Url: <a href="{repo['url']}"> {repo['url']} </a> \n')
            file.write(f"Última actualización: {repo['last_updated']}.\n\n")

    driver.quit()

login()
get_repositories()


