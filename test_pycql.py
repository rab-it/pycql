import connection

def setup_func():
    connection.setup(['localhost:9160:quantweb', 'localhost:9145:quantweb'])
    execute_obj = connection.execute("INSERT INTO songs (id, title)VALUES (62c36092-82a1-3a00-93d1-46196ee77211, 'Come away');")
    return True if execute_obj else False

def test_setup():
    assert setup_func() == True