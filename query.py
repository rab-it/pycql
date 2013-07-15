__author__ = 'rabit'

from render import RenderQuery


class Query(object):
    def __init__(self, table_name, keyspace=None):
        self._placeholder = dict()
        self._main_query = ''
        self._placeholder['_TABLE_'] = keyspace + '.' + table_name if keyspace else table_name

        self.insert = Insert(self).insert
        self.select = Select(self).select

    def execute(self):
        return RenderQuery().render(self)


class Select(Query):
    def __init__(self, obj):
        self._placeholder = obj._placeholder
        self._main_query = "SELECT %(_EXPR_)s FROM %(_TABLE_)s " \
                           "%(_WHERE_)s%(_ORDER_)s" \
                           "%(_LIMIT_)s%(_ALLOW-FILTERING_)s"

    def select(self, *columns):
        if columns and isinstance(columns[0], str):
            self._placeholder['_EXPR_'] = ', '.join(columns)
        elif columns and isinstance(columns[0], (tuple, list, set)):
            self._placeholder['_EXPR_'] = ', '.join(columns[0])
        return self

    def allowFiltering(self):
        self._placeholder['_ALLOW-FILTERING_'] = True
        return self

    def limit(self, limit):
        if isinstance(limit, int):
            self._placeholder['_LIMIT_'] = str(limit)
        return self

    def ttl(self, col_name):
        self._placeholder['_EXPR_'] = 'TTL (' + col_name + ')'
        return self

    def count(self):
        self._placeholder['_EXPR_'] = 'COUNT(*)'
        return self

    def writetime(self, col_name):
        self._placeholder['_EXPR_'] = 'WRITETIME (' + col_name + ')'
        return self

    def compare(self, key, value, comparator='=', no_string=False):
        if not isinstance(key, str):
            raise Exception("Compare key type mismatched")

        if '_WHERE_' not in self._placeholder:
            self._placeholder['_WHERE_'] = list()

        self._placeholder['_WHERE_'].append((key, value, comparator, no_string))

        return self

    def orderBy(self, col_name, order='ASC'):
        self._placeholder['_ORDER_'] = (col_name, order)

    def compareToken(self, key, value, comparator='=', term_only=False):

        key = 'TOKEN (' + key + ')'
        if isinstance(value, str):
            value = "'" + value + "'"

        value = value if term_only else 'TOKEN (' + str(value) + ')'

        return self.compare(key, value, comparator, True)


class Insert(Query):

    def __init__(self, obj):
        self._placeholder = obj._placeholder
        self._main_query = obj._main_query

    def insert(self, data):
        # Todo: Options

        self._main_query = "INSERT INTO %(_TABLE_)s ( %(_IDENTIFIER_)s ) VALUES ( %(_VALUES_)s ) %(_OPTIONS_)s"

        if not isinstance(data, dict):
            raise Exception("Dictionary type data expected for insert query")

        self._placeholder['_IDENTIFIER_'] = data

        return self

    def ttl(self, duration, human_readable='s'):
        """
        Set TTL (Time to Live) for a data

        :param duration:
        :param human_readable: [default 's'] calculate second from human readable time
        :return:
        """

        if human_readable == 'min':
            duration *= 60
        elif human_readable == 'hr':
            duration *= 3600
        elif human_readable == 'day':
            duration *= 86400

        self._placeholder['_OPTIONS_'] = dict({'_TTL_': duration})

        return self