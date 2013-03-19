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
        'add-repository': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
        'remove-repository': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,)),
        'update-repository': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (GObject.TYPE_STRING,))
    }

    def __init__(self):
        # TODO: need persistent caching
        self.__repositoryList = {}
        self.doScanRepositories()

        super(SourceProvider, self).__init__()

    @property
    def image(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    def get_repository(self, id):
        return self.__repositoryList[id]

    @property
    def repositories(self):
        return self.__repositoryList.values()

    def doScanRepositories(self):
        raise NotImplementedError

    def _startScan(self):
        """
        Should be called from doScanRepositories before started
        """
        self.__refoundedRepositories = {}

    def _endScan(self):
        """
        Should be called from doScanRepositories after finished
        """
        for repo in self.repositories:
            if not self.__refoundedRepositories.has_key(repo.id):
                pass
                #self.__repositoryList.pop(repo.id)
                #self.emit('remove-repository', repo.id)

        self.__refoundedRepositories = None

    def _getRepositoryProvider(self, repo):
        raise NotImplementedError

    def _findRepository(self, repo):
        def func(self, repo):
            repo = self._getRepositoryProvider(repo)
            # unknow repo?
            if not self.__repositoryList.has_key(repo.id):
                self.__repositoryList[repo.id] = repo
                self.emit('add-repository', repo.id)
            # any changes in known repo?
            elif self.__repositoryList.has_key(repo.id) and\
                 self.__repositoryList[repo.id].needUpdate(repo):
                self.__repositoryList[repo.id] = repo
                self.emit('update-repository', repo.id)

            if self.__refoundedRepositories is not None:
                self.__refoundedRepositories[repo.id] = repo

        GLib.idle_add(func, self, repo)


class RepositoryProvider(GObject.GObject):
    def needUpdate(self, other):
        """
        return true if the object need a update
        self and other must be the same object -> same id
        """
        if self.id != other.id:
            raise TypeError

        return self.name != other.name and self.description != other.description

    @property
    def id(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @property
    def description(self):
        raise NotImplementedError