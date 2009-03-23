from moksha.lib.base import Controller
from moksha.lib.helpers import Category, MokshaApp, Not, not_anonymous, MokshaWidget
from moksha.api.widgets import ContextAwareWidget, Grid
from moksha.api.widgets.containers import DashboardContainer

from repoze.what.predicates import not_anonymous
from tg import expose, tmpl_context, require, request

class UserMembershipsGrid(Grid, ContextAwareWidget):
    template='mako:fedoracommunity.mokshaapps.people.templates.memberships_table_widget'

class ProfileContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('header-content-column',
                       MokshaApp('', 'fedoracommunity.people/details',
                                 params={'compact': True,
                                         'profile': True}),
                       css_class='header-content-column'
                       ),
              Category('right-content-column',
                       (MokshaApp('Your Packages', 'fedoracommunity.packages/mypackages'),
                        MokshaApp('Alerts', 'fedoracommunity.alerts'),
                        MokshaApp('Quick Links', 'fedoracommunity.quicklinks')),
                        default_child_css="panel",
                        css_class='right-content-column'
                      ),
              Category('left-content-column',
                       (MokshaApp('Your Group Memberships',
                                 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 10,
                                         "filters":{"profile": True,
                                                    "unapproved": False}
                                        }
                                 ),
                        MokshaApp('Your Unapproved Group Memberships',
                                 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 5,
                                         "filters":{"profile": True,
                                                    "approved": False}
                                        }
                                 )
                       ),
                       css_class='left-content-column'
                      )]

class PeopleContainer(DashboardContainer, ContextAwareWidget):
    layout = [Category('header-content-column',
                       MokshaApp('', 'fedoracommunity.people/details',
                                 params={'username':'',
                                         'compact': True})
                       ),
              Category('right-content-column',
                        (MokshaApp('Packages', 'fedoracommunity.packages/userpackages',
                                  params={'username':''}),
                         MokshaApp('Alerts', 'fedoracommunity.alerts'),
                         MokshaApp('Quick Links', 'fedoracommunity.quicklinks'))
                        ),
              Category('left-content-column',
                       (MokshaApp('Group Memberships', 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 10,
                                         "filters":{"username":'',
                                                    "unapproved": False}
                                        }
                                 ),

                        MokshaApp('Unapproved Group Memberships', 'fedoracommunity.people/memberships/table',
                                 params={"rows_per_page": 5,
                                         "filters":{"username":'',
                                                    "approved": False}
                                        }
                                 ),
                        )
                       )]

memberships_grid = UserMembershipsGrid('user_memberships')
people_memberships_container = PeopleContainer('people_memberships_container')
profile_memberships_container = ProfileContainer('profile_memberships_container')

class MembershipsController(Controller):
    @expose('mako:moksha.templates.widget')
    @require(not_anonymous())
    def index(self, **kwds):
        options = {
            'username': kwds.get('username', kwds.get('u')),
            'profile': kwds.get('profile')
        }

        if options['profile']:
            tmpl_context.widget = profile_memberships_container
        elif options['username']:
            tmpl_context.widget = people_memberships_container

        return {'options': options}

    @expose('mako:fedoracommunity.mokshaapps.people.templates.memberships_table')
    @require(not_anonymous())
    def table(self, uid="", rows_per_page=5, filters={}):
        if isinstance(rows_per_page, basestring):
            rows_per_page = int(rows_per_page)

        tmpl_context.widget = memberships_grid
        return {'filters': filters, 'uid':uid, 'rows_per_page':rows_per_page}