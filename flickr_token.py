import argparse
import io
import flickrapi
from idna import unicode
from pip._vendor.distlib.compat import raw_input
import yaml

settings_filename = "settings.yaml"


def set_settings(settings):
    with io.open(settings_filename, 'w', encoding='utf8') as outfile:
        yaml.dump(settings, outfile, default_flow_style=False, allow_unicode=True)


def flickr_api(api_key, api_secret):
    return flickrapi.FlickrAPI(api_key, api_secret, store_token=False)


def main(args):
    flickr = flickr_api(args.api_key, args.api_secret)

    if not flickr.token_valid(perms=u'write'):
        flickr.get_request_token(oauth_callback='oob')

        authorize_url = flickr.auth_url(perms=u'write')
        print(authorize_url)

        verifier = unicode(raw_input('Verifier code: '))

        flickr.get_access_token(verifier)

        token = flickr.token_cache.token.token
        token_secret = flickr.token_cache.token.token_secret

        print("--token", token, "--token_secret", token_secret)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the content of a Flickr album.')

    parser.add_argument('--api_key', help="id of the Flickr album", type=str, required=True)
    parser.add_argument('--api_secret', help="id of the Flickr album", type=str, required=True)

    main(parser.parse_args())
