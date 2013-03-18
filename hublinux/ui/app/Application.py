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

import os
import logging
from gettext import gettext as _

from gi.repository import GLib, Gtk, Notify

from hublinux.Constant import APP_ID, APP_NAME

from hublinux.ui.menu.AppMenu import AppMenu
from hublinux.ui.app.Window import Window

from hublinux.ui.assistant import InitialSetupAssistant

from hublinux.Config import HubLinuxConfig

LOG = logging.getLogger(__name__)

class Application(Gtk.Application):
    def __init__(self):
        super(Application, self).__init__()

        self.appMenu = AppMenu(self)
        self.set_application_id(APP_ID)

    @property
    def window(self):
        return self.appWindow

    def do_activate(self):
        # only one instance
        if len(self.get_windows()) > 0:
            image = os.path.realpath("../assets/icon.png")
            Notify.init(APP_NAME)
            notification = Notify.Notification.new(
                APP_NAME,
                _('Another instance of %(name)s is running. You can start %(name)s only once.') % {'name': APP_NAME},
                image
            )
            notification.show()
            return

        # start setup if no login
        if not HubLinuxConfig().hasLogin:
            loop = GLib.MainLoop(GLib.main_context_default())
            assistance = InitialSetupAssistant(loop)
            assistance.show()
            loop.run()

        # setup canceled?
        if HubLinuxConfig().hasLogin:
            self.set_app_menu(self.appMenu)
            self.appWindow = Window(self)
            self.appWindow.show_all()
        else:
            LOG.warning("No login credentials -> Exit")

    def do_startup(self):
        Gtk.Application.do_startup(self)