"""Phabricator API intercation utility."""

from json import JSONDecodeError
from urllib.parse import urlparse

from requests import Session
from requests_cache import install_cache, uninstall_cache

BOLD = '\x02'


def gettaskinfo(host, apikey, task=1, session=Session()):
    """Get information on a specific task."""
    data = {
        'api.token': apikey,
        'constraints[ids][0]': task,
    }
    response = session.post(
        url=f'{host}/maniphest.search',
        data=data)
    response = response.json()
    try:
        result = response.get('result').get('data')[0]
    except AttributeError:
        return 'An error occurred while parsing the result.'
    except IndexError:
        return None
    install_cache('phab_user_cache', expire_after=2628002, allowable_methods=('POST'))  # a month
    ownerPHID = result.get('fields').get('ownerPHID')
    authorPHID = result.get('fields').get('authorPHID')
    if ownerPHID is not None:
        params = {
            'api.token': apikey,
            'constraints[phids][0]': ownerPHID,
        }
        response2 = session.post(
            url=f'{host}/user.search',
            data=params)
        try:
            response2 = response2.json()
        except JSONDecodeError as e:
            raise ValueError(f'Encountered {e} on {response2.text}')
        owner = response2.get('result').get('data')[0].get('fields').get('username')
    elif ownerPHID is None:
        owner = None
    if ownerPHID == authorPHID:
        author = owner
    else:
        params2 = {
            'api.token': apikey,
            'constraints[phids][0]': authorPHID,
        }
        response3 = session.post(
            url=f'{host}/user.search',
            data=params2)
        uninstall_cache()
        response3 = response3.json()
        author = response3.get('result').get('data')[0].get('fields').get('username')
    priority = result.get('fields').get('priority').get('name')
    status = result.get('fields').get('status').get('name')
    output = f"{'https://' + str(urlparse(host).netloc)}/T{str(result['id'])} - "
    output = '{0}{2}{1}{2}, '.format(output, str(result.get('fields').get('name')), BOLD)
    output = output + 'authored by {1}{0}{1}, '.format(author, BOLD)
    output = output + 'assigned to {1}{0}{1}, '.format(owner, BOLD)
    output = output + 'Priority: {1}{0}{1}, '.format(priority, BOLD)
    output = output + 'Status: {1}{0}{1}'.format(status, BOLD)
    return output  # noqa: R504


def dophabsearch(host, apikey, querykey, limit=True, session=Session()):
    """Perform a maniphest search."""
    data = {
        'api.token': apikey,
        'queryKey': querykey,
    }
    response = session.post(
        url=f'{host}/maniphest.search',
        data=data)
    response = response.json()
    result = response.get('result')
    try:
        data = result.get('data')
    except AttributeError:
        return None
    x = 0
    searchphab = []
    while x < len(data):
        currdata = data[x]
        if x > 5 and limit:
            return ['Limit exceeded. Please perform this search directly on phab.']
        searchphab.append(gettaskinfo(host, apikey, task=currdata.get('id'), session=session))
        x = x + 1
    return searchphab
