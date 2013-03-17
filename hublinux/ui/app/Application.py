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
from gettext import gettext as _

from gi.repository import Gtk, Notify

from hublinux.Constant import APP_ID, APP_NAME

from hublinux.ui.app.AppMenu import AppMenu
from hublinux.ui.app.Window import Window

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
                _('Another instance of %s is running. You can start %s only once.') % (APP_NAME, APP_NAME),
                image
            )
            notification.show()
            return

        self.set_app_menu(self.appMenu)

        self.appWindow = Window(self)
        self.appWindow.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)