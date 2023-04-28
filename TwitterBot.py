from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys

website = "https://www.twitter.com"
path = "/Users/hveer/Downloads/chromedrive"

class FireUp():
    driver = None

    def __init__(self, website, path):
        self.website = str(website)
        self.path = str(path)

    def the_site(self):
        FireUp.driver = webdriver.Chrome(options=options, service=Service(path))
        FireUp.driver.get(website)
        FireUp.driver.maximize_window()

    @classmethod
    def get_driver(cls):
        return cls.driver

class  TwitterSignIn():
    def __init__(self, userName, passWord):
        self.userName = userName
        self.passWord = passWord

    @classmethod
    def signIn(cls):
        driver = FireUp.get_driver()
        try:
            login = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layers"]//a')))
            login.click()
        except:
            pass
        try:
            login = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]//div[3]/div[5]/a')))
            login.click()
        except:
            pass
        userName = input('What is your twitter email or username? ')
        username = driver.find_element(By.XPATH,'//div/input[@autocomplete = "username"]')
        username.send_keys(userName)
        next = driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]//div[2]//div[6]')
        next.click()
        passWord = input('What is your password? ')
        password = driver.find_element(By.XPATH, '//div/input[@name = "password"]')
        password.send_keys(passWord)
        access = driver.find_element(By.XPATH, "//div[contains(@data-testid, 'Login')]//span")
        access.click()
        try:
            popup = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//div//span[contains(text(), "Skip")]')))
            popup.click()
        except:
            pass
        try:
            search = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]')))
            search.click()
            keyword_search = driver.find_element(By.XPATH,'//*[@id="react-root"]//main//div[1]/div[1]/div[1]//div[1]/div[2]//form/div[1]//label/div[2]/div/input')
            keyword_search.click()
            key_to_search = input('What would you like to search for on Twitter? ')
            keyword_search.send_keys(key_to_search)
            keyword_search.send_keys(Keys.ENTER)
        except:
            pass


def tweet_scrape(tweet):
    try:
        username = tweet.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
        tweet_text = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
        name = tweet.find_element(By.XPATH, './/span/*').text
        tweets_data = [name, username, tweet_text]
    except:
        tweets_data = ['null', 'null', 'null']
    return tweets_data

def scroll_down(driver, scrolls=5, sleep_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_tweet_id(tweet):
    tweet_id = tweet.get_attribute('data-tweet-id')
    return tweet_id


FireUp(website, path).the_site()
TwitterSignIn.signIn()

scroll_down(FireUp.get_driver(), scrolls=10, sleep_time=2)

unique_tweet_ids = set()
name_data = []
user_data = []
tweet_data = []
tweets = WebDriverWait(FireUp.get_driver(), 3).until(EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]')))
for tweet in tweets:
    tweet_id = get_tweet_id(tweet)
    if tweet_id not in unique_tweet_ids:
        unique_tweet_ids.add(tweet)
        tweet_list = tweet_scrape(tweet)
        name_data.append(tweet_list[0])
        user_data.append(tweet_list[1])
        tweet_data.append(" ".join(tweet_list[2].split()))

scraped_tweets = pd.DataFrame({'Name': name_data, 'Username': user_data, 'Tweet': tweet_data})
scraped_tweets.to_csv('Scraped_Twitter_Files.csv', index=False)

