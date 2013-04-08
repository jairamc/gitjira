#################################################################################
#
#    Copyright 2013 Jairam Chandar & Michael Pitidis
#  
#    This file is part of GitJira.
#
#    GitJira is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    GitJira is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with GitJira.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
"""
Configuration.
"""

from error import ConfigurationError


class Configuration(object):

    _keys = 'base_url', 'userhash'

    def __init__(self, **kwargs):
        self._validate(kwargs)
        self.__dict__.update(kwargs) # Nasty stuff >_<

    @staticmethod
    def _validate(data):
        missing = [k for k in Configuration._keys if not k in data]
        if missing:
            raise ConfigurationError('Missing keys [%s]' % ', '.join(`k` for k in missing))

    @staticmethod
    def _read(filename, sep='='):
        with open(filename, 'rb') as f:
            for line in f:
                yield tuple(token.strip() for token in line.split(sep, 1))

    @staticmethod
    def read(filename):
        return Configuration(**dict(Configuration._read(filename)))

    def write(self, filename, sep='='):
        with open(filename, 'wb') as f:
            f.write('\n'.join(sep.join([k, getattr(self, k)]) \
                              for k in self._keys))

