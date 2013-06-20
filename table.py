__author__ = 'rabit'

import re


class Table():
    def __init__(self, keyspace=None, case_sensitive=False):
        self._queries = {
            '_CREATE-TABLE_': 'CREATE TABLE %(_KEYSPACE_)s.%(_TABLE_)s ( [[_COLUMNDEF_|, ]], '
                              'PRIMARY KEY (%(_PRIMARYKEY_)s) )'
                              # 'WITH [[_PROPERTIES_|_OP_]]'
        }
        self._placeholder = dict([('_KEYSPACE_', keyspace)])
        self._options = dict([('_CASE-SENSITIVE_', case_sensitive)])
        self._query = ''

    def create(self, table_name):
        self._query = '_CREATE-TABLE_'
        self._placeholder['_TABLE_'] = table_name if self._options['_CASE-SENSITIVE_'] else table_name.lower()

        return self

    def addColumn(self, colname_values):
        if '_COLUMNDEF_' not in self._placeholder:
            self._placeholder['_COLUMNDEF_'] = dict()
        self._placeholder['_COLUMNDEF_'].update(colname_values)
        # print self._placeholder, colname_values

        return self

    def primaryKey(self, key):
        self._placeholder['_PRIMARYKEY_'] = key
        print key
        return self

    def render(self):

        pattern = r'\[\[_[A-Z-]*_\|.*?\]\]'

        placeholders = re.findall(pattern, self._queries[self._query])
        print placeholders

        for item in placeholders:
            # print(item)
            pattern2 = r'\[\[(_[A-Z-]*_)\|(.*?)\]\]'
            match = re.match(pattern2, item).groups()

            if match[0] in self._placeholder:
                column_defs = self._placeholder[match[0]]
                self._placeholder[match[0]] = match[1].join(['%s %s' % (key, value) for (key, value) in column_defs.items()])

        pattern3 = r'\[\[(_[A-Z-]*_)\|.*?\]\]'
        self._queries[self._query] = re.sub(pattern3, r'%(\1)s', self._queries[self._query])

        render = self._queries[self._query] % self._placeholder

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