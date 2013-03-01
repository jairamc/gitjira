
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

