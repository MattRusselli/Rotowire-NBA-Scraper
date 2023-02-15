from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv

load_dotenv()

def get_nba_lineups():

    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    driver = webdriver.Chrome()

    # Login
    driver.get('https://www.rotowire.com/users/login.php')

    driver.find_element(By.NAME, 'username').send_keys(username)

    driver.find_element(By.NAME, 'password').send_keys(password)

    button = driver.find_element(
        By.XPATH, "//button[@type='submit']")

    button.click()

    # Navigate to NBA Lineups
    driver.get('https://www.rotowire.com/basketball/nba-lineups.php')

    # Scrape all projected minutes for all players
    button_element = driver.find_elements(By.CLASS_NAME, "see-proj-minutes")

    result = {}

    for buttons in button_element:

        buttons.click()

        time.sleep(0.5)

        team = driver.find_element(
            By.CLASS_NAME, 'lineups-viz')

        teamName = team.find_element(By.TAG_NAME, 'img').get_attribute('alt')

        players = driver.find_elements(By.CLASS_NAME, 'lineups-viz__player')

        a = []

        for player in players:

            name = player.find_element(By.TAG_NAME, 'a')

            projMin = player.find_element(
                By.CLASS_NAME, "minutes-meter__proj")

            projMin = int(projMin.text.split(' ')[0])

            a.append([name.text, projMin])

            result[teamName] = a

        close_button = driver.find_element(
            By.CLASS_NAME, "lineups-viz__close")

        close_button.click()

    return result