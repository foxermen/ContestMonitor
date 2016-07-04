#!/usr/local/bin/python
# coding=utf-8

from main import make_html

contests_b = (60, 63, 64, 67, 68, 71, 74, 76, 78, 79, 82, 83)

TITLE = u'Сводная таблица ЛКШ 2016 Параллель %s'

make_html(contests=contests_b, title=(TITLE % 'B'), filename="stand_b.html")
