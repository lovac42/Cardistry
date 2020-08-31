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

        addHook(ADDON_NAME + '.configLoaded', self._refresh)
        addHook(ADDON_NAME + '.configUpdated', self._refresh)


    def _refresh(conf):
        "Reset review count after addon config is loaded"
        mw.reset(True)


settings = Settings()
