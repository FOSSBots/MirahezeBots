flake8 MirahezeBots/plugins --max-line-length 265 --exclude=__init__.py
flake8 tests --max-line-length 265
flake8 MirahezeBots/utils --max-line-length 265 --exclude=__init__.py
pytest tests/test_general.py
pytest tests/test_rss.py
pytest tests/test_json.py
pip-missing-reqs --ignore-file=setup.py --ignore-module=pytest --ignore-module=MirahezeBots.* .
pip-extra-reqs --ignore-requirement=sopel-plugins.adminlist --ignore-requirement=sopel-plugins.channelmgnt --ignore-requirement=sopel-plugins.pingpong --ignore-requirement=sopel-plugins.joinall .
pip check
