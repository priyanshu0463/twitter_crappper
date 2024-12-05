Twitter Scraper using Selenium
This project is a web scraper built with Selenium to log in to Twitter (X.com) and scrape tweets and associated images based on specific keywords.

Features
Automated login to Twitter.
Scrapes tweets for specified keywords.
Extracts tweet content and associated images.
Saves data to a JSON file.
Prerequisites
Before setting up and running the project, ensure you have the following:

Python (>=3.8)
Google Chrome browser (latest version)
ChromeDriver matching your Chrome browser version
Selenium Python library
dotenv Python library
Setup Instructions
1. Clone the Repository
bash
Copy code
git clone <repository-url>
cd <repository-folder>
2. Install Python Dependencies
Create a virtual environment (optional but recommended):

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install the required Python libraries:

bash
Copy code
pip install selenium python-dotenv
3. Configure Environment Variables
Create a .env file in the project directory to store your Twitter credentials:

makefile
Copy code
TWITTER_USERNAME=<your-twitter-username>
TWITTER_PASSWORD=<your-twitter-password>
TWITTER_EMAIL=<your-twitter-email>
Note: These credentials are necessary to log in and should be kept private. Use environment variable management tools for secure storage.

4. Prepare Input Keywords
Create a file named key.json in the project directory with a list of keywords to scrape:

json
Copy code
{
  "keywords": ["keyword1", "keyword2", "keyword3"]
}
5. Set Up ChromeDriver
Download ChromeDriver that matches your Chrome version from here.
Move the chromedriver executable to a known location (e.g., /usr/lib/chromium-browser/ or any directory in your PATH).
Update the Service path in the script if needed:
python
Copy code
service = Service("/path/to/chromedriver")
6. Run the Script
Run the project by executing the script:

bash
Copy code
python3 <script-name>.py
Output
The script will save scraped data to imgs.json in the following format:
json
Copy code
[
  {
    "keyword": "example",
    "content": "This is a tweet about example",
    "images": [
      "https://pbs.twimg.com/media/example1.jpg",
      "https://pbs.twimg.com/media/example2.jpg"
    ]
  }
]
Notes
Make sure your .env file is correctly configured to avoid login issues.
If you encounter errors during scraping, check your ChromeDriver setup and Selenium version.
To run in headless mode, ensure the following Chrome options are active:
python
Copy code
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
License
This project is licensed under the MIT License. See the LICENSE file for details.
