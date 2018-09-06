import argparse
from flickr_tools import FlickrTools, print_time


def contains_tag(picture_id, tag, flickr):
<<<<<<< HEAD
    return tag in flickr.get_tags(picture_id)
=======
    return bool(tag in flickr.get_tags(picture_id))


def remove_from_set(picture_id, set_id, flickr):
    print("remove", picture_id, "from", set_id)
    flickr.photosets.removePhoto(photoset_id=set_id, photo_id=picture_id)
>>>>>>> master


def main(args):
    set_name = args.album_name
    tag = args.tag if args.tag else "duplicate"

    flickr = FlickrTools(args.api_key, args.api_secret, args.token, args.token_secret)

    set_id = flickr.photoset_id(set_name)
    pics = [p['id'] for p in flickr.pictures_in_photoset(set_id)]
    for picture_id in pics:
        if contains_tag(picture_id, tag, flickr):
            print("remove", picture_id, "from", set_id)
            flickr.remove_from_set(picture_id, set_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')
    parser.add_argument('--album_name', help="name of the Flickr album", type=str, required=True)
    parser.add_argument('--tag', help="tag which shows the picture is duplicated", type=str)

    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

    args = parser.parse_args()

    with print_time():
        main(args)
