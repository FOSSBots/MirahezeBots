"""Phabricator client classes."""

import requests


class PhabricatorClient:
    """Simple Phabricator client."""

    PRIORITY_HIGH = 75

    STATUS_OPEN = 'open'

    def __init__(self, host, api_token):
        """Create client for specified host and api token."""
        self.host = host
        self.api_token = api_token

    def api_request(self, method, params):
        """Make api request to Phabricator."""
        params['api.token'] = self.api_token
        r = requests.get('https://{}/api/{}'.format(self.host, method),
                         params=params)
        return r.json()['result']

    def get_task(self, task_id):
        """Get task by id."""
        result = self.api_request('maniphest.search', {
            'constraints[ids][0]': task_id
        })['data']

        if len(result) > 0:
            result = result[0]
        else:
            return None

        task = PhabricatorTask(self)
        task.id = result['id']
        task.title = result['fields']['name']
        task.ownerPHID = result['fields']['ownerPHID']
        task.authorPHID = result['fields']['authorPHID']
        task.status = result['fields']['status']['name']
        return task

    def get_user(self, user_phid):
        """Get user by phid."""
        result = self.api_request('user.search', {
            'constraints[phids][0]': user_phid
        })['data'][0]

        user = PhabricatorUser(self)
        user.username = result['fields']['username']
        return user

    def find_tasks(self, priorities=[], statuses=[]):
        """Find tasks."""
        params = {}

        for i in range(0, len(priorities)):
            params['constraints[priorities]['+str(i)+']'] = priorities
        for i in range(0, len(statuses)):
            params['constraints[statuses]['+str(i)+']'] = statuses

        result = self.api_request('maniphest.search', params)['data']
        tasks = []
        for entry in result:
            task = PhabricatorTask(self)
            print(entry)
            task.id = entry['id']
            task.title = entry['fields']['name']
            task.ownerPHID = entry['fields']['ownerPHID']
            task.authorPHID = entry['fields']['authorPHID']
            task.priority = entry['fields']['priority']['name']
            task.status = entry['fields']['status']['name']
            task.dateModified = entry['fields']['dateModified']
            tasks.append(task)
        return tasks

class PhabricatorTask:
    """Class representing Phabricator task."""

    def __init__(self, client):
        """Create instance for client."""
        self.client = client

    @property
    def author(self):
        """Get task author."""
        if self.authorPHID is None:
            return None

        if not hasattr(self, '_author'):
            self._author = self.client.get_user(self.authorPHID)
        return self._author

    @property
    def owner(self):
        """Get task owner/assignee."""
        if self.ownerPHID is None:
            return None

        if not hasattr(self, '_owner'):
            self._owner = self.client.get_user(self.ownerPHID)
        return self._owner

    @property
    def link(self):
        """Get link to the task."""
        return "https://{}/T{}".format(self.client.host, self.id)


class PhabricatorUser:
    """Class representing Phabricator user."""

    def __init__(self, client):
        """Create instance for client."""
        self.client = client
