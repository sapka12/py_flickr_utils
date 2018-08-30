import argparse
from contextlib import contextmanager
from flickr_tools import get_flickr, photoset_id, pictures_in_photoset, hash_by_photoid, add_tag


@contextmanager
def print_time():
    import datetime
    start = datetime.datetime.now()
    yield
    end = datetime.datetime.now()
    print(end - start)


def main(args):
    set_name = args.album_name

    flickr = get_flickr(args.api_key, args.api_secret, args.token, args.token_secret)

    set_id = photoset_id(set_name, flickr)
    pics = [p['id'] for p in pictures_in_photoset(set_id, flickr)]

    hashes = []
    for pic_id in pics:
        try:
            md5_hash = hash_by_photoid(pic_id, flickr)
        except:
            print("error during gathering hash of", pic_id)

        if md5_hash:
            if md5_hash in hashes:
                if args.tag:
                    add_tag(pic_id, args.tag, flickr)
                else:
                    add_tag(pic_id, "duplicate", flickr)
                    add_tag(pic_id, "duplicate_in_" + set_name, flickr)
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
