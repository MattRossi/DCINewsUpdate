import configparser
import praw
from praw.models import Subreddit
from praw.models.reddit.wikipage import WikiPage
from praw.models.reddit.subreddit import SubredditStylesheet
from dcinewsupdate.dci import Story


class Reddit:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.properties')
        self.reddit: praw.Reddit = praw.Reddit(
            client_id=config['REDDIT']['CLIENT_ID'],
            client_secret=config['REDDIT']['CLIENT_SECRET'],
            password=config['REDDIT']['PASSWORD'],
            user_agent=config['REDDIT']['USER_AGENT'],
            username=config['REDDIT']['USERNAME'],
        )
        self.subreddit: Subreddit = self.reddit.subreddit(config['REDDIT']['SUBREDDIT'])

    def update_image(self, story: Story):
        stylesheet: SubredditStylesheet = self.subreddit.stylesheet
        stylesheet.upload(image_path = story.photo, name = 'sidebarimg')
        stylesheet.update(self.subreddit.stylesheet().stylesheet)

    def update_link(self, story: Story):
        wiki: WikiPage = self.subreddit.wiki['config/sidebar']
        before_content: str = wiki.content_md
        new_content = before_content.split('[Sidebarimglink]')[0]
        new_content += f'[Sidebarimglink]({story.url})'
        wiki.edit(content=new_content)
