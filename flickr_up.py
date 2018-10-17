import argparse
from flickr_tools import FlickrTools, print_time
import os
from retry import retry5x
from log import log

LOG = log(__name__)


def _contains(album, filename, flickr):
    albums = [a for a in flickr.photosets() if a[1] == album]
    if albums:
        album_id = albums[0][0]
        name = filename.split(os.sep)[-1]
        pic_names = [p['title'] for p in flickr.pictures_in_photoset(album_id)]
        return name in pic_names
    return False


def parse_foldername(path):
    return os.path.basename(os.path.dirname(os.path.realpath(path)))


def parse_pic_title(path):
    return os.path.basename(os.path.splitext(path)[0])


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def is_pic_in_album(path, album_id, flickr):
    pic_title = parse_pic_title(path)

    def title_match(pic):
        def base_name(_):
            ext = ".jpg"
            lower = _.lower()
            without_ext = lower[:(-1 * len(ext))] if lower.endswith(ext) else lower
            return without_ext

        return base_name(pic["title"]) == base_name(pic_title)

    return any(map(title_match, flickr.pictures_in_photoset(album_id)))


def upload_into_album(album_name, path, flickr):
    photo_id = flickr.upload_photo(path)
    flickr.add_to_album(photo_id, album_name)
    LOG.info('uploaded %s', path)


def upload_path(path, flickr):
    def upload_path_once():
        album_name = parse_foldername(path)
        album_id = flickr.photoset_id(album_name)

        if (not album_id) or (not is_pic_in_album(path, album_id, flickr)):
            upload_into_album(album_name, path, flickr)

    retry5x(upload_path_once)


def main(args):
    base_folder = args.folder
    flickr = FlickrTools(args.api_key, args.api_secret, args.token, args.token_secret)

    pic_paths = flatten([
        [os.path.join(root, file) for file in files if file.lower().endswith(".jpg")]
        for root, dirs, files in os.walk(base_folder)
    ])

    for path in pic_paths:
        upload_path(path, flickr)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='upload all pictures to Flickr into albums from a folder recursively')
        parser.add_argument('--folder', help="source folder of the pictures", type=str, required=True)

        parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
        parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
        parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
        parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

        args = parser.parse_args()

        with print_time():
            main(args)
    except Exception as e:
        import logging
        logging.exception("message")