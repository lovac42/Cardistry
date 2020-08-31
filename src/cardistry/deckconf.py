# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Cardistry
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import aqt
import aqt.deckconf
from aqt import mw
from anki.hooks import wrap
from anki.lang import _
from aqt.qt import *

from .lib.com.lovac42.anki.version import ANKI20, CCBC
from .utils import getYoungCardCnt, getNewCardCnt

if ANKI20 or CCBC:
    from PyQt4 import QtCore, QtGui as QtWidgets
else:
    from PyQt5 import QtCore, QtGui, QtWidgets


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
        # ivl=self.cardistry_ivl.value()
        # fil=self.cardistry_filter.checkState()
        yCnt=getYoungCardCnt(cur['id'])

        if yCnt:
            pLim=getParentLim(cur)
            nCnt=getNewCardCnt(cur['id'])
            npd=self.newPerDay.value()

            cpd=min(pLim,npd,max(0,lim-yCnt))
            d2g=nCnt//(cpd or 1)
            msg="(%d per day, ~%d days to go, %d young/lrn)"%(cpd,d2g or 1,yCnt)
        else:
            msg="Done! or is a parent deck"

        # self.cardistry_ivl.setDisabled(False)
        # self.cardistry_filter.setDisabled(False)
    # else:
        # self.cardistry_ivl.setDisabled(True)
        # self.cardistry_filter.setDisabled(True)
    self.young_card_msg.setText(_(msg))




def dconfsetupUi(self, Dialog):
    r=self.gridLayout.rowCount()

    label=QtWidgets.QLabel(self.tab)
    label.setText(_("Lrn/Yng Cards:"))
    self.gridLayout.addWidget(label,r,0,1,1)

    self.young_card_limit=QtWidgets.QSpinBox(self.tab)
    self.young_card_limit.setMinimum(0)
    self.young_card_limit.setMaximum(9999)
    self.young_card_limit.setSingleStep(1)
    self.gridLayout.addWidget(self.young_card_limit,r,1,1,1)

    self.newPerDay.valueChanged.connect(lambda:valuechange(self))
    self.young_card_limit.valueChanged.connect(lambda:valuechange(self))
    self.young_card_msg=QtWidgets.QLabel(self.tab)
    self.gridLayout.addWidget(self.young_card_msg,r,2,1,1)

    r+=1
    label=QtWidgets.QLabel(self.tab)
    label.setText(_("Mature IVL:"))
    self.gridLayout.addWidget(label,r,0,1,1)

    # self.cardistry_ivl=QtWidgets.QSpinBox(self.tab)
    # self.cardistry_ivl.setMinimum(1)
    # self.cardistry_ivl.setMaximum(999)
    # self.cardistry_ivl.setSingleStep(1)
    # self.cardistry_ivl.valueChanged.connect(lambda:valuechange(self))
    # self.gridLayout.addWidget(self.cardistry_ivl,r,1,1,1)

    # self.cardistry_filter=QtWidgets.QCheckBox(self.tab)
    # self.cardistry_filter.setText(_('count cards in filter decks?'))
    # self.cardistry_filter.clicked.connect(lambda:valuechange(self))
    # self.gridLayout.addWidget(self.cardistry_filter,r,2,1,3)


def loadConf(self):
    lim=self.conf.get("young_card_limit", 0)
    self.form.young_card_limit.setValue(lim)
    # lim=self.conf.get("cardistry_ivl", 21)
    # self.form.cardistry_ivl.setValue(lim)
    # cb=self.conf.get("cardistry_filter", 0)
    # self.form.cardistry_filter.setCheckState(cb)
    valuechange(self.form)


def saveConf(self):
    valuechange(self.form)
    self.conf['young_card_limit']=self.form.young_card_limit.value()
    # self.conf['cardistry_ivl']=self.form.cardistry_ivl.value()
    # self.conf['cardistry_filter']=self.form.cardistry_filter.checkState()


aqt.forms.dconf.Ui_Dialog.setupUi = wrap(
    aqt.forms.dconf.Ui_Dialog.setupUi,
    dconfsetupUi, pos="after"
)

aqt.deckconf.DeckConf.loadConf = wrap(
    aqt.deckconf.DeckConf.loadConf,
    loadConf, pos="after"
)

aqt.deckconf.DeckConf.saveConf = wrap(
    aqt.deckconf.DeckConf.saveConf,
    saveConf, pos="before"
)
