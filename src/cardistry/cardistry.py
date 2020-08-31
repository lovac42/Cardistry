# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Cardistry
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from anki.hooks import wrap, addHook
from anki.utils import ids2str

from .lib.com.lovac42.anki.version import ANKI20
from .utils import getYoungCardCnt


def deckNewLimitSingle(sched, d, _old):
    newMax=_old(sched,d)
    if d['dyn'] or mw.state == "sync":
        return newMax

    c=sched.col.decks.confForDid(d['id'])
    youngMax=c.get("young_card_limit", 0)
    if not youngMax or not newMax:
        return newMax

    incFilter=c.get("cardistry_filter", 0)
    # mIvl=c.get("cardistry_ivl", 21)
    youngCnt=getYoungCardCnt(d['id'], incFilter)

    paddingCnt=max(0,youngMax-youngCnt-d['newToday'][1])
    penetration=min(newMax, paddingCnt)

    # print(str(d['id'])+';;'+str(penetration)+';;'+d['name']) #debug: print to cvs
    return penetration


import anki.sched
anki.sched.Scheduler._deckNewLimitSingle = wrap(
    anki.sched.Scheduler._deckNewLimitSingle,
    deckNewLimitSingle,
    'around'
)

if not ANKI20:
    import anki.schedv2
    anki.schedv2.Scheduler._deckNewLimitSingle = wrap(
        anki.schedv2.Scheduler._deckNewLimitSingle,
        deckNewLimitSingle,
        'around'
    )
