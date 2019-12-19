#!/usr/bin/env python3

# Update projects will retrieve new projects via a csv, and then update the markdown posts
# https://docs.google.com/spreadsheets/d/1FTnl8ucFKYtiS2xhNiK8VwXeE5BuBDCzL_k9SbqyG6A/edit#gid=1109363929
# requests is required
# Copyright @vsoch, 2019

import os
import csv
import requests
import shutil
import sys
import tempfile

here = os.path.dirname(os.path.abspath(__file__))

def get_filepath():
    '''load the counts file.
    '''
    filepath = os.path.join(os.path.dirname(here), '_data', 'projects.csv')

    # Exit on error if we cannot find file
    if not os.path.exists(filepath):
        print("Cannot find %s" % filepath)

    return filepath

def read_rows(filepath, newline='', delim=','):
    '''read in the data rows of a csv file.
    '''
    # Read in the entire membership counts
    with open(filepath, newline=newline) as infile:
        reader = csv.reader(infile, delimiter=delim)
        data = [row for row in reader]
    return data

    
def main():
    '''a small helper to update the _data/projectIdeas.csv file.
    '''
    # We will read through file, and update based on timestamp
    filepath = get_filepath()

    timestamps = set()
    with open(filepath, 'r') as filey:
        content = filey.read().split('\r\n')
        for entry in csv.reader(content[1:], quotechar='"', delimiter=',',
                               quoting=csv.QUOTE_ALL, skipinitialspace=True):
            timestamps.add(entry[0])

    # A csv download for just the worksheet with summary counts
    sheet = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4HHibR3dV9XAGiSHOQGQR91QsHescAHVEGLD5SKdvH9QYIzJJUKECEoegxIy1YNdIXxaiSVUBx143/pub?gid=1606129799&single=true&output=csv"
 
    # Ensure the response is okay
    response = requests.get(sheet)
    if response.status_code != 200:
        print('Error with getting sheet, response code %s: %s' %(response.status_code, response.reason))
        sys.exit(1)

    # Split lines by all sorts of fugly carriage returns
    lines = response.text.split('\r\n')

    # Timestamp, GitHub username, Challenge solving, description
    with open(filepath, 'a+') as filey:
        writer = csv.writer(filey, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_ALL)
        for line in csv.reader(lines[1:], quotechar='"', delimiter=',',
                               quoting=csv.QUOTE_ALL, skipinitialspace=True):
            timestamp = line[0]
            github_user = line[1]
            github_url = line[2]
            description = line[3]

            # If the timestamp isn't included, add it
            if timestamp not in timestamps:
                writer.writerow([timestamp, github_user, github_url, description])

if __name__ == '__main__':
    main()
