import argparse
from contextlib import contextmanager

from flickrapi import FlickrError
import flickr_tools as fkr


def get_album(title):
    import re
    nums = re.sub("[^0-9]", "", title)
    year = nums[0:4]
    month = nums[4:6]

    def valid(y, m):
        try:
            return 1900 < int(y) < 2100 and 1 <= int(m) <= 12
        except:
            return False

    def album_format(y, m):
        return "{}-{}".format(y, m)

    if valid(year, month):
        return album_format(year, month)
    else:
        month = nums[2:4]
        year = nums[4:8]
        if valid(year, month):
            return album_format(year, month)


def upload(pic, album, flickr):
    try:
        fkr.add_to_album(pic['id'], album, flickr)
        print(pic['title'], "added to", album)
    except FlickrError as f_err:
        print(pic['title'], "already in", album)


def main(args):
    albumname = args.album_name if args.album_name else "Auto Upload"
    flickr = fkr.get_flickr(args.api_key, args.api_secret, args.token, args.token_secret)
    set_id = fkr.photoset_id(albumname, flickr)
    pics = fkr.pictures_in_photoset(set_id, flickr)

    for pic in pics:
        album = get_album(pic['title'])
        if album:
            upload(pic, album, flickr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')
    parser.add_argument('--album_name', help="name of the Flickr album", type=str)
    parser.add_argument('--tag', help="add this tag to the duplicated pictures", type=str)

    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

    main(parser.parse_args())
