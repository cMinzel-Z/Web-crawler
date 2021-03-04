# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 21:10:49 2020

@author: Minzel
"""

import sys
import os

from scrapy.cmdline import execute


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "zhihu"])