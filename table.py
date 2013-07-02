__author__ = 'rabit'

import re


class Table():
    def __init__(self, keyspace=None):
        self._queries = {
            '_CREATE-TABLE_': 'CREATE TABLE %(_KEYSPACE_)s.%(_TABLE_)s ( [[_COLUMNDEF_|, ]], '
                              'PRIMARY KEY (%(_PRIMARYKEY_)s) )'
                              # 'WITH [[_PROPERTIES_|_OP_]]'
        }
        self._placeholder = dict([('_KEYSPACE_', keyspace)])
        self._options = dict([('_CASE-SENSITIVE_', False)])
        self._query = ''

    def create(self, table_name):
        self._query = '_CREATE-TABLE_'
        self._placeholder['_TABLE_'] = table_name

        return self

    def addColumn(self, colname_values):
        if '_COLUMNDEF_' not in self._placeholder:
            self._placeholder['_COLUMNDEF_'] = dict()
        self._placeholder['_COLUMNDEF_'].update(colname_values)
        # print self._placeholder, colname_values

        return self

    def primaryKey(self, key):
        if isinstance(key, str):
            key = key
        elif isinstance(key, tuple):
            key = ', '.join(key)

        self._placeholder['_PRIMARYKEY_'] = key
        return self

    def options(self, options):
        self._options = options
        return self

    def render(self):
        case_sensitive = self._options['_CASE-SENSITIVE_']
        pattern_loop_holder = r'\[\[_[A-Z-]*_\|.*?\]\]'

        for key, value in self._placeholder.items():
            if not case_sensitive:
                if isinstance(value, str):
                    self._placeholder[key] = value.lower()
                elif isinstance(value, dict):
                    for dict_key, dict_value in self._placeholder[key].items():
                        self._placeholder[key].pop(dict_key)
                        self._placeholder[key].update({dict_key.lower(): dict_value.lower()})

        placeholders = re.findall(pattern_loop_holder, self._queries[self._query])

        for item in placeholders:
            # print(item)
            pattern_item = r'\[\[(_[A-Z-]*_)\|(.*?)\]\]'
            match = re.match(pattern_item, item).groups()

            if match[0] in self._placeholder:
                column_defs = self._placeholder[match[0]]
                self._placeholder[match[0]] = match[1].join(['%s %s' % (key, value) for (key, value) in column_defs.items()])

        pattern_placeholder_name = r'\[\[(_[A-Z-]*_)\|.*?\]\]'
        self._queries[self._query] = re.sub(pattern_placeholder_name, r'%(\1)s', self._queries[self._query])

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