import argparse
from flickr_tools import FlickrTools


def download_album(album, flickr):
    album_id = flickr.album_id(album)
    if not album_id:
        album_id = album

    for photo in flickr.pictures_in_photoset(album_id):
        flickr.download(photo['id'], photo['title'], album + "_")


def main(args):
    flickr = FlickrTools(args.api_key, args.api_secret, args.token, args.token_secret)
    download_album(args.album, flickr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')
    parser.add_argument('--album', help="name or id of the Flickr album", type=str, required=True)

    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

    main(parser.parse_args())
