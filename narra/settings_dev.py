SECRET_KEY = 'a8&wn^2mn!*sp&@tf6n9rfcfym(4e)$c+g_%!r7(*ggw2i=8u9'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'palmis_prod',
        'USER': 'postgres',
        'PASSWORD': 'Pa$$word99',
        'HOST': 'localhost',
        'PORT': '5432'
    }
    # "default": {
    #     "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
    #     "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
    #     "USER": os.environ.get("SQL_USER", "user"),
    #     "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
    #     "HOST": os.environ.get("SQL_HOST", "localhost"),
    #     "PORT": os.environ.get("SQL_PORT", "5432"),
    # }
}

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'},
    'ACCESS_TOKEN_EXPIRE_SECONDS': 86400,  # 30 min
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400,  # 30 min
    'OAUTH_DELETE_EXPIRED': True,
}
