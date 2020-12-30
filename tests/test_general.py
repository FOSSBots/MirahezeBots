"""General tests for all MHB plugins."""
import os
import re
import sqlite3
import sys

import models

from sqlalchemy import create_engine

PATH = '../MirahezeBots/MirahezeBots'
PLUGINPATH = '../MirahezeBots/MirahezeBots/plugins'
sys.path.append(PATH)


def test_db_schema_is_same():
    """Confirms database matches as expected."""
    original, new = set(), set()  # noqa: F841
    with sqlite3.connect(os.path.join(PATH, 'example.db')) as conn:
        conn.text_factory = str
        res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        [original.add(tbl[0]) for tbl in res if not tbl[0] == 'nick_ids' and not tbl[0] == 'sqlite_sequence']

    try:
        os.unlink(os.path.join(PATH, "example-model.db"))
    except FileNotFoundError:
        pass

    engine = create_engine('sqlite:///{0}'.format(os.path.join(PATH, "..", "example-model.db")))
    models.Base.metadata.create_all(bind=engine)
    assert original == set(engine.table_names())


def test_line_length():
    """Checks line length."""
    MAX_LENGTH = 265 + 1
    for top, dirs, files in os.walk(PLUGINPATH):
        for filen in files:
            if not filen.endswith('.py'):
                continue
            with open(os.path.join(PLUGINPATH, filen)) as python_source:
                src = python_source.readlines()
                for line_number, line in enumerate(src):
                    assert len(line.strip()) < MAX_LENGTH, 'length of line #{0} exceeds limit'.format(line_number)


def test_no_get_on_lists():
    """Checks for misuse of .get() on lists."""
    reg = r'get\([0-9]'
    for top, dirs, files in os.walk(PLUGINPATH):
        for filen in files:
            if not filen.endswith('.py'):
                continue
            with open(os.path.join(PLUGINPATH, filen)) as python_source:
                src = python_source.read()
                assert not re.search(reg, src)
