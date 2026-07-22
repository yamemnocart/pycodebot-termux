class BotBaseError(Exception): pass
class ConfigError(BotBaseError): pass
class SearchError(BotBaseError): pass
class ScrapeError(BotBaseError): pass
class NetworkTimeoutError(BotBaseError): pass
class GitHubRateLimitError(BotBaseError): pass
class TranslationError(BotBaseError): pass
class SandboxError(BotBaseError): pass
