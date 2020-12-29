"""Phabricator API intercation utility."""

from requests import post
from json import JSONDecodeError
from urllib.parse import urlparse

def gettaskinfo(host, apikey, task=1):
    """Get's information on a specific task"""
    data = {
        'api.token': apikey,
        'constraints[ids][0]': task
    }
    response = post(
        url='{0}/maniphest.search'.format(host),
        data=data)
    response = response.json()
    try:
        result = response.get("result").get("data")[0]
    except AttributeError:
        return "An error occurred while parsing the result. "
    except IndexError:
        return "Sorry, but I couldn't find information for the task you searched."
    except Exception:
        return "An unknown error occured."
    params = {
        'api.token': apikey,
        'constraints[phids][0]': result.get("fields").get("ownerPHID")
    }
    response2 = post(
        url='{0}/user.search'.format(host),
        data=params)
    try:
        response2 = response2.json()
    except JSONDecodeError as e:
        raise JSONDecodeError("Encountered {0} on {1}".format(e, response2.text))
    params2 = {
        'api.token': apikey,
        'constraints[phids][0]': result.get("fields").get("authorPHID")
    }
    response3 = post(
        url='{0}/user.search'.format(host),
        data=params2)
    response3 = response3.json()
    if result.get("fields").get("ownerPHID") is None:
        owner = None
    else:
        owner = response2.get("result").get("data")[0].get("fields").get("username")
    author = response3.get("result").get("data")[0].get("fields").get("username")
    priority = result.get("fields").get("priority").get("name")
    status = result.get("fields").get("status").get("name")
    output = '{0}/T{1} - '.format("https://" + str(urlparse(host).netloc), str(result["id"]))
    output = '{0}{2}{1}{2}, '.format(output, str(result.get('fields').get('name')), BOLD)
    output = output + 'authored by {1}{0}{1}, '.format(author, BOLD)
    output = output + 'assigned to {1}{0}{1}, '.format(owner, BOLD)
    output = output + 'Priority: {1}{0}{1}, '.format(priority, BOLD)
    output = output + 'Status: {1}{0}{1}'.format(status, BOLD)
    return output


def dophabsearch(host, apikey, limit=True):
    """Performs a maniphest search."""
    data = {
        'api.token': apikey,
        'queryKey': querykey,
    }
    response = post(
        url='{0}/maniphest.search'.format(host),
        data=data)
    response = response.json()
    result = response.get("result")
    try:
        data = result.get("data")
    except Exception:
        return None
    x = 0
    searchphab = []
    while x < len(data):
        currdata = data[x]
        if x > 5 and limit:
            return  # fix
        else:
            searchphab.append(bot=bot, channel=channel, task=currdata.get("id"))
            x = x + 1
    return searchphab
