# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Cardistry
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw


def getYoungCardCnt(did, mIvl, incFilter):
    "count lrn or burried only, no suspended"

    sql_odid='or odid = %d'%did if incFilter else ''

    cnt=mw.col.db.first("""
Select count() from cards where
type in (1,2,3) and queue in (1,2,3,4,-2,-3)
and ivl < ? and (did = ? %s)
"""%sql_odid,mIvl,did)[0]
    return cnt or 0


