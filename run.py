from dcinewsupdate.reddit import Reddit
from dcinewsupdate.dci import DCI, Story

story: Story = DCI.get_news()
reddit = Reddit()
reddit.update_image(story)
reddit.update_link(story)
