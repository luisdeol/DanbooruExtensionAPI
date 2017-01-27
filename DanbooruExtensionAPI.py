from flask import Flask, request
from flask_restful import Resource, Api
from bs4 import BeautifulSoup
import urllib.request
import json
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
        # Retrieving urls for each image.
        for image_article in image_articles:
            image_urls.append(base_url + image_article['data-file-url'])
            if not os.path.exists(path):
                os.makedirs(path)
        #Iterate over the urls list and downloading the images.
        for url in image_urls:
            image_name = url.split('/')[-1]
            urllib.request.urlretrieve(url, path + image_name)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

api.add_resource(DanbooruScraper, '/api/download_images/<string:tags>')

if __name__ == '__main__':
    app.run(debug = True)
