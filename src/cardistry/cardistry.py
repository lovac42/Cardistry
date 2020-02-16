# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Cardistry
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from anki.hooks import wrap, addHook
from anki.utils import ids2str

from anki import version
ANKI21=version.startswith("2.1.")


def getYoungCardCnt(did, mIvl, incFilter):
    "count lrn or burried only, no suspended"
    sql_odid='or odid = %d'%did if incFilter else ''
    cnt=mw.col.db.first("""
Select count() from cards where
type in (1,2,3) and queue in (1,2,3,4,-2,-3)
and ivl < ? and (did = ? %s)
"""%sql_odid,mIvl,did)[0]
    return cnt or 0



## MONKEY PATCHES ##
def deckNewLimitSingle(sched, d, _old):
    newMax=_old(sched,d)
    if d['dyn'] or mw.state == "sync":
        return newMax

    c=sched.col.decks.confForDid(d['id'])
    youngMax=c.get("young_card_limit",0)
    if not youngMax or not newMax:
        return newMax

    incFilter=c.get("cardistry_filter",0)
    mIvl=c.get("cardistry_ivl",21)
    youngCnt=getYoungCardCnt(d['id'], mIvl, incFilter)

    paddingCnt=max(0,youngMax-youngCnt-d['newToday'][1])
    penetration=min(newMax, paddingCnt)
    # print(str(d['id'])+';;'+str(penetration)+';;'+d['name']) #debug: print to cvs
    return penetration


import anki.sched
anki.sched.Scheduler._deckNewLimitSingle = wrap(anki.sched.Scheduler._deckNewLimitSingle, deckNewLimitSingle, 'around')
if ANKI21:
    import anki.schedv2
    anki.schedv2.Scheduler._deckNewLimitSingle = wrap(anki.schedv2.Scheduler._deckNewLimitSingle, deckNewLimitSingle, 'around')




##################################################
#
#  GUI stuff, adds deck menu options to enable/disable
#  this addon for specific decks
#
#################################################
import aqt
import aqt.deckconf
from anki.lang import _
from aqt.qt import *

if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets


def getNewCardCnt(did, incFilter):
    "count new or burried only, no suspended"
    sql_odid='or odid = %d'%did if incFilter else ''
    cnt=mw.col.db.first("""
Select count() from cards where
type = 0 and queue in (0,-2,-3)
and (did = ? %s)"""%sql_odid,did)[0]
    return cnt or 0


def getParentLim(deck):
    lim=9999
    if "::" in deck['name']:
        for d in mw.col.decks.parents(deck['id']):
            conf=mw.col.decks.confForDid(d['id'])
            npd=conf['new']['perDay']
            lim=min(npd,lim)
    return lim


def valuechange(self):
    msg='(disabled)'
    lim=self.young_card_limit.value()
    if lim:
        cur=mw.col.decks.current()
        ivl=self.cardistry_ivl.value()
        fil=self.cardistry_filter.checkState()
        yCnt=getYoungCardCnt(cur['id'], ivl, fil)

        if yCnt:
            pLim=getParentLim(cur)
            nCnt=getNewCardCnt(cur['id'],fil)
            npd=self.newPerDay.value()

            cpd=min(pLim,npd,max(0,lim-yCnt))
            d2g=nCnt//(cpd or 1)
            msg="(%d per day, ~%d days to go, %d young/lrn)"%(cpd,d2g or 1,yCnt)
        else:
            msg="Done! or is a parent deck"

        self.cardistry_ivl.setDisabled(False)
        self.cardistry_filter.setDisabled(False)
    else:
        self.cardistry_ivl.setDisabled(True)
        self.cardistry_filter.setDisabled(True)
    self.young_card_msg.setText(_(msg))


def dconfsetupUi(self, Dialog):
    r=self.gridLayout.rowCount()

    label=QtWidgets.QLabel(self.tab)
    label.setText(_("Lrn/Yng Cards:"))
    self.gridLayout.addWidget(label,r,0,1,1)

    self.young_card_limit=QtWidgets.QSpinBox(self.tab)
    self.young_card_limit.setMinimum(0)
    self.young_card_limit.setMaximum(9999)
    self.young_card_limit.setSingleStep(5)
    self.gridLayout.addWidget(self.young_card_limit,r,1,1,1)

    self.newPerDay.valueChanged.connect(lambda:valuechange(self))
    self.young_card_limit.valueChanged.connect(lambda:valuechange(self))
    self.young_card_msg=QtWidgets.QLabel(self.tab)
    self.gridLayout.addWidget(self.young_card_msg,r,2,1,1)

    r+=1
    label=QtWidgets.QLabel(self.tab)
    label.setText(_("Mature IVL:"))
    self.gridLayout.addWidget(label,r,0,1,1)

    self.cardistry_ivl=QtWidgets.QSpinBox(self.tab)
    self.cardistry_ivl.setMinimum(1)
    self.cardistry_ivl.setMaximum(999)
    self.cardistry_ivl.setSingleStep(1)
    self.cardistry_ivl.valueChanged.connect(lambda:valuechange(self))
    self.gridLayout.addWidget(self.cardistry_ivl,r,1,1,1)

    self.cardistry_filter=QtWidgets.QCheckBox(self.tab)
    self.cardistry_filter.setText(_('count cards in filter decks?'))
    self.cardistry_filter.clicked.connect(lambda:valuechange(self))
    self.gridLayout.addWidget(self.cardistry_filter,r,2,1,3)



def loadConf(self):
    lim=self.conf.get("young_card_limit", 0)
    self.form.young_card_limit.setValue(lim)
    lim=self.conf.get("cardistry_ivl", 21)
    self.form.cardistry_ivl.setValue(lim)
    cb=self.conf.get("cardistry_filter", 0)
    self.form.cardistry_filter.setCheckState(cb)
    valuechange(self.form)

def saveConf(self):
    valuechange(self.form)
    self.conf['young_card_limit']=self.form.young_card_limit.value()
    self.conf['cardistry_ivl']=self.form.cardistry_ivl.value()
    self.conf['cardistry_filter']=self.form.cardistry_filter.checkState()


aqt.forms.dconf.Ui_Dialog.setupUi = wrap(aqt.forms.dconf.Ui_Dialog.setupUi, dconfsetupUi, pos="after")
aqt.deckconf.DeckConf.loadConf = wrap(aqt.deckconf.DeckConf.loadConf, loadConf, pos="after")
aqt.deckconf.DeckConf.saveConf = wrap(aqt.deckconf.DeckConf.saveConf, saveConf, pos="before")
