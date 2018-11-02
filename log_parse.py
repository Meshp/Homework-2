# -*- encoding: utf-8 -*-
import re
from datetime import datetime
import time
from urllib.parse import urlparse


def check(line):
    r = re.match(
        r'\[(?P<date>\d+/\w+/\d+) (?P<time>\d+:\d+:\d+)\] \"(?P<request_type>\w+) (?P<url>[a-zA-Z0-9:\=\?\#\/\.]+) (?P<protocol>\w+/\d+\.\d+)\" (?P<response_code>\d+) (?P<response_time>\d+)',
        line)
    if r != None:
        return r.groupdict()

    return None


print(check('[21/Mar/2018 21:32:09] "GET https://sys.mail.ru/static/css/reset.css?asd= HTTPS/1.1" 200 1090'))


def Ignore_urls(line, ignore_urls):
    if line in ignore_urls:
        return True
    return False


def Start_at(data, start_at):
    if datetime.strptime(data, "%d/%b/%Y") > datetime.strptime(start_at, "%d/%b/%Y"):
        return True
    return False


def Stop_at(data, stop_at):
    if datetime.strptime(data, "%d/%b/%Y") < datetime.strptime(stop_at, "%d/%b/%Y"):
        return True
    return False


def Ignore_www(line):
    i = re.search('www.', line)
    if i != None:
        return line
    line = line.replace('www.', '', 1)
    return line


def Request_type(line, req):
    if line == req:
        return True
    return False


def Ignore_files(line):
    if '.' in line[line.rfind('/')::]:
        return False
    return True


def parse(
        ignore_files=False,
        ignore_urls=[],
        start_at=None,
        stop_at=None,
        request_type=None,
        ignore_www=False,
        slow_queries=False
):
    f = open('log.log', 'r')
    result = {}
    for line in f:
        d = check(line)
        if d == None:
            continue

        if start_at != None:
            if Start_at(d['date'], start_at) == False:
                continue

        if stop_at != None:
            if Stop_at(d['date'], stop_at) == False:
                break

        if ignore_www == True:
            d['url'] = Ignore_www(d['url'])

        o = urlparse(d['url'])
        url = o.netloc + o.path

        if ignore_urls != []:
            if Ignore_urls(url, ignore_urls) == True:
                continue

        if request_type != None:
            if Request_type(d['request_type'], request_type) == False:
                continue

        if ignore_files == True:
            if Ignore_files(o.path) == False:
                continue

        if url in result:
            result[url][0] += 1
            result[url][1] += int(d['response_time'])
        else:
            result[url] = [1, int(d['response_time'])]

    answer = []

    for key in result:
        if slow_querries == True:
            answer.append(result[url][1] / result[url][0])
        else:
            answer.append(result[url][0])

    answer.sort()
    return answer[-1:-6:-1]

