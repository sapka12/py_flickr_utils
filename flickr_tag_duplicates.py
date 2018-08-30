import os
import sys
import urllib
import hashlib
from flickr_tools import get_flickr, photoset_id, pictures_in_photoset
from contextlib import contextmanager
import argparse


def group(tuple_list):
    _dict = {}
    for k, v in tuple_list:
        if k in _dict:
            _dict[k].append(v)
        else:
            _dict[k] = [v]
    return _dict


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def hash_by_photoid(photo_id, flickr):
    url = flickr.photos.getSizes(photo_id=photo_id)[0][0].attrib["source"]
    filename = photo_id
    urllib.request.urlretrieve(url, filename)
    md5_hash = md5(filename)
    print(photo_id, md5_hash)
    os.remove(filename)
    return md5_hash

@contextmanager
def print_time():
    import datetime
    start = datetime.datetime.now()
    yield
    end= datetime.datetime.now()
    print(end - start)


def add_tag(photo_id, tag, flickr):
    flickr.photos.addTags(photo_id=photo_id, tags=tag)


def try_it(func):
    try:
        return func()
    except:
        return None


def main(args):
    set_name = args.album_name

    flickr = get_flickr(args.api_key, args.api_secret, args.token, args.token_secret)

    set_id = photoset_id(set_name, flickr)
    pics = [p['id'] for p in pictures_in_photoset(set_id, flickr)]
    hashes = [(try_it(lambda: hash_by_photoid(pic_id, flickr)), pic_id) for pic_id in pics]
    hashes = [h for h in hashes if h[0]]
    groups = group(hashes)

    print("hashes are gathered")

    for photo_hash, photo_ids in groups.items():
        keep_photo_id, *duplicate_photo_ids = photo_ids

        print("keep", keep_photo_id)
        if duplicate_photo_ids:
            print("duplicates", duplicate_photo_ids)

        for duplicate_photo_id in duplicate_photo_ids:
            add_tag(duplicate_photo_id, "duplicate", flickr)
            add_tag(duplicate_photo_id, "duplicate_in_" + set_name, flickr)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')
    parser.add_argument('--album_name', help="name of the Flickr album", type=str, required=True)

    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

    args = parser.parse_args()

    with print_time():
        main(args)
