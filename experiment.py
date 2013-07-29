__author__ = 'rabit'

import manager
import query
import connection


from cassandra.io.libevreactor import LibevConnection
from cassandra.cluster import Cluster

cluster = Cluster()
cluster.connection_class = LibevConnection
session = cluster.connect()


# excelsior = manager.Table('emp').drop()
# excelsior = manager.Table('emp').create()
# excelsior.addColumn({"empid": 'int', 'deptid': 'int'})
# excelsior.setPrimaryKey('empid')
# rendered = excelsior.execute()

data = {'empid': 104,
        'deptid': 15}
# query = query.Query('emp').insert(data)
query = query.Query('emp').select()
rendered = query.execute(False)

for i in rendered:
    print(i)

# rendered = "DROP TABLE emp"
# connection.setup(['localhost:9160:demodb'])
# connection.execute(rendered)
