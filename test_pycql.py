__author__ = 'rabit'


import connect
import table

'''
def test_select():
    assert connect.select('gender', 'user_name') == [u'male', u'bapon']
    assert connect.select('gender', 'user_name') != [u'female', u'bapon']


def test_add():
    assert connect.add(5,6) == 11
    assert connect.add(50,25) == 75
    assert connect.add(-50,25) == -25
'''


def test_table():

    node = table.Table('demo')
    node.create('Node')
    node.addColumn('nid', 'uuid')
    node.addColumn('title', 'varchar')
    node.addColumn('body', 'varchar')
    node.primaryKey('nid')
    node = node.execute()

    assert node == 'CREATE TABLE demo.node ( nid uuid, title varchar, body varchar, PRIMARY KEY (nid));'