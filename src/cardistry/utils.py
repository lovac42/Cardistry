# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Cardistry
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from .setting import settings


def getYoungCardCnt(did, incFilter):
    "count lrn or burried only, no suspended"

    opts = settings.conf.get("scan_options", {})
    sd = opts.get("scan_days", 5)
    scan_days = mw.col.sched.today + sd
    scan_ease = opts.get("scan_ease", 4000)
    matured_ivl = opts.get("matured_ivl", 21)

    sql_odid='or odid = %d'%did if incFilter else ''

    cnt=mw.col.db.first("""
Select count() from cards where
type in (1,2,3) and queue in (1,2,3,4,-2,-3)
and ivl < ? and due <= ? and factor <= ?
and (did = ? %s)"""%sql_odid,
matured_ivl, scan_days, scan_ease, did)[0]

    return cnt or 0
