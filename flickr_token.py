import argparse

from flickr_tools import FlickrTools


def main(args):
    FlickrTools(args.api_key, args.api_secret)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Authenticate Flickr.')

    parser.add_argument('--api_key', help="Api Key", type=str, required=True)
    parser.add_argument('--api_secret', help="Api Secret", type=str, required=True)

    main(parser.parse_args())
