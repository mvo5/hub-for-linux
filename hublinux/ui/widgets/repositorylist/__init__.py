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
import logging

from gi.repository import Gtk, GLib

LOG = logging.getLogger(__name__)

class RepositoryList(Gtk.Box):

    def __init__(self, sourceProvider):
        super(RepositoryList, self).__init__()
        self.sourceProvider = sourceProvider

        self.searchEntry = Gtk.SearchEntry()
        self.sourceStore = Gtk.ListStore(str)

        self.sourceList = Gtk.TreeView(self.sourceStore.filter_new())

        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.sourceList.set_headers_visible(False)

        self.__initUI()
        self.sourceProvider.connect('add-repository', self.__onAddRepository)
        self.sourceProvider.connect('remove-repository', self.__onRemoveRepository)
        self.sourceProvider.connect('update-repository', self.__onUpdateRepository)
        self.searchEntry.connect('changed', self.__onChange)

        self.__loadList()

    def __onAddRepository(self, provider, id):
        self.__addRepository(provider.get_repository(id))

    def __onRemoveRepository(self, provider, id):
        LOG.info('onRemoveRepo(%s)' % id)

    def __onUpdateRepository(self, provider, id):
        LOG.info('onUpdateRepo(%s)' % id)

    def __addRepository(self, repo):
        text = "<span weight=\"bold\">%s</span>\n<span size=\"smaller\" weight=\"light\">%s</span>" % (
            repo.name, repo.description)
        self.sourceStore.append([text])

        self.sourceList.set_model(self.sourceStore.filter_new())
        self.__setFilter()
        self.sourceList.show_all()

    def __setFilter(self):
        def filter_func(model, iter, *args):
            search = '.*' + self.searchEntry.get_text().lower() + '.*'
            return re.match(search, model.get_value(iter, 0).lower()) is not None
        self.sourceList.get_model().set_visible_func(filter_func)

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
        for repo in self.sourceProvider.repositories:
            self.__addRepository(repo)

