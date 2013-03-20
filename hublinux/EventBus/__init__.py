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

from threading import Lock
from gi.repository import GObject

class LoadingEventBus(GObject.GObject):
    __gsignals__ = {
        'start-loading' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,()),
        'stop-loading' : (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,())
    }

    __loadCounter = 0
    __loadCounterLock=Lock()
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoadingEventBus, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super(LoadingEventBus, self).__init__()

    def start(self):
        self.__loadCounterLock.acquire()

        self.__loadCounter += 1
        if self.__loadCounter > 0:
            self.emit('start-loading')

        self.__loadCounterLock.release()

    def stop(self):
        self.__loadCounterLock.acquire()

        self.__loadCounter -= 1
        if self.__loadCounter == 0:
            self.emit('stop-loading')

        self.__loadCounterLock.release()
