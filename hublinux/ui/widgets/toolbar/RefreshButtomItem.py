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

import logging

from gi.repository import Gtk, GObject

LOG = logging.getLogger(__name__)

class RefreshButtonItem(Gtk.ToolItem):
    class _EventBus(GObject.GObject):
        __gsignals__ = {
            'start-loading' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,()),
            'stop-loading' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,())
        }

        loadCounter = 0
        _instance = None
        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super(RefreshButtonItem._EventBus, cls).__new__(
                    cls, *args, **kwargs)
            return cls._instance

        def __init__(self):
            super(RefreshButtonItem._EventBus, self).__init__()

        def start(self):
            self.loadCounter += 1
            if self.loadCounter > 0:
                self.emit('start-loading')

        def stop(self):
            self.loadCounter -= 1
            if self.loadCounter == 0:
                self.emit('stop-loading')

    def __init__(self):
        super(RefreshButtonItem, self).__init__()
        self.__eventbus = RefreshButtonItem._EventBus()
        self.__lastConnectedRefreshListener = -1

        self.layout = Gtk.Box()
        self.refreshButton = Gtk.Button()
        self.loadingSpinner = Gtk.Spinner()
        self.__onStopLoading()

        self.__eventbus.connect('start-loading', self.__onStartLoading)
        self.__eventbus.connect('stop-loading', self.__onStopLoading)

        self.__initUI()

    @staticmethod
    def startLoading():
        RefreshButtonItem._EventBus().start()

    @staticmethod
    def stopLoading():
        RefreshButtonItem._EventBus().stop()

    def singleConnectRefreshButtonClicked(self, listener):
        if self.__lastConnectedRefreshListener != -1:
            self.refreshButton.disconnect(self.__lastConnectedRefreshListener)

        self.__lastConnectedRefreshListener = self.refreshButton.connect('clicked', listener)
        return self.__lastConnectedRefreshListener

    def __onShow(self):
        self.refreshButton.show()
        self.loadingSpinner.hide()
        self.loadingSpinner.stop()

    def __onStartLoading(self, *args):
        self.refreshButton.hide()
        self.loadingSpinner.show()
        self.loadingSpinner.start()

    def __onStopLoading(self, *args):
        self.refreshButton.show()
        self.loadingSpinner.hide()
        self.loadingSpinner.stop()

    def __initUI(self):
        # button
        icon = Gtk.Image()
        icon.set_from_stock(Gtk.STOCK_REFRESH, Gtk.IconSize.LARGE_TOOLBAR)
        self.refreshButton.set_image(icon)
        self.refreshButton.set_relief(Gtk.ReliefStyle.NONE)

        self.layout.pack_start(self.refreshButton, False, True, 0)
        self.layout.pack_start(self.loadingSpinner, False, True, 10)
        self.add(self.layout)