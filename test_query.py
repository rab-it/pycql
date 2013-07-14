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