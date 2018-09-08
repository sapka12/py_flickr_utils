import unittest
from flickr_up import *


class flickr_up_spec(unittest.TestCase):
    def test_parse_pic_title(self):
        self.assertEqual(parse_pic_title("c:\\Users\\myuser\\pics\fancy_folder\pic_id.JPG"), "pic_id")
