__author__ = 'rabit'

from render import RenderManagers


class Table(object):
    def __init__(self, table_name, keyspace=None):

        __default_keyspace = 'demodb'
        self._placeholder = dict()

        # keyspace = keyspace if keyspace is not None else __default_keyspace
        # self._placeholder['_TABLE_'] = keyspace + '.' + table_name

        self._placeholder['_TABLE_'] = keyspace + '.' + table_name if keyspace else table_name
        self._query = ''

    def create(self):
        return CreateTable(self)

    def alter(self):
        return AlterTable(self)

    def drop(self):
        return DropTable(self)

    def execute(self):
        string = RenderManagers().render(self)
        return string


class CreateTable(Table):

    def __init__(self, obj):
        """
        _cql_commands is a dictionary containing Lexical structures of cql commands.
        <_VAR_> Means required lookups. [CONST <_VAR_>] means optional lookups

        """
        self._placeholder = obj._placeholder
        self._main_query = 'CREATE TABLE %(_TABLE_)s ( %(_COLUMNDEF_)s, %(_PRIMARY-KEY_)s ) %(_OPTIONS_)s'

        self.addColumn = CreateColumn(self).addColumn
        self.setPrimaryKey = CreateColumn(self).setPrimaryKey
        self.options = TableOptions(self).setOptions


class DropTable(Table):
    def __init__(self, obj):
        self._placeholder = obj._placeholder
        self._main_query = 'DROP TABLE %(_TABLE_)s'


class TableOptions(object):
    def __init__(self, obj):
        self._main_query = obj._main_query
        self._placeholder = obj._placeholder
        self.optionsList = ('compression', 'compaction', 'compact', 'bloom_filter_fp_chance', 'caching', 'comment',
                       'dclocal_read_repair_chance', 'gc_grace_seconds', 'read_repair_chance', 'replicate_on_write')

    def setOptions(self, *args, **kwargs):
        if args and isinstance(args[0], dict):
            for k, v in args[0].items():
                if k not in self.optionsList:
                    raise Exception('Invalid option')
        elif kwargs:
            for k, v in kwargs.items():
                if k not in self.optionsList:
                    raise Exception('Invalid option')

            if '_OPTIONS_' in self._placeholder:
                self._placeholder['_OPTIONS_'].update(kwargs)
            else:
                self._placeholder['_OPTIONS_'] = kwargs

        return self


class AlterTable(Table):
    def __init__(self, obj):

        self._placeholder = obj._placeholder
        self._main_query = 'ALTER TABLE %(_TABLE_)s %(_ALTER_)s %(_OPTIONS_)s'

        self.alterColumn = AlterColumn(self).alterColumn
        self.addColumn = AlterColumn(self).addColumn
        self.renameColumn = AlterColumn(self).renameColumn
        self.dropColumn = AlterColumn(self).dropColumn
        self.options = TableOptions(self).setOptions


class Column(object):

    def __init__(self, obj):
        self._main_query = obj._main_query
        self._placeholder = obj._placeholder

    def _setCqlType(self, name, cql_type, collection=None):
        pass

    def type_ascii(self, name, collection=None):
        self._setCqlType(name, 'ascii', collection)

    def type_bigint(self, name, collection=None):
        self._setCqlType(name, 'bigint', collection)

    def type_blob(self, name, collection=None):
        self._setCqlType(name, 'blob', collection)

    def type_boolean(self, name, collection=None):
        self._setCqlType(name, 'boolean', collection)

    def type_counter(self, name, collection=None):
        self._setCqlType(name, 'counter', collection)

    def type_decimal(self, name, collection=None):
        self._setCqlType(name, 'decimal', collection)

    def type_double(self, name, collection=None):
        self._setCqlType(name, 'double', collection)

    def type_float(self, name, collection=None):
        self._setCqlType(name, 'float', collection)

    def type_inet(self, name, collection=None):
        self._setCqlType(name, 'inet', collection)

    def type_int(self, name, collection=None):
        self._setCqlType(name, 'int', collection)

    def type_text(self, name, collection=None):
        self._setCqlType(name, 'text', collection)

    def type_timestamp(self, name, collection=None):
        self._setCqlType(name, 'timestamp', collection)

    def type_uuid(self, name, collection=None):
        self._setCqlType(name, 'uuid', collection)

    def type_timeuuid(self, name, collection=None):
        self._setCqlType(name, 'timeuuid', collection)

    def type_varchar(self, name, collection=None):
        self._setCqlType(name, 'varchar', collection)

    def type_varint(self, name, collection=None):
        self._setCqlType(name, 'varint', collection)

    # Method for set, list and map
    def type_list(self, name, cql_type):
        self._setCqlType(name, cql_type, 'list')

    def type_set(self, name, cql_type):
        self._setCqlType(name, cql_type, 'set')

    def type_map(self, name, cql_type):
        self._setCqlType(name, cql_type, 'map')

    def addColumn(self, *columns):
        return self


class CreateColumn(Column):

    def _setPlaceholderKey(self, key, value_type):
        if key not in self._placeholder or not self._placeholder[key]:
            # if provided key is not available or if the value is empty
            self._placeholder[key] = value_type

    def _setCqlType(self, name, cql_type, collection=None):
        """
        Type function to set cql data type of Columns

        :param name: String
        :param cql_type: String (general) or Tuple (if collection == 'map')
        :param collection: 'set' | 'list'
        """
        self._setPlaceholderKey('_COLUMNDEF_', dict())

        if collection in ('set', 'list'):
            cql_type = str(collection) + '<' + str(cql_type) + '>'
        elif collection is True:
            self.setPrimaryKey(name)
        elif collection == 'map' and isinstance(cql_type, tuple):
            cql_type = collection + '<' + ', '.join(cql_type) + '>'

        self._placeholder['_COLUMNDEF_'].update({name: cql_type})

    def addColumn(self, *columns):
        """
        Add columns to dictionary. All key and values will be rendered when execute is called.

        :param columns:
        :return: :raise:
        """
        if columns:
            self._setPlaceholderKey('_COLUMNDEF_', dict())

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


class AlterColumn(Column):

    def _setCqlType(self, name, cql_type, collection=None):

        if collection in ('set', 'list'):
            cql_type = str(collection) + '<' + str(cql_type) + '>'
        elif collection == 'map' and isinstance(cql_type, tuple):
            cql_type = collection + '<' + ', '.join(cql_type) + '>'

        self._placeholder[self._placeholder['cql-type']] = (name, cql_type)

    def alterColumn(self, *columns):
        """
        These changes to a column type are not allowed:
            * Changing the type of a clustering column.
            * Changing columns on which an index is defined.

        :param columns:
        :return: :raise:
        """
        self._placeholder['cql-type'] = '_ALTER-COLUMN_'
        if columns and len(columns) == 2:
            self._placeholder['_ALTER-COLUMN_'] = columns
            # Todo validate cql-type and string
        return self

    def addColumn(self, *columns):
        """
        These additions to a table are not allowed:
            * Adding a column having the same name as an existing column.
            * Adding columns to tables defined with COMPACT STORAGE.
        """
        self._placeholder['cql-type'] = '_ADD-COLUMN_'
        if columns and len(columns) == 2:
            self._placeholder['_ADD-COLUMN_'] = columns
            # Todo validate cql-type and string
        return self

    def dropColumn(self, column):
        self._placeholder['_DROP-COLUMN_'] = column

    def renameColumn(self, *columns):
        if columns:
            self._placeholder['_RENAME-COLUMN_'] = columns


if __name__ == '__main__':
    user = Table('user').create()
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

    user.options({'compression': 'guys', 'compaction': 'guys'})
    user.options(compression={'hello': 'guys', 'hi': 'guys'}, compaction={'class': 'sdf'}, compact=True)
    user.options(caching='hellow', comment='hou mou')

    user.execute()

    node = Table('node').create()
    node.options(caching='hellow', comment='hou mou')
    node.execute()

    # print(node._placeholder)
