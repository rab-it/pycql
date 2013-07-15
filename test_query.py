__author__ = 'rabit'

from render import Render
from query import Query
from uuid import uuid4


def test_insert():

    # Insert Test
    uuid = uuid4().hex
    data = dict({'!user_uuid': uuid,
                 'fan': 'johndoe'})

    query = Query('NerdMovies', 'Hollywood').insert(data)
    assert query.execute().strip() == "INSERT INTO Hollywood.NerdMovies ( user_uuid, fan ) " \
                                      "VALUES ( " + uuid + ", 'johndoe' )"

    uuid = uuid4().hex
    data = dict({'!user_uuid': uuid,
                 'fan': 'johndoe'})

    query = Query('NerdMovies', 'Hollywood').insert(data).ttl(1, 'day')
    assert query.execute().strip() == "INSERT INTO Hollywood.NerdMovies ( user_uuid, fan ) " \
                                      "VALUES ( " + uuid + ", 'johndoe' ) "\
                                      "USING TTL 86400"

    data = {'user_id': 'frodo',
            'first_name': 'Frodo',
            'last_name': 'Baggins',
            'emails': {'f@baggins.com', 'baggins@gmail.com'}}
    query = Query('users').insert(data)
    assert query.execute().strip() == "INSERT INTO users ( first_name, last_name, user_id, emails ) "\
                                      "VALUES ( 'Frodo', 'Baggins', 'frodo', {'baggins@gmail.com', 'f@baggins.com'} )"

    data = {'user_id': 'frodo',
            'todo': {'2012-10-2 12:10': 'die'}}
    query = Query('users').insert(data)
    assert query.execute().strip() == "INSERT INTO users ( todo, user_id ) "\
                                      "VALUES ( {'2012-10-2 12:10': 'die'}, 'frodo' )"

    data = {'!id': '62c36092-82a1-3a00-93d1-46196ee77204',
            '!song_order': 1,
            '!song_id': 'a3e64f8f-bd44-4f28-b8d9-6938726e34d4',
            'title': 'La Grange',
            'artist': 'ZZ Top',
            'album': 'Tres Hombres',
            }
    query = Query('playlists').insert(data)
    assert query.execute().strip() == "INSERT INTO playlists ( song_order, album, artist, title, id, song_id ) "\
                                      "VALUES ( 1, 'Tres Hombres', 'ZZ Top', 'La Grange', "\
                                      "62c36092-82a1-3a00-93d1-46196ee77204, a3e64f8f-bd44-4f28-b8d9-6938726e34d4 )"


def test_select():
    """
    + SELECT * FROM peers;
    - SELECT * FROM users WHERE first_name = 'jane' and last_name='smith';
    SELECT TTL (name) from excelsior.clicks WHERE url = 'http://apache.org';
    SELECT WRITETIME (name) FROM excelsior.clicks WHERE url = 'http://apache.org';
    SELECT WRITETIME (date) FROM excelsior.clicks WHERE url = 'http://google.org';
    SELECT * FROM users WHERE gender = 'f' AND state = 'TX' AND birth_year > 1968 ALLOW FILTERING;
    SELECT * FROM test WHERE token(k) > token(42);
    SELECT * FROM myTable WHERE t > maxTimeuuid('2013-01-01 00:05+0000') AND t < minTimeuuid('2013-02-02 10:00+0000')
    SELECT Name, Occupation FROM People WHERE empID IN (199, 200, 207);
    SELECT COUNT(*) FROM users;
    SELECT COUNT(*) FROM big_table LIMIT 50000;
    SELECT COUNT(*) FROM system.Migrations;
    SELECT * FROM ruling_stewards WHERE king = 'Brego' AND reign_start >= 2450 AND reign_start < 2500 ALLOW FILTERING;
    Select * FROM ruling_stewards WHERE king = 'none' AND reign_start >= 1500 AND reign_start < 3000 LIMIT 10 ALLOW FILTERING;
    SELECT * FROM periods WHERE TOKEN(period_name) > TOKEN('Third Age') AND TOKEN(period_name) < TOKEN('Fourth Age');
    SELECT * FROM playlists WHERE id = 62c36092-82a1-3a00-93d1-46196ee77204 ORDER BY song_order DESC LIMIT 50;
    SELECT title FROM playlists WHERE artist = 'Fu Manchu';
    """

    query = Query('peers').select()
    assert query.execute().strip() == "SELECT * FROM peers"

    query = Query('users').select().compare('first_name', 'jane').compare('last_name', 'smith', '=')
    assert query.execute().strip() == "SELECT * FROM users WHERE first_name = 'jane' and last_name = 'smith'"



