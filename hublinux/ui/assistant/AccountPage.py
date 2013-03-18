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

        # login ui
        self.loginEntry = Gtk.Entry()
        self.loginEntry.set_placeholder_text(_('username/email'))

        self.passwordEntry = Gtk.Entry()
        self.passwordEntry.set_property('hexpand', True)
        self.passwordEntry.set_visibility(False)
        self.passwordEntry.set_placeholder_text(_('password'))

        self.loginButton = Gtk.Button()

        # profile ui
        self.loadProfileSpinner = Gtk.Spinner();
        self.profileLabel = Gtk.Label()

        self.logoutButton = Gtk.Button()

        self.__initLoginUi()
        self.__initSignals()

    def __doLogin(self, *args):
        self.__clearUI()
        self.__initProfileUI()

        def async(self, login, password):
            isAuthed = Github.isValidCredentials(login, password)

            # save credentials
            if isAuthed:
                HubLinuxConfig().login = login
                HubLinuxConfig().password = password
                GLib.idle_add(self.__loadProfile)
            else:
                HubLinuxConfig().clearCredentials()
                GLib.idle_add(self.__clearUI)
                GLib.idle_add(self.__initLoginUi)

            GLib.idle_add(self.assistant.set_page_complete, self, isAuthed)


        login = self.loginEntry.get_text()
        password = self.passwordEntry.get_text()
        threading.Thread(target=async, args=(self, login, password)).start()

    def __loadProfile(self):
        def async(self):
            user = Github.getGithub().get_user()

            text = '<b>' + user.name + '</b>\n'
            text += _('%s plan (%i private repositories)') % (user.plan.name, user.total_private_repos)

            GLib.idle_add(self.profileLabel.set_markup, text)
            GLib.idle_add(self.loadProfileSpinner.stop)
            GLib.idle_add(self.loadProfileSpinner.hide)

        threading.Thread(target=async, args=(self, )).start()

    def __doLogout(self, *args):
        HubLinuxConfig().clearCredentials()
        self.assistant.set_page_complete(self, False)
        self.__clearUI()
        self.__initLoginUi()

    def __onCancel(self, *args):
        HubLinuxConfig().clearCredentials()

    def __clearUI(self):
        childWidgets = self.get_children()
        for widget in childWidgets:
            self.remove(widget)

    def __initLoginUi(self):
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
        self.loginButton.set_label(_('login'))
        self.loginButton.connect('clicked', self.__doLogin)

        box = Gtk.Box()
        box.pack_start(self.loginButton, False, True, 0)
        box.pack_start(Gtk.Label(), True, True, 0)
        self.pack_start(box, False, True, 0)

        self.show_all()

    def __initProfileUI(self):
        # init profile
        title = Gtk.Label()
        text = "<span size=\"larger\">%s</span>" % _('logged in as')
        title.set_markup(text)

        box = Gtk.Box()
        box.pack_start(title, False, True, 0)
        box.pack_start(Gtk.Label(), True, True, 0)
        self.pack_start(box, False, True, 10)

        profileBox = Gtk.Box()
        profileBox.pack_start(self.loadProfileSpinner, False, True, 0)
        #self.profileBox.pack_start(self.avatarImage, False, True, 0)
        profileBox.pack_start(self.profileLabel, False, True, 5)

        self.pack_start(profileBox, False, True, 0)

        # logout button
        self.logoutButton.set_label(_('logout'))
        self.logoutButton.connect('clicked', self.__doLogout)

        box = Gtk.Box()
        box.pack_start(self.logoutButton, False, True, 0)
        box.pack_start(Gtk.Label(), True, True, 0)
        self.pack_start(box, False, True, 0)

        #some space
        self.pack_start(Gtk.Label(), False, True, 5)

        self.show_all()
        self.loadProfileSpinner.start()

    def __initSignals(self):
        self.assistant.connect('delete-event', self.__onCancel)
        self.assistant.connect('cancel', self.__onCancel)