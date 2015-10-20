#!/usr/bin/python
#coding: utf-8
#
# back_redis_modify
# $Id: initiate_unback_table.py  2015-10-20 Qiu $
#
# history:
# 2015-10-20 Qiu   created
#
# wangQiu@kunyandata.com
# http://www.kunyandata.com
#
# --------------------------------------------------------------------
# initiate_unback_table.py is
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
initiate_unback_table.py

initiate unback_redis_data table
"""

import MySQLdb
import paramiko
import os
import re

class InitTable(object):

    """initate table unbacked_redis_data in mysql.



    Attributes:
        no.
    """

    def __init__(self):

        """initate table unbacked_redis_data in mysql.



        Attributes:
            no.
        """

        remote_ip = '192.168.31.120'
        user = 'database'
        password = 'database'
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(remote_ip, 22, user, password)
        self.transport = paramiko.Transport((remote_ip, 22))
        self.transport.connect(username=user, password=password)
        self.remote_path = '/home/database/remote/'
        self.local_path = 'D:/home/'
        self.conn = MySQLdb.connect(host='192.168.31.189', user='root',
                                    passwd='root', db='db_machinekeyboard')
        self.curcor = self.conn.cursor()

    def get_files_list(self, remote_path):
        """get remote kunyan data file list.


        Attributes:
            remote_path:remote path.
        """
        stdin, stdout, stderr = self.ssh.exec_command("ls %s" % remote_path)
        if not stderr.readlines():
            remote_file = stdout.readlines()
        result = []
        for line in remote_file:
            result.append(line.encode().split()[0])
        return result

    def get_file_comment(self):

        """get redis data list in 'files'.



        Attributes:
            no.
        """

        remote_file_list = self.get_files_list(self.remote_path)
        if 'file' in remote_file_list:
            sftp = paramiko.SFTPClient.from_transport(self.transport)
            sftp.get(self.remote_path+'file', self.local_path+'file')
        isexists = os.path.exists(self.local_path+"files")
        if isexists:
            file_comment = open(self.local_path+"files")
            result = file_comment.readlines()
            results = []
            for line in result:
                results.append(line.split("\n")[0])
                return results
        else:
            print "Sorry, no file named 'files'."

    def create_table(self):

        """create table unbacked_redis_data.



        Attributes:
            no.
        """
        create_sql = "CREATE TABLE unbacked_redis_data " \
              "(unbacked_redis_stock VARCHAR(50))"
        try:
            self.curcor.execute(create_sql)
            self.conn.commit()
        except Exception, e:
            print e

    def get_unbacked_list(self):

        """get unbacked redis file list.



        Attributes:
            no.
        """
        try:
            self.curcor.execute("SELECT v_hour FROM visit_stock GROUP BY v_hour")
        except Exception, e:
            print e
        max_visit = self.curcor.fetchall()
        try:
            self.curcor.execute("SELECT v_hour FROM search_stock GROUP BY v_hour")
        except Exception, e:
            print e
        max_search = self.curcor.fetchall()
        max_time = max(max_visit[0], max_search[0])
        file_comment = self.get_file_comment()
        time = []
        if not file_comment:
            for line in file_comment:
                t = line[7:11]+ '-'+line[11:13]+ '-'\
                       +line[13:15]+line[15:17]
                if t > max_time:
                    time.append(line)
                    return time
        else:
            return None
            print "All files have been backed"


    def main(self):

        """main function.



        Attributes:
            no.
        """
        files = self.get_file_comment()
        unbacked_list = self.get_unbacked_list()
        try:
            self.curcor.execute("SHOW TABLES IN `stock`")
        except Exception, e:
            print e
        table = self.curcor.fetchall()
        tables = []
        for item in table:
            tables.append(item[0])
        if "unbacked_redis_data" not in tables:
            self.create_table()
        for line in unbacked_list:
            try:
                self.curcor.execute("INSERT INTO unbacked_redis_data SET "
                                    "unbacked_redis_file = '%s'" % line)
                self.conn.commit()
            except Exception, e:
                print e
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        for line in files:
            sftp.get(self.remote_path+line, self.local_path+line)

if __name__ == '__main__':
    inti_table= InitTable()
    inti_table.main()

