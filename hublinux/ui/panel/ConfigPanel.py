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

from hublinux.Config import HubLinuxConfig

class ConfigPanel(Gtk.Box):

    def __init__(self):
        super(ConfigPanel, self).__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)

        self.gitDirButton = Gtk.FileChooserButton()
        self.gitDirButton.set_title(_('Choose your local project directory'))
        self.gitDirButton.set_action(Gtk.FileChooserAction.SELECT_FOLDER)

        self.__initUI()

    def __initUI(self):
        # headline
        title = Gtk.Label()
        text = "<span size=\"larger\">%s</span>" % _('git config')
        title.set_markup(text)

        box = Gtk.Box()
        box.pack_start(title, False, True, 0)
        box.pack_start(Gtk.Label(), True, True, 0)
        self.pack_start(box, False, True, 5)

        # localdir
        box = Gtk.Box()
        box.pack_start(Gtk.Label(_('Choose your local project directory:')), False, True, 0)
        box.pack_start(Gtk.Label(), True, True, 0)

        self.pack_start(box, False, True, 0)
        self.pack_start(self.gitDirButton, False, True, 0)

    def doApply(self, *args):
        HubLinuxConfig().gitPath = self.gitDirButton.get_filename()