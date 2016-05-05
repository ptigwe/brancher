# -*- coding: utf-8 -*-

# Copyright (C) 2015 Tobenna Peter Igwe.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import depend
depend.check_dependencies()

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
import aqt
from brancher.anki_bridge import brancherInstance

aqt.mw.brancher = brancherInstance
action = QAction("Brancher", mw)
mw.connect(action, SIGNAL("triggered()"), aqt.mw.brancher.show)
mw.form.menuTools.addAction(action)
