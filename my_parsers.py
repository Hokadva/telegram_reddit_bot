import requests
import random
from bs4 import BeautifulSoup
import io
from io import BytesIO
from data_base_manage import Database


class Parser():
    def __init__(self, URL):
        self.folder_url = URL
        self.DATABASE = Database('subreddits')


    def get_reserve_image(self):
        """Возвращает BytesIO с изображением для bot.send_photo()"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(self.folder_url, headers=headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        image_ids = []
        for div in soup.find_all('div', attrs={'data-id': True}):
            if 'image' in div.get('aria-label', '').lower() or any(ext in div.text.lower() for ext in ['jpg', 'png', 'gif']):
                image_ids.append(div['data-id'])
        if not image_ids:
            return None
        file_id = random.choice(image_ids)
        img_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        img_resp = requests.get(img_url, headers=headers, stream=True)
        if img_resp.status_code == 200:
            image = io.BytesIO(img_resp.content)
            image.name = 'image.jpg'
            return image
        thumb_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"
        thumb_resp = requests.get(thumb_url, headers=headers)
        if thumb_resp.status_code == 200:
            image = io.BytesIO(thumb_resp.content)
            image.name = 'image.jpg'
            return image
        return None


    def get_image(self):
        """Случайное изображение с Reddit"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        self.subreddit = self.DATABASE.random_print()[0]
        try:
            resp = requests.get(
                f"https://www.reddit.com/r/{self.subreddit}/hot.json?limit=30",
                headers=headers
            )
            data = resp.json()
            posts = data['data']['children']
            img_urls = []
            for post in posts:
                post_data = post['data']
                url = post_data['url']
                if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    img_urls.append(url)
            if not img_urls:
                return None
            img_url = random.choice(img_urls)
            img_resp = requests.get(img_url, headers=headers)
            image = BytesIO(img_resp.content)
            image.name = f'reddit_{self.subreddit}.jpg'
            return image
        except Exception as e:
            print(f"Reddit ошибка: {e}")
            return None
