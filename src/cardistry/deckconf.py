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
    cnt="(disabled)"
    msg=""
    lim=self.young_card_limit.value()
    if lim:
        cur=mw.col.decks.current()
        yCnt=getYoungCardCnt(cur['id'])

        if yCnt:
            pLim=getParentLim(cur)
            nCnt=getNewCardCnt(cur['id'])
            npd=self.newPerDay.value()

            cmin=self.cardistry_min.value()
            cpd=min(pLim,npd,max(0,cmin,lim-yCnt))

            d2g=nCnt//(cpd or 1)
            cnt="(%d young/lrn outstanding)"%yCnt
            msg="(%d per day, ~%d days to go)"%(cpd,d2g or 1)
        else:
            cnt="Done! or is a parent deck"
            msg=""

        self.cardistry_min.setDisabled(False)
    else:
        self.cardistry_min.setDisabled(True)
    self.young_card_cnt.setText(_(cnt))
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
    self.young_card_cnt=QtWidgets.QLabel(self.tab)
    self.gridLayout.addWidget(self.young_card_cnt,r,2,1,1)

    r+=1
    label=QtWidgets.QLabel(self.tab)
    label.setText(_("Do at least:"))
    self.gridLayout.addWidget(label,r,0,1,1)
    self.young_card_msg=QtWidgets.QLabel(self.tab)
    self.gridLayout.addWidget(self.young_card_msg,r,2,1,1)

    self.cardistry_min=QtWidgets.QSpinBox(self.tab)
    self.cardistry_min.setMinimum(0)
    self.cardistry_min.setMaximum(999)
    self.cardistry_min.setSingleStep(1)
    self.cardistry_min.valueChanged.connect(lambda:valuechange(self))
    self.gridLayout.addWidget(self.cardistry_min,r,1,1,1)


def loadConf(self):
    lim=self.conf.get("young_card_limit", 0)
    self.form.young_card_limit.setValue(lim)
    lim=self.conf.get("cardistry_min", 0)
    self.form.cardistry_min.setValue(lim)
    valuechange(self.form)


def saveConf(self):
    valuechange(self.form)
    self.conf['young_card_limit']=self.form.young_card_limit.value()
    self.conf['cardistry_min']=self.form.cardistry_min.value()


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
