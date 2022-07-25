import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.yandex.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '465'))
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() in \
                                                    ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    BLOG_MAIL_SUBJECT_PREFIX = os.environ.get('BLOG_MAIL_SUBJECT_PREFIX', 'blog_flask')
    BLOG_MAIL_SENDER = os.environ.get('BLOG_MAIL_SENDER')
    BLOG_ADMIN = os.environ.get('BLOG_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BLOG_POSTS_PER_PAGE = 5
    BLOG_FOLLOWERS_PER_PAGE = 5
    BLOG_COMMENTS_PER_PAGE = 5
    
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')
    # SQLALCHEMY_ECHO = True



class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    
    'default': DevelopmentConfig
}