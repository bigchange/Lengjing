#!/usr/bin/python
#coding: utf-8
#
# multiple load data to redis
# $Id: Multiple_load_data.py  2015-11-30 Qiu $
#
# history:
# 2015-11-30 Qiu   created

# qiuqiu@kunyand-inc.com
# http://www.kunyandata.com
#
# --------------------------------------------------------------------
#
# Copyright (c)  by ShangHai KunYan Data Service Co. Ltd..  All rights reserved.
#
# By obtaining, using, and/or copying this software and/or its
# associated documentation, you agree that you have read, understood,
# and will comply with the following terms and conditions:
#
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted, provided that the above copyright notice appears in
# all copies, and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# ShangHai KunYan Data Service Co. Ltd. or the author
# not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# --------------------------------------------------------------------

"""
Multiple_load_data.py
"""

import threading
import time
from load_data import LoadData

class MultipleLoad(object):

    """Multiple load data

    Load  stock data  time to redis.

    Attributes:
        input_file: input data..
    """

    def __init__(self):

        """initiate class

        Load  stock data  time to redis.

        Attributes:
            input_file: input data..
        """

    def _counts(self, file):

        """initiate class

        Load  stock data  time to redis.

        Attributes:
            input_file: input data..
        """
        i = 0
        for line in file:
            i += 1
        file.seek(0)
        return i

    def _seg_file(self, path, k):

        """initiate class

        Load  stock data  time to redis.

        Attributes:
            input_file: input data..
        """
        file = open(path, 'r')
        row_nums = self._counts(file)
        K = []










