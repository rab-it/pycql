class Base():
    _default_keyspace = 'demodb'
    _placeholder = dict()
    _cql_commands = dict()

    def execute(self):
        string = Render().render(self)
        return string


class Table(Base):
    def __init__(self, table_name, keyspace=None):
        self.string = table_name + ': '
        keyspace = keyspace if keyspace is not None else self._default_keyspace
        self._placeholder['_TABLE_'] = keyspace + '.' + table_name
        self.Create = CreateTable


class Column(Base):

    def uuid(self, name):
        self._placeholder['_COLUMNDEF_'].update({name: 'uuid'})
        print(self._placeholder)

    def addColumn(self, *columns):
        print (columns)

        if columns:
            if '_COLUMNDEF_' not in self._placeholder:
                self._placeholder['_COLUMNDEF_'] = dict()

            if isinstance(columns[0], str) and len(columns) == 2:
                self._placeholder['_COLUMNDEF_'].update({columns[0]: columns[1]})
                print(self._placeholder)
            elif isinstance(columns[0], dict) and len(columns) == 1:
                self._placeholder['_COLUMNDEF_'].update(columns[0])
                print(self._placeholder)
            else:
                raise Exception("Invalid Column Definition")

        return self


class CreateTable():
    def __init__(self):
        self._cql_commands = {'_CREATE-TABLE_': 'CREATE TABLE %(_TABLE_)s ( [[_COLUMNDEF_]], ) ',
                              '_COLUMNDEF_': {}
                              }
        self.addColumn = Column().addColumn


class AlterTable():
    def __init__(self):
        self._cql_commands = {'_ALTER-TABLE_': 'ALTER TABLE %(_TABLE_)s'}


class Render():

    def validate(self):
        pass

    def render(self, obj):
        self.string = ''
        for k, v in obj._cql_commands.items():
            self.string += str(v)
        return self.string


if __name__ == '__main__':
    node = Table('user')
    node.execute()
    # .Create()
    # node.addColumn('uid', 'uuid')
    # node.addColumn({'uid': 'uuid', 'kdi': 'sdf'})
    # node.addColumn().uuid('mid')
    # node.

    print(node)

