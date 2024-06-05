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

def get_commit_count(repo_url):
    driver.get(repo_url)
    wait = WebDriverWait(driver, 20)  # Aumenta el tiempo de espera
    try:
        # Espera a que el elemento de commits esté visible y obtén su texto
        commits_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.Text-sc-17v1xeu-0.gPDEWA.fgColor-default')))
        commit_text = commits_element.text
        print(commit_text)
        return commit_text
    except TimeoutException:
        return "N/A"

def get_repositories():
    driver.get(URL_REPOS)
    wait = WebDriverWait(driver, 20)
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
        
        commit_counter              = get_commit_count(repo_url)
        
        repositories.append({
            'name'              : name,
            'description'       : description,
            'language'          : language,
            'url'               : repo_url,
            'commit_counter'    : commit_counter,
            'last_updated'      : last_updated_formatted
        })
        driver.get(URL_REPOS)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ul[data-filterable-for="your-repos-filter"]')))
        time.sleep(1)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"# {USERNAME} Github repositories.\n")
        file.write(f'<a href="https://github.com/{USERNAME}?tab=repositories">https://github.com/{USERNAME}?tab=repositories</a> \n')

        for i, repo in enumerate(repositories, start=1):
            file.write(f"## _{i}. {repo['name']}._ \n")
            file.write(f"| Language             | Description                                                    | Last update          | Commits | \n")
            file.write(f"| :------------------- | :------------------------------------------------------------- | :---------------------------- | :------ | \n")
            file.write(f"| `{repo['language']}` | {repo['description']}                                          | `{repo['last_updated']}`      | `{repo['commit_counter']}` |\n\n")
            file.write(f'<a href="{repo['url']}"> {repo['url']} </a> \n')

    driver.quit()

login()
get_repositories()


