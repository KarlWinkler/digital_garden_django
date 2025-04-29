import re

from post.models import Category

class PostService():
    @classmethod
    def slugify(klass, text: str):
        text = re.sub(r'[\s]+', ' ', text)
        text = re.sub(r'[^A-Za-z0-9\s]+', '', text).strip()

        return text.replace(' ', '-').lower()
