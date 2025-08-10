from dataclasses import dataclass
import requests
from requests import Response
from bs4 import BeautifulSoup
from PIL import Image


@dataclass
class Story:
    photo: str
    url: str

class API:

    DEFAULT_HEADERS: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) ' +\
            'Gecko/20100101 Firefox/141.0'
    }

    @staticmethod
    def get_request(url: str, headers: dict = None) -> Response:
        response: Response = requests.get(
            url=url,
            timeout=30,
            headers=headers if headers else None
        )
        print(f'Response Code: {response.status_code}')
        return response

    @staticmethod
    def post_request(url: str, data: str, headers: dict) -> Response:
        response: Response = requests.post(
            url= url,
            data = data,
            headers = headers,
            timeout=30
        )
        print(f'Response Code: {response.status_code} | Response Content: {response.content}')
        return response

class DCI:

    NEWS_SOURCE_URL: str = 'https://www.dci.org/news/?corpId&sort=desc&type=featured&pageno=1'

    @staticmethod
    def get_news() -> Story:
        response: Response = API.get_request(DCI.NEWS_SOURCE_URL, headers=API.DEFAULT_HEADERS)
        soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
        image_link: str = soup.find('div', class_='recent-story-item-img').find('img').attrs['src']
        with open('img.jpg', 'wb') as f:
            f.write(API.get_request(image_link, headers=API.DEFAULT_HEADERS).content)
        img = Image.open('img.jpg')
        img.save('img.jpg', quality=50, optimize=True)
        url: str = soup.find('div', class_='recent-story-item-info').find('a').attrs['href']
        return Story('img.jpg', url)
