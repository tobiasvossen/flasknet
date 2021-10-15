import secrets


class Config(object):
    DATABASE = ''
    TESTING = False

    @property
    def SECRET_KEY(self):
        return secrets.token_urlsafe(16)

    def summary(self):
        print(' * Database at ' + self.DATABASE)
        print(' * Testing? ' + str(self.TESTING))


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'


class TestingConfig(Config):
    TESTING = True
