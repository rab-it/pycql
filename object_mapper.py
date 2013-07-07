import re


class Base():
    _default_keyspace = 'demodb'
    _placeholder = dict()
    _cql_commands = dict()
    _main_query = ''

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
        """
        _cql_commands is a dictionary containing Lexical structures of cql commands.
        <_VAR_> Means required lookups. [CONST <_VAR_>] means optional lookups

        """

        self._cql_commands = {'_CREATE-TABLE_': 'CREATE TABLE %(_TABLE_)s ( %(<_COLUMNDEF_>)s, '
                                                '%(<_PRIMARY-KEY_>)s )',
                              }

        self._main_query = '_CREATE-TABLE_'

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
        elif collection is True:
            self.setPrimaryKey(name)
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
            elif isinstance(columns[0], str) and columns[2] is True:
                self._placeholder['_COLUMNDEF_'].update({columns[0]: columns[1]})
                self.setPrimaryKey(columns[0])
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
                if 'clustering' not in self._placeholder['_PRIMARY-KEY_'] or not self._placeholder['_PRIMARY-KEY_']['clustering']:
                    self._placeholder['_PRIMARY-KEY_']['clustering'] = list()
                self._placeholder['_PRIMARY-KEY_']['clustering'].append(key)


class Render():

    def validate(self):
        pass

    def _placeholders(self):

        functions = {'_TABLE_': self._placeholder['_TABLE_'],
                     '_COLUMNDEF_': self.__renderColumndef(),
                     '_PRIMARY-KEY_': self.__renderPK()
                     }

        return functions

    def __renderColumndef(self):
        if self._placeholder['_COLUMNDEF_']:
            return ', '.join(['%s %s' % (key, value) for (key, value) in self._placeholder['_COLUMNDEF_'].items()])

    def __validatePK(self):
        if 'composite' in self._placeholder['_PRIMARY-KEY_']:
            pk_dict = self._placeholder['_PRIMARY-KEY_']
            for pk_type in pk_dict:
                if isinstance(pk_dict[pk_type], list):
                    for pk in pk_dict[pk_type]:
                        if not pk in self._placeholder['_COLUMNDEF_']:
                            raise Exception('{} key {} is not a column'.format(pk_type.title(), pk))
                else:
                    if not pk_dict[pk_type] in self._placeholder['_COLUMNDEF_']:
                        raise Exception('{} key {} is not a column'.format(pk_type.title(), pk_dict[pk_type]))

        else:
            raise Exception('Primary key is required')

    def __renderPK(self):

        self.__validatePK()

        pk_dict = self._placeholder['_PRIMARY-KEY_']

        pk = 'PRIMARY KEY ('

        if isinstance(pk_dict['composite'], list):
            pk += '(' + ', '.join(pk_dict['composite']) + ')'
        else:
            pk += pk_dict['composite']

        if 'clustering' in pk_dict:
            pk += ', ' + ', '.join(pk_dict['clustering'])

        pk += ')'

        return pk

    def render(self, obj):

        self._placeholder = obj._placeholder
        self._cql_commands = obj._cql_commands
        self._main_query = obj._main_query

        pattern_query_placeholder = r'<(_[A-Z-]*?_)>'

        query_with_placeholders = re.sub(pattern_query_placeholder, r'\1', self._cql_commands[self._main_query])
        print(query_with_placeholders)

        render = query_with_placeholders % self._placeholders()
        print (render)
        return render


if __name__ == '__main__':
    user = Table('user').Create()
    user.addColumn('uid', 'uuid')

    user.addColumn({'uid': 'uuid', 'email': 'text'})

    user.addColumn().type_ascii('char')

    user.addColumn().type_varchar('username')

    user.addColumn().type_text('email', 'set')

    user.addColumn().type_list('fav_post', 'varchar')

    user.addColumn().type_map('todo', ('timestamp', 'text'))

    user.addColumn({'name': 'varchar', 'email': 'text'})
    user.addColumn().type_uuid('uid')
    user.setPrimaryKey('uid')

    user.addColumn({'name': 'varchar', 'email': 'text', 'phone': 'text'})
    user.addColumn().type_uuid('uid')
    user.setPrimaryKey('uid', 'email')

    user.setPrimaryKey('uid', 'email', 'phone')

    user.setPrimaryKey(('uid', 'email'), 'username', 'phone')

    user.execute()

    # print(user._placeholder)
