from MirahezeBots_jsonparser import jsonparser as jp

DICT = {'#miraheze-cvt-private': {'inherits-from': ['#miraheze-cvt']}, '#miraheze-cvt': {'chanops': ['NDKilla', 'Voidwalker', 'Reception123', 'The_Pionner', 'JohnLewis', 'Zppix']}}

ALTDICT = {'#miraheze-cvt-fake': {'inherits-from': ['#miraheze-cvt']}, '#miraheze-cvt': {'chanops': ['NDKilla', 'Voidwalker', 'Reception123', 'The_Pionner', 'JohnLewis', 'Zppix']}}


def test_create_dict():
    assert DICT == jp.createdict('tests/test_json.json')


def test_check_dict_true():
    result = jp.validatecache('tests/test_json.json', DICT)
    assert result is True


def test_check_dict_false():
    result = jp.validatecache('tests/test_json.json', ALTDICT)
    assert result is False
