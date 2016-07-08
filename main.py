# coding=utf-8

import lxml.html as html
import os
from jinja2 import FileSystemLoader, Environment

MATCH_URL = "http://contest.stavpoisk.ru/olympiad/%s/show-monitor"


def get_tasks(head):
    tasks = head.find_class('task')
    result = [t.text.strip() for t in tasks]
    return result


def get_user_info(user):
    if len(user.find_class('user')) == 0:
        return 0, 0
    name = user.find_class('user')[0].text.strip()
    tasks = user.find_class('task')
    result = []
    for task in tasks:
        text = task.getchildren()[0].text.strip()
        if text.find('\n') != -1:
            text = text[:text.find('\n')]
        result.append(text)
    return name, result


def get_users_from_contest(num):
    result = {'head': {}, }
    page = html.parse(MATCH_URL % num)
    title = page.getroot().find_class('page-title')[0].text
    title = title[:title.find('\n')]
    result['head']['title'] = title

    table = page.getroot().find_class('acm-monitor')[0].getchildren()

    head = table[0]
    result['head']['problems'] = get_tasks(head=head)

    body = table[1]
    for children in body.getchildren():
        name, info = get_user_info(user=children)
        if name != 0:
            result[name] = info

    return result


def get_accepted_and_se(data):
    accepted = 0
    se = 0
    for contest in data.keys():
        for status in data[contest]:
            if status[0] == '+':
                accepted += 1
                if len(status) > 1:
                    se += int(status[1:])
    return accepted, se


def get_user_ac_and_se(users):
    result = []
    for name in users.keys():
        if name != 'head':
            accepted, se = get_accepted_and_se(data=users[name])
            result.append((name, accepted, se))
    result.sort(key=lambda x: (-x[1], x[2], x[0]))
    return result


def get_titles(data, contests):
    result = []
    for contest in contests:
        result.append({'title': data[contest]['title'],
                       'count': len(data[contest]['problems']), })
    return result


def get_problems(data, contests):
    result = []
    for contest in contests:
        for s in data[contest]['problems']:
            result.append(s)
    return result


def make_html(contests, title, filename):
    users = {}
    for contest in contests:
        result = get_users_from_contest(contest)
        for key in result.keys():
            if key not in users.keys():
                users[key] = {}
            users[key][contest] = result[key]

    user_list = get_user_ac_and_se(users=users)

    loader = FileSystemLoader(os.path.abspath(os.curdir))
    env = Environment(loader=loader)
    template = env.get_template('template.html')

    titles = get_titles(data=users['head'], contests=contests)
    problems = get_problems(data=users['head'], contests=contests)

    lst = []
    i = 1
    for user in user_list:
        user_dict = {'num': i,
                     'name': user[0],
                     'accepted': user[1],
                     'se': user[2],
                     'problems': [], }
        for contest in contests:
            if contest in users[user[0]]:
                for problem in users[user[0]][contest]:
                    if problem == '.':
                        user_dict['problems'].append({'color': '#FFFFFF',
                                                      'text': '', })
                    elif problem[0] == '+':
                        user_dict['problems'].append({'color': '#90FF77',
                                                      'text': problem, })
                    else:
                        user_dict['problems'].append({'color': '#DD290E',
                                                      'text': problem, })
            else:
                for _ in users['head'][contest]['problems']:
                    user_dict['problems'].append({'color': 'FFFFFF',
                                                  'text': '', })

        lst.append(user_dict)
        i += 1

    with open(filename, 'w') as f:
        f.write(template.render({'title': title,
                                 'titles': titles,
                                 'problems': problems,
                                 'users': lst, }).encode('utf8'))
