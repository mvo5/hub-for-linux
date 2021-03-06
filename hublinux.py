#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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

import sys
import logging

from gi.repository import GLib
from hublinux.ui.app import Application

# DEBUG
logging.basicConfig(level=logging.INFO)

GLib.threads_init()

if __name__ == "__main__":
    exit_status = Application().run(sys.argv)
    sys.exit(exit_status)