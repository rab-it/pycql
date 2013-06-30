__author__ = 'rabit'

import connection
import table

def setup_func():
    connection.setup(['localhost:9160:quantweb', 'localhost:9145:quantweb'])
    execute_obj = connection.execute("INSERT INTO songs (id, title)VALUES (62c36092-82a1-3a00-93d1-46196ee77211, 'Come away');")
    return True if execute_obj else False


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
    node.addColumn({'nid': 'uuid'})
    node.addColumn({'title': 'varchar'})
    node.addColumn({'body': 'varchar'})
    node.primaryKey('nid')
    node = node.execute()

    assert node == 'CREATE TABLE demo.node ( body varchar, nid uuid, title varchar, PRIMARY KEY (nid) )'

    columns = dict([('UID', 'uuid'), ('username', 'VARCHAR'), ('Email', 'varchar')])
    user = table.Table('TEST')
    user.create('USERS')
    user.addColumn(columns)
    user.addColumn({'Reg': 'varchar'})
    user.primaryKey(('Username', 'Reg'))
    user = user.execute()

    assert user == 'CREATE TABLE test.users ( username varchar, uid uuid, reg varchar, email varchar, ' \
                   'PRIMARY KEY (username, reg) )'

    columns = dict([('UID', 'uuid'), ('username', 'VARCHAR'), ('Email', 'varchar')])

    user = table.Table('TEST')
    user.create('USERS')
    user.addColumn(columns)
    user.addColumn({'Reg': 'varchar'})
    user.primaryKey(('username', 'Reg'))
    user.options({'_CASE-SENSITIVE_': True})
    user = user.execute()

    assert user == 'CREATE TABLE TEST.USERS ( username VARCHAR, Reg varchar, UID uuid, Email varchar, ' \
                   'PRIMARY KEY (username, Reg) )'

def test_setup():
    assert setup_func() == True