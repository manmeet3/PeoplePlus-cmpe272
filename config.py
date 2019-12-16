class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    # setting this to True activates the debug mode on the app.
    # This allows us to use the Flask debugger in case of an unhandled exception, and
    # also automatically reloads the application when it is updated.
    SQLALCHEMY_ECHO = True
    # setting this to True helps us with debugging by allowing SQLAlchemy to
    # log errors.


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    # 'SECRET_KEY': 'u\x91\xcf\xfa\x0c\xb9\x95\xe3t\xba2K\x7f\xfd\xca\xa3\x9f\x90\x88\xb8\xee\xa4\xd6\xe4',
    'TESTING': True,
    'KEYCLOAK_URL':'http://localhost:8080/auth/',
    'REALM_NAME':'BlueHats',
    'CLIENT_NAME':'emp_client',
    'CLIENT_SECRET':'1fa17208-c3ef-45ac-a0a5-21062c5c1080',
    'USERNAME':'bluehats_user',
    'PASSWORD':'password'
    # 'DEBUG': True,
    # 'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    # 'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    # 'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    # 'OIDC_VALID_ISSUERS': ['http://localhost:8080/auth/realms/peopleplus'],
    # 'OIDC_OPENID_REALM': 'http://localhost:5000/oidc_callback'
}

