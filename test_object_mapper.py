__author__ = 'rabit'

import object_mapper


def test_table():
    user = object_mapper.Table('user').Create()
    assert str(user)[:44] == '<pycql.object_mapper.CreateTable instance at'
