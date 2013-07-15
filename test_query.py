__author__ = 'rabit'

from render import Render
from query import Query
from uuid import uuid4


def test_insert():

    # Insert Test
    uuid = uuid4().hex
    data = dict({'user__uuid': uuid,
                 'fan': 'johndoe'})

    query = Query('NerdMovies', 'Hollywood').insert(data)
    assert query.execute().strip() == "INSERT INTO Hollywood.NerdMovies ( user__uuid, fan ) " \
                                      "VALUES ( " + uuid + ", 'johndoe' )"

    uuid = uuid4().hex
    data = dict({'user__uuid': uuid,
                 'fan': 'johndoe'})

    query = Query('NerdMovies', 'Hollywood').insert(data).ttl(1, 'day')
    assert query.execute().strip() == "INSERT INTO Hollywood.NerdMovies ( user__uuid, fan ) " \
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

    data = {'id__uuid': '62c36092-82a1-3a00-93d1-46196ee77204',
            'song_order': 1,
            'song_id__uuid': 'a3e64f8f-bd44-4f28-b8d9-6938726e34d4',
            'title': 'La Grange',
            'artist': 'ZZ Top',
            'album': 'Tres Hombres',
            }
    query = Query('playlists').insert(data)
    assert query.execute().strip() == "INSERT INTO playlists ( id__uuid, album, song_order, artist, title, song_id__uuid ) "\
                                      "VALUES ( 62c36092-82a1-3a00-93d1-46196ee77204, 'Tres Hombres', 1, 'ZZ Top', 'La Grange', "\
                                      "a3e64f8f-bd44-4f28-b8d9-6938726e34d4 )"


def test_select():

    query = Query('peers').select()
    assert query.execute().strip() == "SELECT * FROM peers"

    query = Query('users').select().compare('first_name', 'jane').compare('last_name', 'smith', '=')
    assert query.execute().strip() == "SELECT * FROM users WHERE first_name = 'jane' AND last_name = 'smith'"

    query = Query('clicks', 'excelsior').select().ttl('name').compare('url', 'http://apache.org')
    assert query.execute().strip() == "SELECT TTL (name) FROM excelsior.clicks WHERE url = 'http://apache.org'"

    query = Query('clicks', 'excelsior').select().writetime('name').compare('url', 'http://apache.org')
    assert query.execute().strip() == "SELECT WRITETIME (name) FROM excelsior.clicks WHERE url = 'http://apache.org'"

    query = Query('clicks', 'excelsior').select().writetime('date').compare('url', 'http://google.org')
    assert query.execute().strip() == "SELECT WRITETIME (date) FROM excelsior.clicks WHERE url = 'http://google.org'"

    query = Query('users').select().compare('gender', 'f').compare('state', 'TX').compare('birth_year', 1968, '>')
    query.allowFiltering()
    assert query.execute().strip() == "SELECT * FROM users WHERE gender = 'f' AND state = 'TX' AND birth_year > 1968 " \
                                      "ALLOW FILTERING"

    query = Query('test').select().compareToken('k', 42, '>')
    assert query.execute().strip() == "SELECT * FROM test WHERE TOKEN (k) > TOKEN (42)"

    query = Query('myTable').select().compare('t', "maxTimeuuid('2013-01-01 00:05+0000')", '>', True)
    query.compare('t', "minTimeuuid('2013-02-02 10:00+0000')", '<', True)
    assert query.execute().strip() == "SELECT * FROM myTable WHERE t > maxTimeuuid('2013-01-01 00:05+0000') " \
                                      "AND t < minTimeuuid('2013-02-02 10:00+0000')"

    query = Query('People').select('Name', 'Occupation').compare('empID', (199, 200, 207), 'IN')
    assert query.execute().strip() == "SELECT Name, Occupation FROM People WHERE empID IN (199, 200, 207)"

    query = Query('users').select('COUNT(*)')
    assert query.execute().strip() == "SELECT COUNT(*) FROM users"

    query = Query('users').select().count()
    assert query.execute().strip() == "SELECT COUNT(*) FROM users"

    query = Query('big_table').select().count().limit(50000)
    assert query.execute().strip() == "SELECT COUNT(*) FROM big_table LIMIT 50000"

    query = Query('Migrations', 'system').select().count()
    assert query.execute().strip() == "SELECT COUNT(*) FROM system.Migrations"

    query = Query('ruling_stewards').select().compare('king', 'Brego', '=').compare('reign_start', 2450, '>=')
    query.compare('reign_start', 2500, '<').allowFiltering()
    assert query.execute().strip() == "SELECT * FROM ruling_stewards WHERE king = 'Brego' AND reign_start >= 2450 " \
                                      "AND reign_start < 2500 ALLOW FILTERING"

    query = Query('ruling_stewards').select().compare('king', 'none').compare('reign_start', 1500, '>=')
    query.compare('reign_start', 3000, '<').allowFiltering().limit(10)
    assert query.execute().strip() == "SELECT * FROM ruling_stewards WHERE king = 'none' AND reign_start >= 1500 " \
                                      "AND reign_start < 3000 LIMIT 10 ALLOW FILTERING"

    query = Query('periods').select().compareToken('period_name', 'Third Age', '>')
    query.compareToken('period_name', 'Fourth Age', '<')
    assert query.execute().strip() == "SELECT * FROM periods WHERE TOKEN (period_name) > TOKEN ('Third Age') " \
                                      "AND TOKEN (period_name) < TOKEN ('Fourth Age')"

    query = Query('playlists').select().compare('id__uuid', '62c36092-82a1-3a00-93d1-46196ee77204')
    query.limit(50).orderBy('song_order', 'desc')
    assert query.execute().strip() == "SELECT * FROM playlists WHERE id__uuid = 62c36092-82a1-3a00-93d1-46196ee77204 " \
                                      "ORDER BY song_order DESC LIMIT 50"

    query = Query('playlists').select('title').compare( 'artist', 'Fu Manchu')
    assert query.execute().strip() == "SELECT title FROM playlists WHERE artist = 'Fu Manchu'"





