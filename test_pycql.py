import connection
# from table import Table
#
# def setup_func():
#     connection.setup(['localhost:9160:quantweb', 'localhost:9145:quantweb'])
#     execute_obj = connection.execute("INSERT INTO songs (id, title)VALUES (62c36092-82a1-3a00-93d1-46196ee77211, 'Come away');")
#     return True if execute_obj else False
#
# def test_setup():
#     assert setup_func() == True


connection.setup(['localhost:9160:quantweb', 'localhost:9145:quantweb'])


def select(*columns):
    columns = list(columns)

    columns_names = ', '.join(columns)
    execute_obj = connection.execute("SELECT " + columns_names + " FROM songs")

    # pycql = connect()
    # pycql.execute("SELECT " + columns_names + " FROM songs")

    return execute_obj.fetchall()

print select('title')