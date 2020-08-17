from MirahezeBots.utils import jsonparser as jp

DICT = {'#miraheze-cvt-private': {'inherits-from': ['#miraheze-cvt']}, '#miraheze-cvt': {'chanops': ['NDKilla', 'Voidwalker', 'Reception123', 'The_Pionner', 'JohnLewis', 'Zppix']}}

def test_create_dict():
  assert dict = jp.createdict('test_json.json')
