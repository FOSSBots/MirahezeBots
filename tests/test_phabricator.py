import pytest
import vcr

testing_vcr = vcr.VCR(
    cassette_library_dir='tests/cassettes',
    record_mode='once'
)

import sys, os
sys.path.insert(0, os.path.abspath(__file__ + "/../.."))

from modules.utils.phabricator import PhabricatorClient

def test_get_task():
    with testing_vcr.use_cassette('phabricator_get_task.yaml'):
        phabricator = PhabricatorClient('phabricator.miraheze.org', 'api_token')

        task = phabricator.get_task(1)
        assert task.title == 'Tracking: Deployment of Miraheze'
        assert task.status == 'Resolved'
        assert task.author.username == 'John'
        assert task.owner.username == 'github-migration'


def test_find_tasks():
    with testing_vcr.use_cassette('phabricator_find_tasks.yaml'):
        phabricator = PhabricatorClient('phabricator.miraheze.org', 'api_token')
        priorities = [PhabricatorClient.PRIORITY_HIGH]
        statuses = [PhabricatorClient.STATUS_OPEN]
        tasks = phabricator.find_tasks(priorities=priorities, statuses=statuses)

        for task in tasks:
            assert task.priority == 'High'
            assert task.status == 'Open'
