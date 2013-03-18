# -*- coding: utf-8 -*-
# Copyright (C) 2013 Peter Golm
#
# Authors:
#  Peter Golm <golm.peter@gmail.com>
#
# This file is part of hub:linux.
#
# hub:linux is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# hub:linux is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import threading
import logging
from gettext import gettext as _

from gi.repository import GLib, Gtk

from hublinux.backend.Github import Github
from hublinux.Config import HubLinuxConfig

LOG = logging.getLogger(__name__)

class AccountPage(Gtk.Box):
    def __init__(self, assistant):
        super(AccountPage, self).__init__()
        self.assistant = assistant

        self.loginEntry = Gtk.Entry()
        self.loginEntry.set_placeholder_text(_('username/email'))

        self.passwordEntry = Gtk.Entry()
        self.passwordEntry.set_property('hexpand', True)
        self.passwordEntry.set_visibility(False)
        self.passwordEntry.set_placeholder_text(_('password'))

        self.loginButton = Gtk.Button()
        self.loginButton.set_label(_('login'))
        self.loginButton.connect('clicked', self.__doLogin)

        self.__initUi()
        self.__initSignals()

    def __doLogin(self, *args):
        def async(self, login, password):
            isAuthed = Github.isValidCredentials(login, password)

            # save credentials
            if isAuthed:
                HubLinuxConfig().login = login
                HubLinuxConfig().password = password
            else:
                HubLinuxConfig().clearCredentials()

            GLib.idle_add(self.assistant.set_page_complete, self, isAuthed)


        login = self.loginEntry.get_text()
        password = self.passwordEntry.get_text()
        threading.Thread(target=async, args=(self, login, password)).start()

    def __onCancel(self, *args):
        HubLinuxConfig().clearCredentials()

    def __initUi(self):
        self.set_orientation(Gtk.Orientation.VERTICAL)

        # login box
        box = Gtk.Box()
        box.pack_start(Gtk.Label(_('username/email')), False, True, 0)
        box.pack_start(Gtk.Label(), True, True, 0)

        self.loginEntry.set_placeholder_text(_('username/email'))

        self.pack_start(box, False, True, 0)
        self.pack_start(self.loginEntry, False, True, 0)

        # password box
        box = Gtk.Box()
        box.pack_start(Gtk.Label(_('password')), False, True, 0)
        box.pack_start(Gtk.Label(), True, True, 0)

        self.passwordEntry.set_visibility(False)
        self.passwordEntry.set_placeholder_text(_('password'))

        self.pack_start(box, False, True, 0)
        self.pack_start(self.passwordEntry, False, True, 0)

        #login button
        box = Gtk.Box()
        box.pack_start(self.loginButton, False, True, 0)
        box.pack_start(Gtk.Label(), True, True, 0)
        self.pack_start(box, False, True, 0)

    def __initSignals(self):
        self.assistant.connect('delete-event', self.__onCancel)
        self.assistant.connect('cancel', self.__onCancel)