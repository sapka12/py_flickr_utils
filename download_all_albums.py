import argparse
from flickr_tools import FlickrTools
from flickr_download_album import download_album


def main(args):
    flickr = FlickrTools(args.api_key, args.api_secret, args.token, args.token_secret)

    albums = flickr.albums()
    for _, album_name in albums:
        print("downloading", album_name)
        download_album(album_name, flickr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')
    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

    main(parser.parse_args())
