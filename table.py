__author__ = 'rabit'


class Table():
    def __init__(self, keyspace=None, case_sensitive=False):
        self.__query = ''
        self.__case_sensitive = case_sensitive
        self.__keyspace = keyspace

    def create(self, table_name):
        """

        :param table_name:
        :return:
        """

        table_name = table_name if self.__case_sensitive else table_name.lower()
        self.__query = 'CREATE TABLE ' + self.__keyspace + '.' + table_name
        return self

    def addColumn(self, column_name, column_type):
        self.__query = self.__query + column_name + ' ' + column_type + ', '
        return self

    def primaryKey(self, key):
        self.__query = self.__query + 'PRIMARY KEY (' + key + ')'
        print self.__query
        return self

    def execute(self):
        # TODO: close conn
        return self.__query


if __name__ == '__main__':
    node = Table('demo')
    node.create('Node')
    node.addColumn('nid', 'uuid')
    node.addColumn('title', 'varchar')
    node.addColumn('body', 'varchar')
    node.primaryKey('nid')
    node.execute()