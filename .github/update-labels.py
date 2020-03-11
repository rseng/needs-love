#!/usr/bin/env python3

# Update projects will retrieve new projects via a csv, and then update the markdown posts
# https://docs.google.com/spreadsheets/d/1FTnl8ucFKYtiS2xhNiK8VwXeE5BuBDCzL_k9SbqyG6A/edit#gid=1109363929
# requests is required
# Copyright @vsoch, 2019

import os
import csv
import json
import requests
import sys

    
def main():
    '''Determine the labels added or removed. If needs-love is added,
       make sure to removed matched and vice versa.
    '''
    payload = os.environ.get("GITHUB_EVENT_PATH", "")
    if not os.path.exists(payload):
        sys.exit("Cannot find %s" % payload)

    with open(payload, 'r') as fd:
        payload = json.loads(fd.read())

    # We will need the issue URL to update
    issue_url = "%s/labels" % payload.get('issue')['url']

    # Headers must include token
    headers = {"Authorization": "Bearer %s" % token}

    # get token from environment
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("Token is required to update labels.")

    # Create variables for label added or removed, and action
    action = payload.get('action')
    labels = set(["matched", "needs-love"])
    label = payload.get('label')
    labels.remove(label)
    other_label = list(labels)[0]

    print("Found label %s" % label)
    response = None
    if action == 'labeled':
        print("%s was added, removing %s" %(label, other_label))
        data = {"labels": [other_label]}
        response = requests.delete(issue_url, headers=headers, json=data)

    elif action == "unlabeled":
        print("%s was removed, adding %s" %(label, other_label))
        data = {"labels": [other_label]}
        response = requests.post(issue_url, headers=headers, json=data)

    # 404 is allowed if someone already removed
    if response:
        if response.status_code not in [200, 201, 404]:
            sys.exit("Issue with creating or removing issue labels.")

if __name__ == '__main__':
    main()
