# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Cardistry
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


#####################
# ALPHA VERSION:
# Shows count on SELECTED deck from deck list
#####################

from aqt import mw
from aqt.utils import showText
from aqt.qt import *


from anki import version
ANKI21=version.startswith("2.1.")


class CardistryCount:
    def __init__(self):
        menu=None
        for a in mw.form.menubar.actions():
            if '&Study' == a.text():
                menu=a.menu()
                # menu.addSeparator()
                break
        if not menu:
            menu=mw.form.menubar.addMenu('&Study')

        qact=QAction("Cardistry: Show Count", mw)
        qact.triggered.connect(self.show)
        menu.addAction(qact)


    def show(self):
        arr=[]
        for did in mw.col.decks.active():
            name=mw.col.decks.name(did)
            deck=mw.col.decks.get(did)
            nCnt=deck['newToday'][1]
            rCnt=deck['revToday'][1]
            arr.append("%04d;;%05d;;%d;;%s"%(nCnt,rCnt,did,name))
        showText('\n'.join(arr))


cc=CardistryCount()
