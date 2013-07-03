__author__ = 'rabit'

import object_mapper


def test_table():
    user = object_mapper.Table('user').Create()
    assert str(user)[:44] == '<pycql.object_mapper.CreateTable instance at'

    user.addColumn('uid', 'uuid')
    assert user._placeholder['_COLUMNDEF_']['uid'] == 'uuid'

    user._placeholder['_COLUMNDEF_'] = ''
    user.addColumn({'uid': 'uuid', 'email': 'text'})
    assert user._placeholder['_COLUMNDEF_']['uid'] is 'uuid' and user._placeholder['_COLUMNDEF_']['email'] is 'text'

    user._placeholder['_COLUMNDEF_'] = ''
    user.addColumn().type_ascii('char')
    assert user._placeholder['_COLUMNDEF_']['char'] == 'ascii'

    user.addColumn().type_varchar('username')
    assert user._placeholder['_COLUMNDEF_']['username'] == 'varchar'

    user._placeholder['_COLUMNDEF_'] = 0
    user.addColumn().type_text('email', 'set')
    assert user._placeholder['_COLUMNDEF_']['email'] == 'set<text>'

    user._placeholder['_COLUMNDEF_'] = {}
    user.addColumn().type_list('fav_post', 'varchar')
    assert user._placeholder['_COLUMNDEF_']['fav_post'] == 'list<varchar>'

    user._placeholder['_COLUMNDEF_'] = {}
    user.addColumn().type_map('todo', ('timestamp', 'text'))
    assert user._placeholder['_COLUMNDEF_']['todo'] == 'map<timestamp, text>'

    user._placeholder['_COLUMNDEF_'] = {}
    user.addColumn({'name': 'varchar', 'email': 'text'})
    user.addColumn().type_uuid('uid')
    user.setPrimaryKey('uid')
    assert user._placeholder['_PRIMARY-KEY_']['composite'] == 'uid'

    user._placeholder['_COLUMNDEF_'] = {}
    user.addColumn({'name': 'varchar', 'email': 'text'})
    user.addColumn().type_uuid('uid')
    user.setPrimaryKey('uid', 'email')
    assert user._placeholder['_PRIMARY-KEY_']['composite'] == 'uid'
    assert user._placeholder['_PRIMARY-KEY_']['compound'] == ['email']

    user.setPrimaryKey('uid', 'username', 'phone')
    assert user._placeholder['_PRIMARY-KEY_']['composite'] == 'uid'
    assert user._placeholder['_PRIMARY-KEY_']['compound'] == ['username', 'phone']

    user.setPrimaryKey(('uid', 'timezone'), 'username', 'phone')
    assert user._placeholder['_PRIMARY-KEY_']['composite'] == ['uid', 'timezone']
    assert user._placeholder['_PRIMARY-KEY_']['compound'] == ['username', 'phone']