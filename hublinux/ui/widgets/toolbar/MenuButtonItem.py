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

from gi.repository import Gtk, Gio

from hublinux.ui.menu import ToolbarMenu
class MenuButtonItem(Gtk.ToolItem):

    def __init__(self):
        super(MenuButtonItem, self).__init__()

        self.__initUI()

    def __initUI(self):
        self.menuButton = Gtk.MenuButton()

        icon = Gtk.Image()
        icon.set_from_stock(Gtk.STOCK_PROPERTIES, Gtk.IconSize.LARGE_TOOLBAR)
        self.menuButton.set_image(icon)
        self.menuButton.set_halign(Gtk.Align.END) # FIXME: don't work, why?
        self.menuButton.set_menu_model(ToolbarMenu())
        self.menuButton.set_relief(Gtk.ReliefStyle.NONE)

        self.add(self.menuButton)