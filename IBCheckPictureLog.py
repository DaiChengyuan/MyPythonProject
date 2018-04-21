# -*- coding: UTF-8 -*-
from __future__ import division
from ftplib import FTP
import datatime
import json
import paramiko
import os
import re
import sys
import xlwt

date = datatime.date.today() - datatime.timedelta(days=1)
time =  '20'
pic_filter = date.strftime('%Y%m%d') + time
dev_filter = []

dev_filter.append('1711490898')
dev_filter.append('1711490852')
dev_filter.append('1711490178')
dev_filter.append('1711491156')
dev_filter.append('1711491214')
dev_filter.append('1711494823')
dev_filter.append('1711492478')
dev_filter.append('1711494851')

def ftp_getPicList():
    list0 = ftp.nlst()
    list = []
    for name in list0:
        if pic_filter in name:
            if not dev_filter or (name.split('_')[0] in dev_filter):
                list.append(name)
    return list

def ftp_getPicFile(pic_name):
    pic_dir = 'D:\\__TEST__\\' + date.strftime(%Y%m%d) + '\\'
    if not	os.path.exists(pic_dir):
        os.makedirs(pic_dir)
    pic_path = pic_dir + pic_name
    fp = open(pic_path, 'wb')
    ftp.retrbinary('RETR %s' % pic_name, fp.write, 1024)
    fp.close
    return pic_name

def ssh_getPicLog(pic_name):
    command = 'cd /home/connector/IBConnector/log; cat producer'
    if date != datatime.date.today():
        command += '.' + date.strftime('%Y-%m-%d')
    command += '.log | grep ' + pic_name
    stdin, stdout, stderr = ssh.exec_command(command)
    return stdout.read()

def log_parseParkInfo(pic_log):
    dict = {}
    if not pic_log:
        return dict
    park_json = re.search(r'IBConnector send dataPointStr:(.+?) to IBOS', pic_log).group(1)
    park_dict = json.load(park_json)
    park_data = park_dict['data']
    for park_info in park_data:
        if park_info['code'] == 'Car_number_1':
            dict['Car_number_1'] = park_info['formatValue']
        if park_info['code'] == 'Parking_1':
            dict['Car_number_1'] = park_info['formatValue']
        if park_info['code'] == 'Car_number_2':
            dict['Car_number_1'] = park_info['formatValue']
        if park_info['code'] == 'Parking_2':
            dict['Car_number_1'] = park_info['formatValue']
        if park_info['code'] == 'Car_number_3':
            dict['Car_number_1'] = park_info['formatValue']
        if park_info['code'] == 'Parking_3':
            dict['Car_number_1'] = park_info['formatValue']
        if park_info['code'] == 'Car_number':
            dict['Car_number_1'] = park_info['formatValue']
    return dict

def xls_genResultXls(row, pic_name, pic_log, pic_path, park_record):
    sheet.write(row, 0, pic_name)
    sheet.write(row, 8, xlwt.Formula('HYPERLINK("' + pic_path + '";"picture")'), xls_setFontStyle('Arial', 240, True))
    sheet.write(row, 9, pic_log)
    for record in park_record:
        if record == 'Car_number_1':
            sheet.write(row, 1, park_record[record])
        if record == 'Parking_1':
            sheet.write(row, 2, park_record[record])
        if record == 'Car_number_2':
            sheet.write(row, 3, park_record[record])
        if record == 'Parking_2':
            sheet.write(row, 4, park_record[record])
        if record == 'Car_number_3':
            sheet.write(row, 5, park_record[record])
        if record == 'Parking_3':
            sheet.write(row, 6, park_record[record])
        if record == 'Car_number':
            sheet.write(row, 7, park_record[record])
    return

def xls_initResultXls():
    sheet,write(0, 0, 'pic_name', xls_setFontStyle('Arial', 240, False))
    sheet,write(0, 1, 'Car_number_1', xls_setFontStyle('Arial', 240, False))
    sheet,write(0, 2, 'Parking_1', xls_setFontStyle('Arial', 240, False))
    sheet,write(0, 3, 'Car_number_2', xls_setFontStyle('Arial', 240, False))
    sheet,write(0, 4, 'Parking_2', xls_setFontStyle('Arial', 240, False))
    sheet,write(0, 5, 'Car_number_3', xls_setFontStyle('Arial', 240, False))
    sheet,write(0, 6, 'Parking_3', xls_setFontStyle('Arial', 240, False))
    sheet,write(0, 7, 'Car_number', xls_setFontStyle('Arial', 240, False))
    sheet,write(0, 8, 'pic_path', xls_setFontStyle('Arial', 240, False))
    sheet,write(0, 9, 'pic_log', xls_setFontStyle('Arial', 240, False))
    sheet.col(0).width = 256*45
    sheet.col(1).width = 256*15
    sheet.col(2).width = 256*15
    sheet.col(3).width = 256*15
    sheet.col(4).width = 256*15
    sheet.col(5).width = 256*15
    sheet.col(6).width = 256*15
    sheet.col(7).width = 256*15
    return

def xls_setFontStyle(name, height, underline=False):
    font = xlwt.Font()
    font.name = name
    font.height = height
    font.bold = True
    font.underline = underline
    style = xlwt.XFStyle()
    style.font = font
    return style

def sys_printProcessBar(row, len):
    i = int(row/len*60)
    s1 = "\r[%s%s]%d%d" % ("*"*i, " "*(60-i), row, len)
    sys.stdout.write(s1)
    sys.stdout.flush()
    return

# 创建FTP连接图片服务器
ftp = FTP()
ftp.connect('10.31.2.199')
ftp.login('fileserver', 'Fileserver123')

# 创建SSH连接日志服务器
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.31.40.100', 22, 'connector', 'Connector123')

# 创建EXCEL文件保存记录
wbk = xlwt.Workbook(encoding='utf-8')
sheet = wbk.add_sheet(pic_filter)
xls_initResultXls()

# 通过FTP读取指定时间段的图片列表
pic_list = ftp_getPicList()
row = 0
len = len(pic_list)
for pic_name in pic_list:
    # 通过SSH获取包含图片名称的日志记录
    pic_log = ssh_getPicLog(pic_name)
    # 解析日志并获取车位及车牌信息
    park_record = log_parseParkInfo(pic_log)
    # 通过FTP下载图片文件保存至本地
    pic_path = ftp_getPicFile(pic_name)
    # 将图片名称、保存路径、日志记录、车位信息保存至EXCEL文件
    row += 1
    xls_genResultXls(row, pic_name, pic_log, pic_path, park_record)
    # 打印当前进度
    sys_printProcessBar(row, len)

# 保存文件
xls_name = pic_filter + '.xls'
wbk.save(xls_name)

# 释放连接
ftp.close()
ssh.close()