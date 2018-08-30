import argparse
from flickr_tools import get_flickr, download


def download_album(album_id, flickr):
    photo_set = [{'id': p.attrib['id'], 'title': p.attrib['title']} for p in
                 list(flickr.photosets.getPhotos(photoset_id=album_id)[0])]

    for photo in photo_set:
        download(photo['id'], photo['title'], flickr, album_id + "_")


def main():
    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')
    parser.add_argument('--album_id', help="id of the Flickr album", type=str, required=True)

    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

    args = parser.parse_args()

    flickr = get_flickr(args.api_key, args.api_secret, args.token, args.token_secret)
    download_album(args.album_id, flickr)


if __name__ == '__main__':
    main()
