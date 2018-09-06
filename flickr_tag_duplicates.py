import argparse
from flickr_tools import FlickrTools, print_time


def main(args):
    set_name = args.album_name

    flickr = FlickrTools(args.api_key, args.api_secret, args.token, args.token_secret)

    set_id = flickr.photoset_id(set_name)
    pics = [p['id'] for p in flickr.pictures_in_photoset(set_id)]

    hashes = []
    for pic_id in pics:
        try:
            md5_hash = flickr.hash_by_photoid(pic_id)
        except:
            print("error during gathering hash of", pic_id)

        if md5_hash:
            if md5_hash in hashes:

                print("tagged", pic_id)

                if args.tag:
                    tags = args.tag.split(",")
                    for tag in tags:
                        flickr.add_tag(pic_id, tag)
                else:
                    flickr.add_tag(pic_id, "duplicate")
                    flickr.add_tag(pic_id, "duplicate_in_" + set_name)
            else:
                hashes.append(md5_hash)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')
    parser.add_argument('--album_name', help="name of the Flickr album", type=str, required=True)
    parser.add_argument('--tag', help="add this tag to the duplicated pictures", type=str)

    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--token_secret', help="id of the Flickr album", type=str, required=True)

    args = parser.parse_args()

    with print_time():
        main(args)
