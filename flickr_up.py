import sys
import os
import logging
from flickr_tools import photosets, pictures_in_photoset, get_flickr, add_to_album

log_file = "flickr_up.log"

logging.basicConfig(
    filename=log_file,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.WARN
)

flickr = get_flickr()


def upload_photo(filename):
    response = flickr.upload(filename)

    # magic
    photoid = response[0].text
    return photoid


def _contains(album, filename):
    albums = [a for a in photosets(flickr) if a[1] == album]
    if albums:
        album_id = albums[0][0]
        name = filename.split(os.sep)[-1]
        pic_names = [p['title'] for p in pictures_in_photoset(album_id, flickr)]
        return name in pic_names
    return False


def parse_foldername(filename):
    return os.path.basename(os.path.dirname(os.path.realpath(filename)))


if __name__ == '__main__':
    filename = sys.argv[1]

    if len(sys.argv) > 2:
        album = sys.argv[2]
    else:
        album = parse_foldername(filename)

    if _contains(album, filename):
        logging.info("album {} already contains {}".format(album, filename))
    else:
        pic_id = upload_photo(filename)
        add_to_album(pic_id, album, flickr)
        logging.warning("uploaded {} into album {}".format(filename, album))
