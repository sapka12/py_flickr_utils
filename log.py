import logging.config
import yaml
import os


def log(name, path='{}/logging.yaml'.format(os.path.dirname(__file__))):
    with open(path, 'rt') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        return logging.getLogger(name)
