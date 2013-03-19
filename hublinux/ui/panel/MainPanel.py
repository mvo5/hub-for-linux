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

from gi.repository import Gtk

from hublinux.ui.widgets.sourcelist import SourceList
from hublinux.ui.widgets.repositorylist import RepositoryList

class MainPanel(Gtk.Box):

    def __init__(self):
        super(MainPanel, self).__init__()
        self.sourceList = SourceList()
        self.repositoryBin = Gtk.Box()

        self.pack_start(self.sourceList, False, True, 15)
        self.pack_start(self.repositoryBin, True, True, 0)

        self.sourceList.addSourceSelectListener(self.__onSourceSelected)
        self.sourceList.loadSources()

    def __setRepositoryWidget(self, widget):
        for w in self.repositoryBin.get_children():
            self.repositoryBin.remove(w)

        self.repositoryBin.pack_start(widget, True, True, 0)
        self.repositoryBin.show_all()

    def __onSourceSelected(self, btn, sourceProvider):
        self.__setRepositoryWidget(RepositoryList(sourceProvider))
        