"""
This file was generated with the custommenu management command, it contains
the classes for the admin menu, you can customize this class as you want.

To activate your custom menu add the following to your settings.py::
    ADMIN_TOOLS_MENU = 'paranuara_challenge.menu.CustomMenu'
"""

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from admin_tools.menu import items, Menu


class CustomMenu(Menu):
    """
    Custom Menu for Paranuara Challenge admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),
            items.Bookmarks(),
            # items.AppList(
            #     _('Context'),
            #     models=(
            #         'paranuara_challenge.context.*',
            #         'paranuara_challenge.feature.*',
            #         'paranuara_challenge.follow.*',
            #         'django_proximity_roles.*',
            #     ),
            # ),
            # items.AppList(
            #     _('Decisions'),
            #     models=(
            #         'paranuara_challenge.polls.*',
            #         'paranuara_challenge.polls.*',
            #         'paranuara_challenge.decisions.*',
            #     )
            # ),
            items.AppList(
                _('ALL'),
            ),
            items.AppList(
                _('CMS'),
                models=(
                    'wagtail.*',
                    'wagtailmedia.*',
                    'theming.*',
                    'pure_cms.pages.*',
                )
            ),
            items.AppList(
                _('Accounts'),
                models=(
                    'paranuara_challenge.users.*',
                    'django_proximity_roles.*',
                    'paranuara_challenge.accounts.*',
                    'allauth.*',
                    'rest_framework.*',
                    # 'paranuara_challenge.vsinvitations.*',
                    'invitations.*',
                    'actstream.*',
                )
            ),

            items.AppList(
                _('Administration'),
                models=(
                    # 'paranuara_challenge.tracker.*',
                    # 'paranuara_challenge.resources.*',
                    'django.contrib.*',
                )
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomMenu, self).init_with_context(context)
