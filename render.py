__author__ = 'rabit'

import re


class Render(object):

    def validate(self):
        pass

    def _placeholders(self):

        functions = {'_TABLE_': self._placeholder['_TABLE_'],
                     '_COLUMNDEF_': self.__renderColumndef(),
                     '_PRIMARY-KEY_': self.__renderPK(),
                     '_OPTIONS_': self.__renderOptions(),
                     '_ALTER_': self.__renderAlter(),
                     }

        return functions

    def __renderOptions(self):

        opt = ''
        if '_OPTIONS_' not in self._placeholder:
            return opt

        opt_dict = self._placeholder['_OPTIONS_']

        opt_dict['_PROPERTIES_'] = list()
        opt += 'WITH '

        compact = opt_dict.pop('compact', None)
        if compact:
            opt_dict['_PROPERTIES_'].append('COMPACT STORAGE')

        if opt_dict:
            opt_dict['_PROPERTIES_'] += (['{} = {}'.format(k, v) for (k, v) in opt_dict.items()
                                          if not re.search(r'_[A-Z-]*?_', k)])

        opt += ' AND '.join(opt_dict['_PROPERTIES_'])

        return opt

    def __renderColumndef(self):
        if '_COLUMNDEF_' in self._placeholder:
            return ', '.join(['%s %s' % (key, value) for (key, value) in self._placeholder['_COLUMNDEF_'].items()])
        else:
            return ''

    def __renderAlter(self):
        if '_ALTER-COLUMN_' in self._placeholder:
            column = self._placeholder['_ALTER-COLUMN_']
            return 'ALTER ' + column[0] + ' TYPE ' + column[1]
        if '_ADD-COLUMN_' in self._placeholder:
            column = self._placeholder['_ADD-COLUMN_']
            return 'ADD ' + column[0] + ' ' + column[1]
        if '_DROP-COLUMN_' in self._placeholder:
            return 'DROP ' + self._placeholder['_DROP-COLUMN_']
        if '_RENAME-COLUMN_' in self._placeholder:
            column = self._placeholder['_RENAME-COLUMN_']
            return 'RENAME ' + column[0] + ' TO ' + column[1]

    def __validatePK(self):
        if '_PRIMARY-KEY_' in self._placeholder and 'composite' in self._placeholder['_PRIMARY-KEY_']:
            pk_dict = self._placeholder['_PRIMARY-KEY_']
            for pk_type in pk_dict:
                if isinstance(pk_dict[pk_type], list):
                    for pk in pk_dict[pk_type]:
                        if not pk in self._placeholder['_COLUMNDEF_']:
                            raise Exception('{} key {} is not a column'.format(pk_type.title(), pk))
                else:
                    if not pk_dict[pk_type] in self._placeholder['_COLUMNDEF_']:
                        raise Exception('{} key {} is not a column'.format(pk_type.title(), pk_dict[pk_type]))

        else:
            raise Exception('Primary key is required')

    def __renderPK(self):

        pk = ''

        if '_PRIMARY-KEY_' not in self._placeholder:
            return pk

        self.__validatePK()

        pk_dict = self._placeholder['_PRIMARY-KEY_']

        pk += 'PRIMARY KEY ('

        if isinstance(pk_dict['composite'], list):
            pk += '(' + ', '.join(pk_dict['composite']) + ')'
        else:
            pk += pk_dict['composite']

        if 'clustering' in pk_dict:
            pk += ', ' + ', '.join(pk_dict['clustering'])

        pk += ')'

        return pk

    def render(self, obj):

        self._placeholder = obj._placeholder
        self._main_query = obj._main_query

        pattern_query_placeholder = r'<(_[A-Z-]*?_)>'

        query_with_placeholders = re.sub(pattern_query_placeholder, r'\1', self._main_query)

        render = query_with_placeholders % self._placeholders()
        print (render)
        return render


class RenderQuery(Render):
    def _placeholders(self):

        functions = {'_TABLE_': self._placeholder['_TABLE_'],
                     '_IDENTIFIER_': self.__renderIdentifier(),
                     '_VALUES_': self.__renderValues(),
                     '_OPTIONS_': self.__renderOptions(),
                     }

        return functions

    def __renderIdentifier(self):
        if '_IDENTIFIER_' not in self._placeholder:
            raise Exception('Identifier missing in query')
        elif not isinstance(self._placeholder['_IDENTIFIER_'], dict):
            raise Exception('Dictonay type expected')

        identifier = self._placeholder['_IDENTIFIER_']
        key = list()
        value = list()
        wrapQuote = lambda string: "'" + str(string) + "'"

        for k, v in identifier.items():
            key.append(k[1:]) if k[:1] == '!' else key.append(k)
            if not isinstance(v, (list, set, dict)):
                value.append(str(v) if k[:1] == '!' else wrapQuote(v))
            elif isinstance(v, (set, list)):
                v = '{' + ', '.join(list(v) if k[:1] == '!' else [wrapQuote(item) for item in v]) + '}'
                value.append(v)
            elif isinstance(v, dict):
                value.append(str(v))

        self._placeholder['_VALUES_'] = ', '.join(value)
        return ', '.join(key)

    def __renderValues(self):

        if '_VALUES_' not in self._placeholder:
            self.__renderIdentifier()

        return self._placeholder['_VALUES_']

    def __renderOptions(self):
        if '_OPTIONS_' in self._placeholder and '_TTL_' in self._placeholder['_OPTIONS_']:
            return 'USING TTL ' + str(self._placeholder['_OPTIONS_']['_TTL_'])
        else:
            return ''