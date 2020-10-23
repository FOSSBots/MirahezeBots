from json import JSONDecodeError
from urllib.parse import urlparse

import requests


BOLD = '\x02'


def searchphab(PHAB_SETTINGS, task=1):
    host = PHAB_SETTINGS["phab-active-url"]
    apikey = PHAB_SETTINGS["phab-active-api_token"]

    data = {
        'api.token': apikey,
        'constraints[ids][0]': task
    }
    response = requests.post(
        url='{0}/maniphest.search'.format(host),
        data=data)
    response = response.json()
    go = 0
    try:
        result = response.get("result").get("data")[0]
        go = 1
    except AttributeError:
        return "An error occurred while parsing the result."
    except IndexError:
        return "Sorry, but I couldn't find information for the task you searched."
    except Exception:
        raise Exception("An unknown error occured.")
    if go == 1:
        params = {
            'api.token': apikey,
            'constraints[phids][0]': result.get("fields").get("ownerPHID")
        }
        response2 = requests.post(
            url='{0}/user.search'.format(host),
            data=params)
        try:
            response2 = response2.json()
        except JSONDecodeError as e:
            raise Exception("Encountered {} on: {}").format(str(e), response2.text)
        params2 = {
            'api.token': apikey,
            'constraints[phids][0]': result.get("fields").get("authorPHID")
        }
        response3 = requests.post(
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


def dophabsearch(PHAB_SETTINGS, limit=True, querykey='open'):
    host = PHAB_SETTINGS["phab-active-url"]
    apikey = PHAB_SETTINGS["phab-active-api_token"]
    data = {
        'api.token': apikey,
        'queryKey': querykey,
    }
    response = requests.post(
        url='{0}/maniphest.search'.format(host),
        data=data)
    response = response.json()
    result = response.get("result")
    try:
        data = result.get("data")
        go = 1
    except Exception:
        return "There are no tasks matching your search that I can process, good job!"
        go = 0
    if go == 1:
        x = 0
        result = []
        while x < len(data):
            currdata = data[x]
            if x > 5 and limit:
                return "They are more than 5 tasks. Please see {0} for the rest or use .highpri".format(host)
                break
            else:
                result.append(searchphab(PHAB_SETTINGS, task=currdata.get("id")))
                x = x + 1
        return result
