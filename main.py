import lxml.html as html

MATCH_URL = "http://contest.stavpoisk.ru/olympiad/%s/show-monitor"


def get_tasks(head):
    tasks = head.find_class('task')
    result = [t.text_content().strip() for t in tasks]
    return result


def get_user_info(user):
    name = user.find_class('user')[0].text_content().strip()
    tasks = user.find_class('task')
    result = []
    for task in tasks:
        text = task.getchildren()[0].text_content().strip()
        if text.find('\n') != -1:
            text = text[:text.find('\n')]
        result.append(text)
    return name, result


def get_users_from_contest(num):
    result = {'head': {}, }
    page = html.parse(MATCH_URL % num)
    title = page.getroot().find_class('page-title')[0].text_content()
    title = title[:title.find('\n')]
    result['head']['title'] = title

    table = page.getroot().find_class('acm-monitor')[0].getchildren()

    head = table[0]
    result['head']['problems'] = get_tasks(head=head)

    body = table[1]
    for children in body.getchildren():
        name, info = get_user_info(user=children)
        result[name] = info

    return result


def make_html(contests, title):
    users = {}
    for contest in contests:
        result = get_users_from_contest(contest)
        for key in result.keys():
            if key not in users.keys():
                users[key] = {}
            users[key][contest] = result[key]
