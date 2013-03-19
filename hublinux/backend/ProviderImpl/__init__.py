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

from gi.repository import GObject, GLib

class Provider(GObject.GObject):

    def __init__(self):
        super(Provider, self).__init__()

    @property
    def sources(self):
        """
        :return: list of :class: SourceProvider
        """
        raise NotImplementedError

class SourceProvider(GObject.GObject):
    __gsignals__ = {
        'add-repository' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,(GObject.TYPE_INT,)),
        'remove-repository' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,()),
        'update-repository' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,())
    }

    def __init__(self):
        self.__repositoryList = []
        self.doScanRepositories()

        super(SourceProvider, self).__init__()

    @property
    def image(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @property
    def repositories(self):
        return self.__repositoryList

    def doScanRepositories(self):
        raise NotImplementedError

    def _getRepositoryProvider(self, repo):
        raise NotImplementedError

    def _findRepository(self, repo):
        def func(self, repo):
            repo = self._getRepositoryProvider(repo)
            if repo not in self.__repositoryList:
                self.__repositoryList.append(repo)
                pos = len(self.__repositoryList) - 1
                self.emit('add-repository', pos)

        GLib.idle_add(func, self, repo)

class RepositoryProvider(GObject.GObject):

    def __eq__(self, other):
        return self.id == other.id

    @property
    def id(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @property
    def description(self):
        raise NotImplementedError