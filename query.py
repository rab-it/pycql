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
        self._main_query = obj._main_query

    def select(self, *args):

        self._main_query = "SELECT %(<_EXPR_>)s FROM %(_TABLE_)s " \
                           "%(<_WHERE_>)s %(<_ORDER_>)s " \
                           "%(<_LIMIT_>)s %(<_ALLOW-FILTERING_>)s"
        return self

    def compare(self, key, value, comparator='='):
        if not isinstance(key, str):
            raise Exception("Compare key type mismatched")

        if '_WHERE_' not in self._placeholder:
            self._placeholder['_WHERE_'] = list()

        self._placeholder['_WHERE_'].append((key, value, comparator))

        return self


class Insert(Query):

    def __init__(self, obj):
        self._placeholder = obj._placeholder
        self._main_query = obj._main_query

    def insert(self, data):
        # Todo: Options

        self._main_query = "INSERT INTO %(_TABLE_)s ( %(<_IDENTIFIER_>)s ) VALUES ( %(<_VALUES_>)s ) %(<_OPTIONS_>)s"

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