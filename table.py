__author__ = 'rabit'

from string import Template


class Table():
    def __init__(self, keyspace=None, case_sensitive=False):
        self._queries = {
            '_CREATE-TABLE_': 'CREATE TABLE {{_KEYSPACE_}}.{{_TABLE_}} ( [[_COLUMNDEF_|, ]] ) '
                              'WITH [[_PROPERTIES_|_OP_]]'
        }
        self._placeholder = dict([('_KEYSPACE_', keyspace)])
        self._options = dict([('_CASE-SENSITIVE_', case_sensitive)])
        self._query = ''

    def create(self, table_name):
        self._query = '_CREATE-TABLE_'
        self._placeholder['_TABLE_'] = table_name if self._options['_CASE-SENSITIVE_'] else table_name.lower()

        return self

    def addColumn(self, column_name, column_type):
        self._query = self._query + column_name + ' ' + column_type + ', '
        return self

    def primaryKey(self, key):
        self._query = self._query + 'PRIMARY KEY (' + key + ')'
        print self._query
        return self

    def render(self):
        render = ''
        print(self._placeholder)
        for placeholder, value in self._placeholder.items():
            render = self._queries[self._query].replace('{{' + placeholder + '}}', value)

        self._render = render
        return self

    def execute(self):
        self.render()
        # TODO: close conn

        return self._render


if __name__ == '__main__':
    node = Table('demo')
    node.create('Node')
    # node.addColumn('nid', 'uuid')
    # node.addColumn('title', 'varchar')
    # node.addColumn('body', 'varchar')
    # node.primaryKey('nid')
    node.execute()