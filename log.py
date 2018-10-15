import logging.config
import yaml


def log(name, path='logging.yaml'):
    with open(path, 'rt') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        return logging.getLogger(name)
