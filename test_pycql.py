import connection
import table
#
# def setup_func():
#     connection.setup(['localhost:9160:quantweb', 'localhost:9145:quantweb'])
#     execute_obj = connection.execute("INSERT INTO songs (id, title)VALUES (62c36092-82a1-3a00-93d1-46196ee77211, 'Come away');")
#     return True if execute_obj else False
#
# def test_setup():
#     assert setup_func() == True


connection.setup(['localhost:9160:quantweb', 'localhost:9145:quantweb'])


def select(*columns):
    columns = list(columns)

    columns_names = ', '.join(columns)
    execute_obj = connection.execute("SELECT " + columns_names + " FROM songs")

    # pycql = connect()
    # pycql.execute("SELECT " + columns_names + " FROM songs")

    return execute_obj.fetchall()
print select('title')








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



