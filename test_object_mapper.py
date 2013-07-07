__author__ = 'rabit'

import object_mapper


def test_Create_table():

    ###
    ### Add column test
    ###

    # Create table
    user = object_mapper.Table('user').Create()
    assert str(user)[:44] == '<pycql.object_mapper.CreateTable instance at'

    # Add column Tuple
    user.addColumn('uid', 'uuid')
    assert user._placeholder['_COLUMNDEF_']['uid'] == 'uuid'

    # Add column Dictionary
    user._placeholder['_COLUMNDEF_'] = ''
    user.addColumn({'uid': 'uuid', 'email': 'text'})
    assert user._placeholder['_COLUMNDEF_']['uid'] is 'uuid' and user._placeholder['_COLUMNDEF_']['email'] is 'text'

    # Add column as type
    user._placeholder['_COLUMNDEF_'] = ''
    user.addColumn().type_ascii('char')
    assert user._placeholder['_COLUMNDEF_']['char'] == 'ascii'

    user.addColumn().type_varchar('username')
    assert user._placeholder['_COLUMNDEF_']['username'] == 'varchar'

    # Add column with collection as type
    user._placeholder['_COLUMNDEF_'] = 0
    user.addColumn().type_text('email', 'set')
    assert user._placeholder['_COLUMNDEF_']['email'] == 'set<text>'

    # Add column as collection
    user._placeholder['_COLUMNDEF_'] = {}
    user.addColumn().type_list('fav_post', 'varchar')
    assert user._placeholder['_COLUMNDEF_']['fav_post'] == 'list<varchar>'

    # Add column as map
    user._placeholder['_COLUMNDEF_'] = {}
    user.addColumn().type_map('todo', ('timestamp', 'text'))
    assert user._placeholder['_COLUMNDEF_']['todo'] == 'map<timestamp, text>'

    # Add column as type with primary key
    user._placeholder['_COLUMNDEF_'] = {}
    user.addColumn({'name': 'varchar', 'email': 'text'})
    user.addColumn().type_uuid('uid', True)
    assert user._placeholder['_PRIMARY-KEY_']['composite'] == 'uid'

    # Set primary key
    user._placeholder['_COLUMNDEF_'] = {}
    user.addColumn({'name': 'varchar', 'email': 'text'})
    user.addColumn().type_uuid('uid')
    user.setPrimaryKey('uid')
    assert user._placeholder['_PRIMARY-KEY_']['composite'] == 'uid'

    # Set compound primary key
    user._placeholder['_COLUMNDEF_'] = {}
    user.addColumn({'name': 'varchar', 'email': 'text'})
    user.addColumn().type_uuid('uid')
    user.setPrimaryKey('uid', 'email')
    assert user._placeholder['_PRIMARY-KEY_']['composite'] == 'uid'
    assert user._placeholder['_PRIMARY-KEY_']['clustering'] == ['email']

    # Set compound primary key with multiple clustering key
    user.setPrimaryKey('uid', 'username', 'phone')
    assert user._placeholder['_PRIMARY-KEY_']['composite'] == 'uid'
    assert user._placeholder['_PRIMARY-KEY_']['clustering'] == ['username', 'phone']

    # Set composite primary key with multiple composite key and multiple clustering key
    user.setPrimaryKey(('uid', 'timezone'), 'username', 'phone')
    assert user._placeholder['_PRIMARY-KEY_']['composite'] == ['uid', 'timezone']
    assert user._placeholder['_PRIMARY-KEY_']['clustering'] == ['username', 'phone']

    ###
    ###  Render Functions test
    ###
    renderUser = user
    renderUser.addColumn('username', 'text')
    renderUser.addColumn('phone', 'text')
    renderUser.setPrimaryKey('uid', 'username', 'phone')
    render = renderUser.execute()
    assert 'PRIMARY KEY (uid, username, phone)' in render

    renderUser.addColumn().type_timeuuid('timezone')
    renderUser.setPrimaryKey(('uid', 'timezone'), 'username', 'phone')
    render = renderUser.execute()
    assert 'PRIMARY KEY ((uid, timezone), username, phone)' in render

    renderUser.setPrimaryKey('uid')
    render = renderUser.execute()
    assert 'PRIMARY KEY (uid)' in render

    ###
    ### Table Options test
    ###
    user = object_mapper.Table('user')
    user.Create().options({'hello': 'guys'})


