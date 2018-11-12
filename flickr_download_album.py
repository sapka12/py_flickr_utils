import argparse
from flickr_tools import FlickrTools
from log import log

LOG = log(__name__)
out = "out.txt"


def add_to_file(content):
    with open(out, 'a') as the_file:
        the_file.write(content)
        the_file.write('\n')


def downloaded_ids():
    with open(out) as f:
        return f.read().splitlines()


def download_album(album, flickr):
    LOG.info("download_album: {}".format(album))
    album_id = flickr.album_id(album)
    if not album_id:
        album_id = album

    downloaded = downloaded_ids()

    pics = flickr.pictures_in_photoset(album_id)
    LOG.info("all pictures in album: {}".format(len(pics)))

    photos_to_download = [p for p in pics if not (p['id'] in downloaded)]
    LOG.info("photos_to_download: {}".format(len(photos_to_download)))

    directory = "./{}/".format(album)
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)

    failed = []
    counter = 0
    for photo in photos_to_download:
        try:
            flickr.download(photo['id'], photo['title'], folder=directory)
            add_to_file(photo['id'])
        except:
            failed.append(photo['id'])
            LOG.info("could not download: {} {}".format(photo['id'], photo['title']))
        counter += 1
        LOG.info("{}/{}".format(counter, len(photos_to_download)))

    if failed:
        LOG.warning("failed:")
        for f in failed:
            LOG.warning(f)


def main(args):
    flickr = FlickrTools(args.api_key, args.api_secret, args.token, args.token_secret)
    for album in args.album:
        download_album(album, flickr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')
    parser.add_argument('--album', help="name or id of the Flickr album", type=str, nargs='+', required=True)

    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

    main(parser.parse_args())
