try:
    import local_settings
    DEBUG = local_settings.DEBUG
except ImportError:
    DEBUG = False