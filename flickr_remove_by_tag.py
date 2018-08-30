import argparse
import sys
from flickr_tools import get_flickr, photoset_id, pictures_in_photoset


def contains_tag(picture_id, tag, flickr):
    response = flickr.tags.getListPhoto(photo_id=picture_id)
    tags = [tag.attrib['raw'] for tag in list(response[0][0])]
    return bool(tag in tags)


def remove_from_set(picture_id, set_id, flickr):
    print("remove", picture_id, "from", set_id)
    flickr.photosets.removePhoto(photoset_id=set_id, photo_id=picture_id)


def main():
    set_name = args.album_name
    tag = args.tag if args.tag else "duplicate"

    flickr = get_flickr(args.api_key, args.api_secret, args.token, args.token_secret)

    set_id = photoset_id(set_name, flickr)
    pics = [p['id'] for p in pictures_in_photoset(set_id, flickr)]
    for picture_id in pics:
        if contains_tag(picture_id, tag, flickr):
            remove_from_set(picture_id, set_id, flickr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')
    parser.add_argument('--album_name', help="name of the Flickr album", type=str, required=True)
    parser.add_argument('--tag', help="tag which shows the picture is duplicated", type=str)

    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

    args = parser.parse_args()

    main(args)
