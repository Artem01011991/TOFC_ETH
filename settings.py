try:
    import local_settings
    DEBUG = local_settings.DEBUG
except:
    DEBUG = False

HEROKU_APP_NAME = 'immense-eyrie-59509'
