# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Cardistry
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.2



# CONFIGS ############################

YOUNG_CARD_IVL = 21
INCLUDE_FILTERED_DECKS = True

# END CONFIGS ########################


from aqt import mw
from anki.hooks import wrap
from anki.sched import Scheduler


## MONKEY PATCHES ##
def deckNewLimitSingle(self, d, _old):
    if d['dyn']: return self.reportLimit

    c=self.col.decks.confForDid(d['id'])
    newMax = max(0, c['new']['perDay'] - d['newToday'][1])
    youngMax = c.get("young_card_limit", 0)
    if youngMax==0 or newMax==0: return newMax

    sql_odid=''
    if INCLUDE_FILTERED_DECKS:
        sql_odid='or odid=%d'%d['id']

    cnt = self.col.db.first("""select 
sum(case when queue > 0 and ivl < ? then 1 else 0 end)
from cards where did=? %s"""%sql_odid, YOUNG_CARD_IVL, d['id'])

    youngCnt =  cnt[0] or 0
    paddingCnt = max(0, youngMax-youngCnt-d['newToday'][1])
    return min(newMax, paddingCnt)


Scheduler._deckNewLimitSingle = wrap(Scheduler._deckNewLimitSingle, deckNewLimitSingle, 'around')



##################################################
#
#  GUI stuff, adds deck menu options to enable/disable
#  this addon for specific decks
#
#################################################
import aqt
import aqt.deckconf
from aqt.qt import *

from anki import version
ANKI21 = version.startswith("2.1.")
if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


def dconfsetupUi(self, Dialog):
    r=self.gridLayout.rowCount()

    #ShowAnswer Timeout limit
    self.young_card_label = QtWidgets.QLabel(self.tab_3)
    self.young_card_label.setObjectName(_fromUtf8("young_card_label"))
    self.young_card_label.setText(_("New/Young Cards:"))
    self.gridLayout.addWidget(self.young_card_label, r, 0, 1, 1)
    self.young_card_limit = QtWidgets.QSpinBox(self.tab_3)
    self.young_card_limit.setMinimum(0)
    self.young_card_limit.setMaximum(9999)
    self.young_card_limit.setSingleStep(5)
    self.young_card_limit.setObjectName(_fromUtf8("young_card_limit"))
    self.gridLayout.addWidget(self.young_card_limit, r, 1, 1, 1)


def loadConf(self):
    lim=self.conf.get("young_card_limit", 0)
    self.form.young_card_limit.setValue(lim)

def saveConf(self):
    self.conf['young_card_limit']=self.form.young_card_limit.value()

aqt.forms.dconf.Ui_Dialog.setupUi = wrap(aqt.forms.dconf.Ui_Dialog.setupUi, dconfsetupUi, pos="after")
aqt.deckconf.DeckConf.loadConf = wrap(aqt.deckconf.DeckConf.loadConf, loadConf, pos="after")
aqt.deckconf.DeckConf.saveConf = wrap(aqt.deckconf.DeckConf.saveConf, saveConf, pos="before")
