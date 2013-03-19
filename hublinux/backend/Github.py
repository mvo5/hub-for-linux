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

import httplib2

import github

#noinspection PyUnresolvedReferences
from gi.repository import GLib
from gi.repository.GdkPixbuf import PixbufLoader, InterpType

from hublinux.Constant import CACHE_DIR
from hublinux.Config import HubLinuxConfig

from hublinux.ui.widgets.toolbar.RefreshButtomItem import RefreshButtonItem

class Github(object):

    @staticmethod
    def getGithub(login=None, password=None):
        if login is None or password is None:
            login = HubLinuxConfig().login
            password = HubLinuxConfig().password

        return github.Github(login_or_token=login, password=password)

    @staticmethod
    def isValidCredentials(login, password):
        #noinspection PyBroadException
        try:
            return Github.getGithub(login, password).get_user().name is not None
        except Exception:
            pass
        return False

    @staticmethod
    def getAvatarPixbuf(avatarObj=None, size=None):
        GLib.idle_add(RefreshButtonItem.startLoading)# start loading indicator
        if avatarObj is None:
            avatarObj = Github.getGithub().get_user()

        url = avatarObj.avatar_url

        client = httplib2.Http(cache=CACHE_DIR)
        resp, content = client.request(url)

        loader = PixbufLoader()
        loader.write(content)
        loader.close()

        GLib.idle_add(RefreshButtonItem.stopLoading)# stop loading indicator
        if size is None:
            return loader.get_pixbuf()
        else:
            return loader.get_pixbuf().scale_simple(size[0], size[1], InterpType.BILINEAR)
