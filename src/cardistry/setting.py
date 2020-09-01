# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Cardistry
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from anki.hooks import addHook

from .const import ADDON_NAME
from .config import Config


class Settings:

    def __init__(self):
        self.conf = Config(ADDON_NAME)

        addHook(ADDON_NAME + '.configLoaded', self.onConfig)
        addHook(ADDON_NAME + '.configUpdated', self.onConfig)


    def onConfig(self):
        self.checkOptions()
        self._refresh()

    def checkOptions(self):
        opts = self.conf.get("scan_options", {})
        sd = opts.get("scan_days", 5)
        se = opts.get("scan_ease", 4000)
        ivl = opts.get("matured_ivl", 21)

        opts["scan_days"] = max(1, sd)
        opts["scan_ease"] = max(1300, se)
        opts["matured_ivl"] = max(1, ivl)
        self.conf.set("scan_options", opts)


    def _refresh(self):
        "Reset review count after addon config is loaded"
        mw.reset(True)


settings = Settings()
