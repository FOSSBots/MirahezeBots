from MirahezeBots.utils import jsonparser as jp
import os


DICT = {'#miraheze-cvt-private': {'inherits-from': ['#miraheze-cvt']}, '#miraheze-cvt': {'chanops': ['NDKilla', 'Voidwalker', 'Reception123', 'The_Pionner', 'JohnLewis', 'Zppix']}}
PATH = '../MirahezeBots/MirahezeBots/tests'


def test_create_dict():
    assert dict == jp.createdict(os.path.join(PATH, 'test_json.json'))
