import logging
import os
import urllib
from contextlib import contextmanager

import flickrapi
from flickrapi.auth import FlickrAccessToken
import hashlib
from idna import unicode
from pip._vendor.distlib.compat import raw_input
from PIL import Image

log_file = "flickr_up.log"


@contextmanager
def print_time():
    import datetime
    start = datetime.datetime.now()
    yield
    end = datetime.datetime.now()
    print(end - start)


class FlickrTools:
    def __init__(self, api_key, api_secret, token=None, token_secret=None):
        if not token or not token_secret:
            token, token_secret = self.get_token(api_key, api_secret)
            print("--token", token, "--token_secret", token_secret)
        self.flickr = self.get_flickr(api_key, api_secret, token, token_secret)

    def get_token(self, api_key, api_secret):
        flickr = flickrapi.FlickrAPI(api_key, api_secret, store_token=False)

        flickr.get_request_token(oauth_callback='oob')

        authorize_url = flickr.auth_url(perms=u'write')
        print(authorize_url)

        verifier = unicode(raw_input('Verifier code: '))
        flickr.get_access_token(verifier)

        return flickr.token_cache.token.token, flickr.token_cache.token.token_secret

    def get_flickr(self, api_key, api_secret, token, token_secret):
        logging.basicConfig(
            filename=log_file,
            format='%(asctime)s %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.WARN
        )

        return flickrapi.FlickrAPI(api_key, api_secret, token=FlickrAccessToken(token, token_secret, u'write'))

    def photosets(self):
        _page_size = 500

        def go(aggr, _page):
            current_sets = [
                (ps[u'id'], ps[u'title'][u'_content'])
                for ps in self.flickr.photosets.getList(
                    format="parsed-json",
                    per_page=_page_size,
                    page=_page
                )[u'photosets'][u'photoset']
            ]

            new_aggr = aggr + current_sets

            if len(current_sets) < _page_size:
                return new_aggr
            else:
                go(new_aggr, _page + 1)

        return go([], 1)

    def photoset_id(self, set_name):
        for s in self.photosets():
            if s[1] == set_name:
                return s[0]

    def pictures_in_photoset(self, set_id):
        def photo_page(agg_pictures, _page):
            page_size = 500
            response = self.flickr.photosets.getPhotos(photoset_id=set_id, per_page=page_size, page=_page)
            act_pictures = [{'id': photo.attrib['id'], 'title': photo.attrib['title']} for photo in response[0]]
            agg = agg_pictures + act_pictures
            if len(act_pictures) < page_size:
                return agg
            else:
                return photo_page(agg, _page + 1)

        return photo_page([], 1)

    def set_photo_title(self, photo_id, title):
        self.flickr.photos.setMeta(photo_id=photo_id, title=title)

    def download(self, photo_id, filename, prefix=""):
        label_photo = "Original"
        label_video = "Video Original"
        ext_photo = ".jpg"
        ext_video = ".avi"

        response = self.flickr.photos.getSizes(photo_id=photo_id)
        is_video = any(map(lambda _: _.attrib["label"] == label_video, response[0]))

        label = label_video if is_video else label_photo
        ext = ext_video if is_video else ext_photo

        url = list(filter(
            lambda _: _.attrib["label"] == label,
            list(response[0])
        ))[0].attrib["source"]

        filename = prefix + (filename if filename.endswith(ext) else filename + ext)

        print("downloading: ", filename, url)

        try:
            urllib.request.urlretrieve(url, filename)
        except:
            print("error during download", filename, url)

    def create_album(self, album, photo_id):
        response = self.flickr.photosets.create(title=album, primary_photo_id=photo_id)
        return response[0].get("id")

    def add_to_album(self, pic_id, album_name):
        all_albums = self.photosets()
        same_albumnames = [a for a in all_albums if a[1] == album_name]
        if same_albumnames:
            album_id = same_albumnames[0][0]
            self.flickr.photosets.addPhoto(photoset_id=album_id, photo_id=pic_id)
        else:
            return self.create_album(album_name, pic_id)

    def pixels(self, fname):
        im = Image.open(fname)
        width = im.size[0]
        height = im.size[1]
        pix = im.load()

        def j(arr):
            return "".join(arr)

        def hexa(x, y):
            return j([hex(p) for p in pix[x, y]])

        return (
            j([j([hexa(x, y) for y in range(height)]) for x in range(width)])
        ).encode('utf-8')

    def md5(self, fname):
        px = self.pixels(fname)
        hash_md5 = hashlib.md5()
        hash_md5.update(px)
        return hash_md5.hexdigest()

    def hash_by_photoid(self, photo_id):
        url = self.flickr.photos.getSizes(photo_id=photo_id)[0][0].attrib["source"]
        filename = photo_id
        urllib.request.urlretrieve(url, filename)
        md5_hash = self.md5(filename)
        print(photo_id, md5_hash)
        os.remove(filename)
        return md5_hash

    def add_tag(self, photo_id, tag):
        self.flickr.photos.addTags(photo_id=photo_id, tags=tag)

    def get_tags(self, picture_id):
        response = self.flickr.tags.getListPhoto(photo_id=picture_id)
        return [tag.attrib['raw'] for tag in list(response[0][0])]

    def remove_from_set(self, picture_id, set_id):
        self.flickr.photosets.removePhoto(photoset_id=set_id, photo_id=picture_id)


    def upload_photo(self, filename):
        response = self.flickr.upload(filename)

        # magic
        photoid = response[0].text
        return photoid