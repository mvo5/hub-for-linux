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

from gettext import gettext as _

from gi.repository import Gtk

from WelcomePage import WelcomePage
from AccountPage import AccountPage
from ConfigPage import ConfigPage
from SummaryPage import SummaryPage

from hublinux.Constant import APP_NAME, ASSISTANCE_SIZE

class InitialSetupAssistant(Gtk.Assistant):
    def __init__(self, loop):
        super(InitialSetupAssistant, self).__init__()
        self.loop = loop

        self.set_title(_('%s Setup Assistant') % APP_NAME)
        self.set_default_size(ASSISTANCE_SIZE[0], ASSISTANCE_SIZE[1])
        self.set_position(Gtk.WindowPosition.CENTER)

        self.__initUI()
        self.__initSignals()
        self.show_all()

    def __initUI(self):
        # welcome
        self.welcomePage = WelcomePage()
        self.append_page(self.welcomePage)
        self.set_page_title(self.welcomePage, _('Welcome'))
        self.set_page_complete(self.welcomePage, True)
        self.set_page_type(self.welcomePage, Gtk.AssistantPageType.INTRO)

        # account
        self.accountPage = AccountPage(self)
        self.append_page(self.accountPage)
        self.set_page_title(self.accountPage, _('Connect'))
        self.set_page_type(self.accountPage, Gtk.AssistantPageType.CONTENT)

        # configuration
        self.configPage = ConfigPage(self)
        self.append_page(self.configPage)
        self.set_page_title(self.configPage, _('Configuration'))
        self.set_page_type(self.configPage, Gtk.AssistantPageType.CONTENT)

        # summary
        self.summaryPage = SummaryPage()
        self.append_page(self.summaryPage)
        self.set_page_title(self.summaryPage, _('Summary'))
        self.set_page_complete(self.summaryPage, True)
        self.set_page_type(self.summaryPage, Gtk.AssistantPageType.SUMMARY)

    def __initSignals(self):
        self.connect('close', self.loop.quit)
        self.connect('delete-event', self.loop.quit)
        self.connect('cancel', self.loop.quit)