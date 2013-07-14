__author__ = 'rabit'

from render import RenderQuery


class Query(object):
    def __init__(self, table_name, keyspace=None):
        self._placeholder = dict()
        self._main_query = ''
        self._placeholder['_TABLE_'] = keyspace + '.' + table_name if keyspace else table_name

        self.insert = Insert(self).insert

    def execute(self):
        return RenderQuery().render(self)


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