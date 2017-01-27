from flask import Flask, request
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
import urllib.request
import os


app = Flask(__name__)
api = Api(app)

path = 'C:/Users/luisdeolpy/Documents/GitHub/DanbooruScraperAPI/images/'


class DanbooruScraper(Resource):
    def get(self, tags):
        image_urls = []
        base_url = 'http://danbooru.donmai.us/'
        url = 'http://danbooru.donmai.us/posts?tags=' + tags
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        image_articles = soup.find_all("article")
        for image_article in image_articles:
            image_urls.append(base_url + image_article['data-file-url'])
        for url in image_urls:
            image_name = url.split('/')[-1]
            urllib.request.urlretrieve(url, path + image_name)
        return 200

api.add_resource(DanbooruScraper, '/api/download_images/<string:tags>')

if __name__ == '__main__':
    app.run(debug = True)
