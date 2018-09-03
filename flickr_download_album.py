import argparse
from flickr_tools import FlickrTools


def download_album(album_id, flickr):
    for photo in flickr.pictures_in_photoset(album_id):
        flickr.download(photo['id'], photo['title'], album_id + "_")


def main():
    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')
    parser.add_argument('--album_id', help="id of the Flickr album", type=str, required=True)

    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

    args = parser.parse_args()

    flickr = FlickrTools(args.api_key, args.api_secret, args.token, args.token_secret)
    download_album(args.album_id, flickr)


if __name__ == '__main__':
    main()
