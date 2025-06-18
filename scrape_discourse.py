import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_discourse_posts(start_date, end_date):
       url = "https://discourse.onlinedegree.iitm.ac.in/c/tools-in-data-science"
       response = requests.get(url)
       soup = BeautifulSoup(response.text, 'html.parser')

       posts = []
       for post in soup.find_all('div', class_='topic-list-item'):
           title = post.find('a', class_='title').text
           link = post.find('a', class_='title')['href']
           date_str = post.find('time')['datetime']
           post_date = datetime.fromisoformat(date_str[:-1])  # Remove 'Z' for UTC

           if start_date <= post_date <= end_date:
               posts.append({
                   'title': title,
                   'link': link,
                   'date': post_date.isoformat()
               })

       return posts

   # Define date range
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 4, 14)

   # Scrape posts
discourse_posts = scrape_discourse_posts(start_date, end_date)

   # Save to JSON file
with open('discourse_posts.json', 'w') as f:
       json.dump(discourse_posts, f, indent=4)
if __name__ == "__main__":
       print("Scraping completed and saved to discourse_posts.json")
   