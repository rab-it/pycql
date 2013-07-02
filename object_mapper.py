class Base():
    _default_keyspace = 'demodb'
    _placeholder = dict()
    _cql_commands = dict()


class Table(Base):
    def __init__(self, table_name, keyspace=None):
        self.string = table_name + ': '
        keyspace = keyspace if keyspace is not None else self._default_keyspace
        self._placeholder['_TABLE_'] = keyspace + '.' + table_name
        self.Create = CreateTable


class __ColumnProperties(Base):

    def addColumn(self):
        self.string = 'node'
        self.string += " column added"
        return self

    def renameColumn(self):
        self.string += " column renamed"
        return self

    def execute(self):
        string = Render().render(self)
        return string


class CreateTable(__ColumnProperties):
    def __init__(self):
        self._cql_commands = {'_CREATE-TABLE_': 'CREATE TABLE %(_TABLE_)s ( [[_COLUMNDEF_]], ) ',
                              '_COLUMNDEF_': {}
                              }


class AlterTable(__ColumnProperties):
    def __init__(self):
        self._cql_commands = {'_ALTER-TABLE_': 'ALTER TABLE %(_TABLE_)s'}


class Render():
    def render(self, obj):
        self.string = ''
        for k, v in obj._cql_commands.items():
            self.string += str(v)
        return self.string


if __name__ == '__main__':
    node = Table('user').Create()
    # node.addColumn('uid', 'uuid')

    print(node)

