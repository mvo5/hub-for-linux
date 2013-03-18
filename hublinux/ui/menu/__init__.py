# -*- coding: utf-8 -*-
# Copyright (C) 2013 Peter Golm
#
# Authors:
#  Peter Golm <golm.peter@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import logging
from gettext import gettext as _

from gi.repository import Gio

from hublinux.Config import HubLinuxConfig

LOG = logging.getLogger(__name__)

class ToolbarMenu(Gio.Menu):
    def __init__(self, app):
        super(ToolbarMenu, self).__init__()
        self.application = app
        self.__initUI()

    def __initUI(self):
        self.append(_('Settings'), 'app.settings')

        exitMenu = Gio.Menu()
        exitMenu.append(_('Logout'), 'app.logout')
        exitMenu.append(_('Close'), 'app.close')
        exitMenu.append(_('Quit'), 'app.quit')

        self.append_section(None, exitMenu)

        logoutAction = Gio.SimpleAction.new("logout", None)
        logoutAction.connect("activate", self.__onLogoutClick)
        self.application.add_action(logoutAction)

    def __onLogoutClick(self, *args):
        HubLinuxConfig().clearCredentials()
        LOG.info("credentials cleared -> Exit now")
        self.application.activate_action('quit', None)
