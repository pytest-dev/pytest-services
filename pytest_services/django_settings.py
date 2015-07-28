"""Django setttings helpers."""
import imp
import os
import sys

from importlib import import_module
from django.core.urlresolvers import clear_url_caches, set_urlconf
from django.template import context, base, loader
from django.utils import translation
from django.utils.translation import trans_real


def setup_django_settings(test_settings):
    """Override the enviroment variable and call the _setup method of the settings object to reload them."""
    os.environ['DJANGO_SETTINGS_MODULE'] = test_settings

    from django.conf import settings as django_settings

    # (re)setup django settings
    django_settings._setup()

    # reload settings
    reload_settings(django_settings)


def clean_django_settings():
    """Clean current django settings."""
    from django.conf import settings as django_settings

    del os.environ['DJANGO_SETTINGS_MODULE']
    django_settings._wrapped = None


def reload_settings(settings, databases=None):
    """Special routine to reload django settings.

    Including:
    urlconf module, context processor, templatetags settings, database settings.
    """
    if databases:
        settings.DATABASES.update(databases)

    # check if there's settings to reload
    if hasattr(settings, 'ROOT_URLCONF'):
        if settings.ROOT_URLCONF in sys.modules:
            imp.reload(sys.modules[settings.ROOT_URLCONF])
        import django
        if hasattr(django, 'setup'):
            django.setup()
        import_module(settings.ROOT_URLCONF)
        set_urlconf(settings.ROOT_URLCONF)
        settings.LANGUAGE_CODE = 'en'  # all tests should be run with English by default

        # Make the ConnectionHandler use the new settings, otherwise the ConnectionHandler will have old configuraton.
        from django.db.utils import ConnectionHandler
        import django.db
        from django.db.utils import load_backend
        import django.db.transaction
        import django.db.models
        import django.db.models.sql.query
        import django.core.management.commands.syncdb
        import django.db.models.sql.compiler
        import django.db.backends
        import django.db.backends.mysql.base
        import django.core.management.commands.loaddata

        # all modules which imported django.db.connections should be changed to get new ConnectionHanlder
        django.db.models.sql.compiler.connections = django.db.models.connections = \
            django.core.management.commands.loaddata.connections = \
            django.db.backends.connections = django.db.backends.mysql.base.connections = \
            django.core.management.commands.syncdb.connections = django.db.transaction.connections = \
            django.db.connections = django.db.models.base.connections = django.db.models.sql.query.connections = \
            ConnectionHandler(settings.DATABASES)

        # default django connection and backend should be also changed
        django.db.connection = django.db.connections[django.db.DEFAULT_DB_ALIAS]
        django.db.backend = load_backend(django.db.connection.settings_dict['ENGINE'])

        import django.core.cache
        django.core.cache.cache = django.core.cache._create_cache(django.core.cache.DEFAULT_CACHE_ALIAS)

        # clear django urls cache
        clear_url_caches()
        # clear django contextprocessors cache
        context._standard_context_processors = None
        # clear django templatetags cache
        base.templatetags_modules = None

        # reload translation files
        imp.reload(translation)
        imp.reload(trans_real)

        # clear django template loaders cache
        loader.template_source_loaders = None
        from django.template.loaders import app_directories
        imp.reload(app_directories)
    from django.template.base import get_templatetags_modules
    get_templatetags_modules.cache_clear()
    import django.apps
    import django
    import django.template
    django.template.engines.__dict__.pop('templates', None)
    django.template.engines._templates = None
    django.template.engines._engines = {}
    if django.apps.apps.ready:
        django.apps.apps.set_installed_apps(settings.INSTALLED_APPS)
    django.setup()
