import requests
from bs4 import BeautifulSoup
import argparse
import re
import os
from git import Repo
import git
from github import Github
import sys
import pygit2

def CreateSearchURL(searchWord, page, sortBy, language):
    url = ''.join(list(
        ['''https://github.com/search?o=desc&p=''', str(page), '&q=', searchWord, '&s=', sortTypes[sortBy],
         '&type=Repositories', f'&l={language}']))
    return url

def init_remote(repo, name, url):
    # Create the remote with a mirroring url
    remote = repo.remotes.create(name, url, "+refs/*:refs/*")
    # And set the configuration option to true for the push command
    mirror_var = "remote.{}.mirror".format(name)
    repo.config[mirror_var] = True
    # Return the remote, which pygit2 will use to perform the clone
    return remote

parser = argparse.ArgumentParser(description="Download Github repos")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--url", type=str, help="Enter the URL")
group.add_argument('--search', type=str, help='Enter the search term')
parser.add_argument('--sortby', type=str, help='Sort By: best, stars, forks, date', default='star', required=False)
parser.add_argument("-n", type=int, help="Number of top repos", default=1, required=False)
parser.add_argument('-l', type=str, help='Language to search for: \neg. jupyter, python, c++, c', default='',
                    required=False)

args = parser.parse_args()
URL = args.url
SEARCH_TERM = args.search
SORT_BY = args.sortby
COUNT_REPOS = args.n
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

sortTypes = {'star': 'stars', 'best': '', 'fork': 'forks', 'date': 'updated'}
languages = {'jupyter': 'jupyter+notebook', 'python': 'python', 'c++': 'C%2B%2B', 'c': 'c', '': ''}
g = Github(ACCESS_TOKEN)

print("Downloading address's HTML...")

if not URL == None:
    searchKeyWord = URL.split('&q=')[1].split('&')[0]
    results=g.search_repositories(searchKeyWord,sortTypes[SORT_BY],'desc')
elif not SEARCH_TERM == None:
    searchKeyWord = '+'.join(query.strip() for query in SEARCH_TERM.split(','))
    results=g.search_repositories(searchKeyWord,sortTypes[SORT_BY],'desc')

count=1
for result in results:
    rate_limit = g.get_rate_limit()
    rate = rate_limit.search
    if rate.remaining == 0:
        print(f'You have 0/{rate.limit} API calls remaining. Reset time: {rate.reset}')
        continue
    else:
        print(f'You have {rate.remaining}/{rate.limit} API calls remaining')

    if count>COUNT_REPOS:
        break
    try:
        title = str(result.clone_url.split('/')[-1].split('.')[0]).strip('/')

        print("*" * 50)
        print(f"Processing ... {count}/{COUNT_REPOS}\nPaper Title: {title} ")
        print("*" * 50)
        path = os.getcwd()
        path = os.path.join(path, f"{count} _ " + title)
        if not os.path.exists(path):
            os.mkdir(path)

        with open(os.path.join(path, "ReadMe.txt"), "w+") as file:
            file.write(path + "\n")
        url = result.clone_url.split('.gi')[0]
        pygit2.clone_repository(url, title, bare=True, remote=init_remote)
        print(f'Succesfully cloned [{title}] : {count}/{COUNT_REPOS}')
        count += 1
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        count += 1
