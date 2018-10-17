import time


def retry(f, _times=1, **args):
    while _times > 0:
        try:
            return f(**args)
        except Exception as e:
            time.sleep(1)
            ex = e
            _times -= 1
    raise ex
