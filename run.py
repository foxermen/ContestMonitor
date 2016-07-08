#!/usr/local/bin/python
# coding=utf-8

from main import make_html

contests_b = (91, 94, 96)
contests_c = (92, 93, 95)

TITLE = u'Параллель %s'

make_html(contests=contests_b, title=(TITLE % 'B'), filename="./../stand_b.html")
make_html(contests=contests_c, title=(TITLE % 'C'), filename="./../stand_c.html")
