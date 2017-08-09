#!/usr/bin/env python
# -*- coding:utf-8 -*-

#./autoUpToPGYBuild.py -p youproject.xcodeproj
#./autoUpToPGYBuild.py -w AutoPageDemo.xcworkspace

import argparse
import subprocess
import requests
import os
import datetime

#configuration for iOS build setting
CONFIGURATION = "Release"
#CONFIGURATION = "Debug"
EXPORT_OPTIONS_PLIST = "exportOptions.plist"

#要打包的TARGET名字
TARGET = 'AutoPageDemo'

#Info.plist路径
PLIST_PATH = "./AutoPageDemo/Info.plist"

#发布版本号
VERSION = '2.0.0'
BUILD = '200'

#VERSION = os.system('/usr/libexec/PlistBuddy -c "Print:CFBundleShortVersionString" %s' % (PLIST_PATH))
#BUILD   = os.system('/usr/libexec/PlistBuddy -c "Print:CFBundleVersion" %s' % (PLIST_PATH))



#存放路径以时间命令
DATE = datetime.datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

#会在桌面创建输出ipa文件的目录
EXPORT_MAIN_DIRECTORY = "~/Desktop/" + TARGET + DATE

#xcarchive文件路径（含有dsym），后续查找BUG用途
ARCHIVEPATH = EXPORT_MAIN_DIRECTORY + "/%s%s.xcarchive" %(TARGET,VERSION)

#ipa路径
IPAPATH = EXPORT_MAIN_DIRECTORY + "/%s.ipa" %(TARGET)


# configuration for pgyer
PGYER_UPLOAD_URL = "http://www.pgyer.com/apiv1/app/upload"
DOWNLOAD_BASE_URL = "http://www.pgyer.com"
USER_KEY = "c6eaef131044e51e779288cec9d17570"
API_KEY = "ddb74e126bebd1a10a91183a6e63f2bd"
#设置从蒲公英下载应用时的密码
PYGER_PASSWORD = ""

#clean
def cleanArchiveFile():
	cleanCmd = "rm -r %s" %(ARCHIVEPATH)
	process = subprocess.Popen(cleanCmd, shell = True)
	process.wait()
	print "cleaned archiveFile: %s" %(ARCHIVEPATH)


#解析上传到蒲公英的返回数据
def parserUploadResult(jsonResult):
	resultCode = jsonResult['code']
	if resultCode == 0:
		downUrl = DOWNLOAD_BASE_URL +"/"+jsonResult['data']['appShortcutUrl']
		print "Upload Success"
		print "DownUrl is:" + downUrl
	else:
		print "Upload Fail!"
		print "Reason:"+jsonResult['message']

#上传到蒲公英
def uploadIpaToPgyer(ipaPath):
	print "ipaPath:"+ipaPath
	ipaPath = os.path.expanduser(ipaPath)
	ipaPath = unicode(ipaPath, "utf-8")
	files = {'file': open(ipaPath, 'rb')}
	headers = {'enctype':'multipart/form-data'}
	payload = {'uKey':USER_KEY,'_api_key':API_KEY,'publishRange':'2','isPublishToPublic':'2', 'password':PYGER_PASSWORD}
	print "uploading...."
	r = requests.post(PGYER_UPLOAD_URL, data = payload ,files=files,headers=headers)
	if r.status_code == requests.codes.ok:
		result = r.json()
		parserUploadResult(result)
	else:
		print 'HTTPError,Code:'+r.status_code

#导出包
def exportArchive():
	exportCmd = "xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s" %(ARCHIVEPATH, EXPORT_MAIN_DIRECTORY, EXPORT_OPTIONS_PLIST)
	process = subprocess.Popen(exportCmd, shell=True)
	(stdoutdata, stderrdata) = process.communicate()

	signReturnCode = process.returncode
	if signReturnCode != 0:
		print "export %s failed" %(TARGET)
		return ""
	else:
		return EXPORT_MAIN_DIRECTORY
#编译project
def buildProject(project):
    archiveCmd = 'xcodebuild -project %s -scheme %s -configuration %s archive -archivePath %s -destination generic/platform=iOS' %(project, TARGET, CONFIGURATION, ARCHIVEPATH)
    process = subprocess.Popen(archiveCmd, shell=True)
    process.wait()

    archiveReturnCode = process.returncode
    if archiveReturnCode != 0:
        print "archive project %s failed" %(project)
        cleanArchiveFile()

#编译workSpace
def buildWorkspace(workspace):
	archiveCmd = 'xcodebuild -workspace %s -scheme %s -configuration %s archive -archivePath %s -destination generic/platform=iOS' %(workspace, TARGET, CONFIGURATION, ARCHIVEPATH)
	process = subprocess.Popen(archiveCmd, shell=True)
	process.wait()

	archiveReturnCode = process.returncode
	if archiveReturnCode != 0:
		print "archive workspace %s failed" %(workspace)
		cleanArchiveFile()

#编译
def xcbuild(options):
	project = options.project
	workspace = options.workspace

	if project is None and workspace is None:
		pass
	elif project is not None:
		buildProject(project)
	elif workspace is not None:
		buildWorkspace(workspace)

	#导出ipa文件
	exportarchive = exportArchive()
	print "~~~~~~~~~~~~~~~~正在上传到蒲公英~~~~~~~~~~~~~~~~"
	if exportarchive != "":
		uploadIpaToPgyer(IPAPATH)


#主入口
def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("-w", "--workspace", help="Build the workspace name.xcworkspace.", metavar="name.xcworkspace")
	parser.add_argument("-p", "--project", help="Build the project name.xcodeproj.", metavar="name.xcodeproj")

	options = parser.parse_args()

	print "options: %s，VERSION:%s；BUILD:%s" % (options,VERSION,BUILD)

#	os.system('/usr/libexec/PlistBuddy -c "Set:CFBundleShortVersionString %s" %s' % (VERSION,PLIST_PATH))
#	os.system('/usr/libexec/PlistBuddy -c "Set:CFBundleVersion %s" %s' % (BUILD, PLIST_PATH))

#开始编译
	xcbuild(options)

if __name__ == '__main__':
	main()
