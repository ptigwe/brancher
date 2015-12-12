from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
import aqt
from brancher.anki_bridge import brancherInstance

aqt.mw.brancher = brancherInstance
action = QAction("Brancher", mw)
mw.connect(action, SIGNAL("triggered()"), aqt.mw.brancher.show)
mw.form.menuTools.addAction(action)
