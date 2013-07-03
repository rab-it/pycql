class Base():
    _default_keyspace = 'demodb'
    _placeholder = dict()
    _cql_commands = dict()

    def execute(self):
        string = Render().render(self)
        return string


class Table(Base):
    def __init__(self, table_name, keyspace=None):
        keyspace = keyspace if keyspace is not None else self._default_keyspace
        self._placeholder['_TABLE_'] = keyspace + '.' + table_name
        self.Create = CreateTable


class CreateTable(Base):
    def __init__(self):
        self._cql_commands = {'_CREATE-TABLE_': 'CREATE TABLE %(_TABLE_)s ( [[_COLUMNDEF_]], ) ',
                              '_COLUMNDEF_': {}
                              }
        self.addColumn = Column().addColumn
        self.setPrimaryKey = Column().setPrimaryKey


class AlterTable(Base):
    def __init__(self):
        self._cql_commands = {'_ALTER-TABLE_': 'ALTER TABLE %(_TABLE_)s'}


class TableOptions(Base):
    pass


class Column(Base):

    def __setPlaceholderKey(self, key, value_type):
        if key not in self._placeholder or not self._placeholder[key]:
            # if provided key is not available or if the value is empty
            self._placeholder[key] = value_type

    def __setCqlType(self, name, cql_type, collection=None):
        """
        Type function to set cql data type of Columns

        :param name: String
        :param cql_type: String (general) or Tuple (if collection == 'map')
        :param collection: 'set' | 'list'
        """
        self.__setPlaceholderKey('_COLUMNDEF_', dict())

        if collection in ('set', 'list'):
            cql_type = str(collection) + '<' + str(cql_type) + '>'
        elif collection == 'map' and isinstance(cql_type, tuple):
            cql_type = collection + '<' + ', '.join(cql_type) + '>'

        self._placeholder['_COLUMNDEF_'].update({name: cql_type})

    def type_ascii(self, name, collection=None):
        self.__setCqlType(name, 'ascii', collection)

    def type_bigint(self, name, collection=None):
        self.__setCqlType(name, 'bigint', collection)

    def type_blob(self, name, collection=None):
        self.__setCqlType(name, 'blob', collection)

    def type_boolean(self, name, collection=None):
        self.__setCqlType(name, 'boolean', collection)

    def type_counter(self, name, collection=None):
        self.__setCqlType(name, 'counter', collection)

    def type_decimal(self, name, collection=None):
        self.__setCqlType(name, 'decimal', collection)

    def type_double(self, name, collection=None):
        self.__setCqlType(name, 'double', collection)

    def type_float(self, name, collection=None):
        self.__setCqlType(name, 'float', collection)

    def type_inet(self, name, collection=None):
        self.__setCqlType(name, 'inet', collection)

    def type_int(self, name, collection=None):
        self.__setCqlType(name, 'int', collection)

    def type_text(self, name, collection=None):
        self.__setCqlType(name, 'text', collection)

    def type_timestamp(self, name, collection=None):
        self.__setCqlType(name, 'timestamp', collection)

    def type_uuid(self, name, collection=None):
        self.__setCqlType(name, 'uuid', collection)

    def type_timeuuid(self, name, collection=None):
        self.__setCqlType(name, 'timeuuid', collection)

    def type_varchar(self, name, collection=None):
        self.__setCqlType(name, 'varchar', collection)

    def type_varint(self, name, collection=None):
        self.__setCqlType(name, 'varint', collection)

    # Method for set, list and map
    def type_list(self, name, cql_type):
        self.__setCqlType(name, cql_type, 'list')

    def type_set(self, name, cql_type):
        self.__setCqlType(name, cql_type, 'set')

    def type_map(self, name, cql_type):
        self.__setCqlType(name, cql_type, 'map')

    def addColumn(self, *columns):
        """
        Add columns to dictionary. All key and values will be rendered when execute is called.

        :param columns:
        :return: :raise:
        """
        if columns:
            self.__setPlaceholderKey('_COLUMNDEF_', dict())

            if isinstance(columns[0], str) and len(columns) == 2:
                self._placeholder['_COLUMNDEF_'].update({columns[0]: columns[1]})
                # print(self._placeholder)
            elif isinstance(columns[0], dict) and len(columns) == 1:
                self._placeholder['_COLUMNDEF_'].update(columns[0])
                # print(self._placeholder)
            else:
                raise Exception("Invalid Column Definition")

        return self

    def alterColumn(self):
        # Todo
        pass

    def delColumn(self):
        # Todo
        pass

    def setPrimaryKey(self, *keys):
        self._placeholder['_PRIMARY-KEY_'] = dict()

        first = True

        for key in keys:
            if first:
                first = False
                if isinstance(key, tuple):
                    self._placeholder['_PRIMARY-KEY_']['composite'] = [item for item in key]
                elif isinstance(key, str):
                    self._placeholder['_PRIMARY-KEY_']['composite'] = key
                else:
                    raise Exception("Invalid Primary Key")
            else:
                if 'compound' not in self._placeholder['_PRIMARY-KEY_'] or not self._placeholder['_PRIMARY-KEY_']['compound']:
                    self._placeholder['_PRIMARY-KEY_']['compound'] = list()
                self._placeholder['_PRIMARY-KEY_']['compound'].append(key)


class Render():

    def validate(self):
        pass

    def render(self, obj):
        self.string = ''
        for k, v in obj._cql_commands.items():
            self.string += str(v)
        return self.string


if __name__ == '__main__':
    node = Table('user').Create()
    node.addColumn('uid', 'uuid')
    node.addColumn({'uid': 'uuid', 'kdi': 'sdf'})
    node.addColumn().type_ascii('char')
    node.addColumn().type_boolean('gender')
    node.addColumn().type_varchar('name')
    # node.addColumn().timestamp('mdk')
    node.execute()

    print(node._placeholder)

