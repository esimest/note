# -*- coding: utf-8 -*-
"""字典相关操作"""


def dict_create():
    d1 = {'name': 'json', 'age': 20, 'gender': 'male'}
    breakpoint()
    d2 = dict([('name', 'json'), ('age', 20), ('gender', 'male')])
    d3 = dict(zip(['name', 'age', 'gender'], ['json', 20, 'male']))
    d4 = dict({'name': 'json', 'age': 20, 'gender': 'male'})
    d = dict(name='json', age=20, gender='male')
    return d1 == d2 == d3 == d4 == d


def dict_update():
    d = {'name': 'json', 'age': 20}
    d['gender'] = 'male'
    d['dob'] = '1995-09-28'
    d['dob'] = '1996-02-17'
    d.pop('dob')
    d.update({'dob': '1996-02-17'})
    d.pop()


if __name__ == '__main__':
    breakpoint()
    dict_update()
