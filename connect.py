__author__ = 'rabit'

import cql
import table


def connect():
    # cql_version='3.0.0' is a must to keep it working
    conn = cql.connect('localhost', keyspace='demodb', cql_version='3.0.0')
    cursor = conn.cursor()

    # cursor.close()
    # con.close()
    return cursor


def add(a, b, c):
    return a+b+c


def select(*columns):
    columns = list(columns)

    columns_names = ', '.join(columns)

    pycql = connect()
    pycql.execute("SELECT " + columns_names + " FROM users")

    return pycql.fetchone()


def main():
    print select('gender', 'user_name')
    node = table.Table()
    node.create('Node').execute()


if __name__ == '__main__':
    main()