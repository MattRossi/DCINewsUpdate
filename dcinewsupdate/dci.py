from dataclasses import dataclass
import requests
from requests import Response


@dataclass
class Story:
    photo: str
    url: str

class DCI_API:

    BASE_URL: str = 'https://api.dci.org/api/v1/'

    @staticmethod
    def get_request(url: str) -> Response:
        response: Response = requests.get(
            url=url,
            timeout=30
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

    BASE_URL: str = 'https://www.dci.org/news/'
    STORY_INDEX: int = 0

    @staticmethod
    def get_news() -> Story:
        response: Response = DCI_API.get_request(DCI_API.BASE_URL + 'news?type=1')
        with open('img.jpg', 'wb') as f:
            f.write(DCI_API.get_request(response.json()[DCI.STORY_INDEX]['photoUrlThumb']).content)
        url = DCI.BASE_URL + response.json()[DCI.STORY_INDEX]['slug']
        return Story('img.jpg', url)
