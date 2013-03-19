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

import abc

class Provider(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def sources(self):
        """
        :return: list of :class: SourceProvider
        """
        return

class SourceProvider(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def image(self):
        return None

    @abc.abstractproperty
    def name(self):
        return None

    @abc.abstractproperty
    def repositories(self):
        return None

class RepositoryProvider(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def name(self):
        return None

    @abc.abstractproperty
    def description(self):
        return None