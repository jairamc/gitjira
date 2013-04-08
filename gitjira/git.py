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
Handle git actions.
"""

import subprocess


class Git(object):
    def __init__(self, git='git'):
        self._git = git

    def _run(self, command, caller=subprocess.check_output):
        cmd = [self._git]
        if isinstance(command, basestring):
            cmd.append(command)
        else:
            cmd.extend(command)
        return caller(cmd)

    def status(self):
        return self._run('status')

    def branch(self, branch):
        return self._run(['checkout', '-b', branch])

    def commit(self, message=None):
        args = ['commit'] if message is None else ['commit', '-m', message, '-e']
        return self._run(args, caller=subprocess.call)

