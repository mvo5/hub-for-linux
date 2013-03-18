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

from gettext import gettext as _

from gi.repository import Gio

class AppMenu(Gio.Menu):

    def __init__(self, app):
        super(AppMenu, self).__init__()
        self.application = app

        self.append(_('Close'), 'app.close')
        self.append(_('Quit'), 'app.quit')



        closeAction = Gio.SimpleAction.new("close", None)
        closeAction.connect("activate", self.__onCloseClick)
        self.application.add_action(closeAction)

        quitAction = Gio.SimpleAction.new("quit", None)
        quitAction.connect("activate", self.__onQuitClick)
        self.application.add_action(quitAction)

    def __onCloseClick(self, *args):
        self.application.window.hide()

    def __onQuitClick(self, *args):
        self.application.quit()
