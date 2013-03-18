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

from gi.repository import Gtk, GLib

from hublinux.backend.Github import Github

class ProfileImageToolItem(Gtk.ToolItem):
    def __init__(self):
        super(ProfileImageToolItem, self).__init__()

        self.layout = Gtk.Box()
        self.image = Gtk.Image()
        self.layout.pack_start(self.image, False, True, 0)

        self.add(self.layout)
        self.loadProfile()

    def loadProfile(self):
        def async(self):
            imagePixbuf = Github.getAvatarPixbuf(Github.getGithub().get_user(), (32, 32))
            GLib.idle_add(self.image.set_from_pixbuf, imagePixbuf)

        threading.Thread(target=async, args=(self,)).start()