import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Auto-login function
def auto_login(driver, username, password, email):
    login_url = "https://x.com/login"
    driver.get(login_url)
    time.sleep(5)


    username_input = driver.find_element(By.NAME, "text")
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)
    time.sleep(3)  

    
    try:
        email_input = driver.find_element(By.NAME, "text")
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)
        time.sleep(3)
    except Exception as e:
        print("Email input step skipped:", e)

    
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

# Scraping function
def scrape_tweets(driver, keyword, tweet_data, max_tweets=1000):
    print(f"Scraping tweets for: {keyword}")
    seen_tweets = set(tweet["content"] for tweet in tweet_data if tweet.get("keyword") == keyword)
    scroll_pause = 3
    search_url = f"https://x.com/search?q={keyword}&src=typed_query&f=live"
    driver.get(search_url)
    time.sleep(5)

    def extract_tweets():
        tweets = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        for tweet in tweets:
            try:
                content = tweet.text.strip()
                if content and content not in seen_tweets:
                    image_elements = tweet.find_elements(By.XPATH, ".//img[contains(@src, 'https://pbs.twimg.com/media/')]")
                    image_urls = [img.get_attribute("src") for img in image_elements]
                    tweet_data.append({
                        "keyword": keyword,
                        "content": content,
                        "images": image_urls
                    })

                    seen_tweets.add(content)
                    if len(seen_tweets) >= max_tweets:
                        return True
            except Exception as e:
                print(f"Error extracting tweet: {e}")
        return False
    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(seen_tweets) < max_tweets:
        if extract_tweets():
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print(f"Completed scraping for {keyword}. Total tweets: {len(seen_tweets)}.")


def extract_and_group_links(input_file, output_file):
    # Load existing data from the output JSON file if it exists
    existing_links = {"telegram": set(), "other_links": set()}
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
                existing_links["telegram"] = set(entry["link"] for entry in existing_data.get("telegram", []))
                existing_links["other_links"] = set(entry["link"] for entry in existing_data.get("other_links", []))
            except json.JSONDecodeError:
                print(f"{output_file} is empty or corrupted. Starting fresh.")
                existing_data = {"telegram": [], "other_links": []}
    else:
        existing_data = {"telegram": [], "other_links": []}

    # Load the input JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    # Extract and categorize links
    telegram_links = []
    other_links = []
    for item in input_data:
        content = item.get("content", "")
        # Find all links
        links = re.findall(r'(https?://[^\s]+)', content)
        for link in links:
            if re.match(r'http[s]?://(t\.me|T\.me)/', link):
                if link not in existing_links["telegram"]:
                    telegram_links.append({"link": link, "content": content.strip()})
                    existing_links["telegram"].add(link)
            else:
                if link not in existing_links["other_links"]:
                    other_links.append({"link": link, "content": content.strip()})
                    existing_links["other_links"].add(link)

    # Append new links to the existing data
    if telegram_links:
        existing_data["telegram"].extend(telegram_links)
    if other_links:
        existing_data["other_links"].extend(other_links)

    # Write the updated data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    print(f"Added {len(telegram_links)} new Telegram links and {len(other_links)} other links to {output_file}.")

# Main execution
def main():
    load_dotenv()
    keywords_file = "key.json"
    output_file = "imgs_0512.json"
    # current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # output_file = f"tweets_{current_time}.json"
    with open(keywords_file, 'r', encoding='utf-8') as f:
        keywords = json.load(f).get("keywords", [])

    if not keywords:
        print("No keywords found in the input JSON file.")
        return
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            try:
                tweet_data = json.load(f)
            except json.JSONDecodeError:
                tweet_data = []
    else:
        tweet_data = []

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service("/usr/lib/chromium-browser/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Replace these with your credentials
    username = os.getenv("TWITTER_USERNAME")
    password = os.getenv("TWITTER_PASSWORD")
    email = os.getenv("TWITTER_EMAIL")

    auto_login(driver, username, password, email)

    for keyword in keywords:
        scrape_tweets(driver, keyword, tweet_data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tweet_data, f, ensure_ascii=False, indent=4)

    print(f"Scraping completed for all keywords. Data saved to {output_file}.")

    extract_and_group_links(output_file, "links/sus-links.json")

    # Quit the driver
    driver.quit()

if __name__ == "__main__":
    main()
