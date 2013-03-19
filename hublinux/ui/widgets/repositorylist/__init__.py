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

import re
import threading

from gi.repository import Gtk, GLib

class RepositoryList(Gtk.Box):
    def __init__(self, sourceProvider):
        super(RepositoryList, self).__init__()
        self.sourceProvider = sourceProvider

        self.searchEntry = Gtk.SearchEntry()
        self.sourceStore = Gtk.ListStore(str)
        self.sourceList = Gtk.TreeView(self.sourceStore)

        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.sourceList.set_headers_visible(False)

        self.__initUI()
        self.__loadList()
        self.searchEntry.connect('changed', self.__onChange)

    def __onChange(self, data):
            if isinstance(self.sourceList.get_model(), Gtk.TreeModelFilter):
                self.sourceList.get_model().refilter()

    def __initUI(self):
        self.pack_start(self.searchEntry, False, True, 0)

        # text
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('', renderer, markup=0)
        column.set_property('expand', True)
        self.sourceList.append_column(column)

        sourceScroll = Gtk.ScrolledWindow()
        sourceScroll.add(self.sourceList)
        self.pack_start(sourceScroll, True, True, 0)

    def __loadList(self):
        self.searchEntry.set_text('')
        newStore = Gtk.ListStore(str)

        def async(self):
            for repository in self.sourceProvider.repositories:
                text = "<span weight=\"bold\">%s</span>\n<span size=\"smaller\" weight=\"light\">%s</span>" % (
                    repository.name, repository.description)
                newStore.append([text])

            def filter_func(model, iter, *args):
                search = '.*' + self.searchEntry.get_text().lower() + '.*'
                return re.match(search, model.get_value(iter, 0).lower()) is not None

            filter = newStore.filter_new()

            GLib.idle_add(filter.set_visible_func, filter_func)
            GLib.idle_add(self.sourceList.set_model, filter)
            GLib.idle_add(self.sourceList.show)

        threading.Thread(target=async, args=(self, )).start()
