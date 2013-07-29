__author__ = 'rabit'

import manager
import connection

# excelsior = manager.Table('emp').drop()
excelsior = manager.Table('emp').create()
excelsior.addColumn({"empid": 'int', 'deptid': 'int'})
excelsior.setPrimaryKey('empid')
rendered = excelsior.execute()

# rendered = "DROP TABLE emp"
# connection.setup(['localhost:9160:demodb'])
# connection.execute(rendered)
