"""General tests for all MHB plugins."""
import os
import re
import sqlite3
import sys
from contextlib import suppress

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
        for tbl in res:
            if tbl[0] not in ('nick_ids', 'sqlite_sequence'):
                original.add(tbl[0])
    with suppress(FileNotFoundError):
        os.unlink(os.path.join(PATH, 'example-model.db'))

    engine = create_engine(f"sqlite:///{os.path.join(PATH, '..', 'example-model.db')}")
    models.Base.metadata.create_all(bind=engine)
    assert original == set(engine.table_names())


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


def future_test_db_cleanup():
    """Confirms database matches as expected."""  # noqa: D401
    engine = create_engine(f'sqlite:///{os.path.join(PATH, "..", "hasan2.db")}')
    models.Base.metadata.create_all(bind=engine)
