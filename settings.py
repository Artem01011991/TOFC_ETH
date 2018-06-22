try:
    import local_settings
    DEBUG = local_settings.DEBUG
except:
    DEBUG = False