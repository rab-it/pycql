__author__ = 'rabit'

import object_mapper


def test_Create_table():

    ###
    ### Add column test
    ###

    # Create table
    user = object_mapper.Table('user').create()
    # assert str(user)[:42] == '<pycql.object_mapper.CreateTable object at'

    # Add column Tuple
    user.addColumn('uid', 'uuid')
    # assert user._placeholder['_COLUMNDEF_']['uid'] == 'uuid'

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
    user.options(compact=True)

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
    user = object_mapper.Table('user').create()
    user.options(compression={'hello': 'guys', 'hi': 'guys'}, compaction={'class': 'sdf'})
    render = user.execute()
    assert "WITH compression = {'hi': 'guys', 'hello': 'guys'} " \
           "AND compaction = {'class': 'sdf'}" in render

    user = object_mapper.Table('user').create()
    user.options(compression={'hello': 'guys', 'hi': 'guys'}, compaction={'class': 'sdf'})
    user.options(caching='hellow', comment='hou mou')
    render = user.execute()
    assert "WITH caching = hellow AND comment = hou mou AND compression = {'hi': 'guys', 'hello': 'guys'} " \
           "AND compaction = {'class': 'sdf'}" in render

    user = object_mapper.Table('user').create()
    user.addColumn('uid', 'uuid')
    user.options(compression={'hello': 'guys', 'hi': 'guys'}, compaction={'class': 'sdf'})
    user.options(caching='hellow', comment='hou mou')
    user.options(compact=True)
    render = user.execute()
    assert "WITH COMPACT STORAGE AND comment = hou mou AND compression = {'hi': 'guys', 'hello': 'guys'} " \
           "AND compaction = {'class': 'sdf'} AND caching = hellow" in render

    ###
    ### Table Alter Test
    ###

    # Alter Column
    user = object_mapper.Table('adamsFamily', 'monsters').alter()
    user.alterColumn('lastKnownLocation', 'uuid')
    user.options(compact=True)
    render = user.execute()
    assert render == 'ALTER TABLE monsters.adamsFamily ALTER lastKnownLocation TYPE uuid WITH COMPACT STORAGE'

    # Alter Column with type syntax
    user = object_mapper.Table('adamsFamily', 'monsters').alter()
    user.alterColumn().type_uuid('lastKnownLocation')
    user.options(compact=True)
    render = user.execute()
    assert render == 'ALTER TABLE monsters.adamsFamily ALTER lastKnownLocation TYPE uuid WITH COMPACT STORAGE'

    # Alter column with map type
    user = object_mapper.Table('adamsFamily', 'monsters').alter()
    user.alterColumn().type_map('lastKnownLocation', ('uuid', 'text'))
    user.options(compact=True)
    render = user.execute()
    assert render == 'ALTER TABLE monsters.adamsFamily ALTER lastKnownLocation TYPE map<uuid, text> ' \
                     'WITH COMPACT STORAGE'