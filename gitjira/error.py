

class GitJiraError(Exception):
    pass


class HTTPError(GitJiraError):
    pass


class ConfigurationError(GitJiraError):
    pass


class GitError(GitJiraError):
    pass

class GitBranchError(GitError):
    pass

