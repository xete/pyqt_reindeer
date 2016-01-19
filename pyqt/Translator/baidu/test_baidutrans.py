#!/usr/bin/python
# -*- coding: utf-8 -*-

import baidutrans
import sys
from time import sleep

TEST_LIST = {"zh", "en", "yue", "wyw", "jp", "kor", "fra", "spa", "th", "ara", "ru", "pt", "de", "it", "el", "nl", "pl", "bul", "est", "dan", "fin", "cs", "rom", "slo", "swe", "hu", "cht", "nonsense"}

t = baidutrans.baiduTranslator()
print '>> some tests...'
for lan in TEST_LIST: 
	print lan, ":", t.translate('umbrella', 'en', lan)
print '\n>> preparing for more tests...'
sleep(3)
for lan in TEST_LIST: 
	print lan, ":", t.translate('interpreter', 'en', lan)
sys.exit()

