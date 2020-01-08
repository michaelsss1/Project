import win32com.client
import win32api 
import win32con
import os
import sys
import socket

def findAllExcel(topDir):
    FileExtList = ['xls', 'xlsm']
    suspiciousXlsFilePathList = []
    for root, dirs, files in os.walk(topDir, topdown = False):
        for fileName in files:
            if fileName.split(".")[-1] in FileExtList:
                suspiciousXlsFilePath = os.path.join(root, fileName)
                print(suspiciousXlsFilePath)
                suspiciousXlsFilePathList.append(suspiciousXlsFilePath)
            else:
                pass
    return suspiciousXlsFilePathList


def setREG():
# RegOpenKeyEx(key, subKey , reserved , sam )
# http://docs.activestate.com/activepython/2.4/pywin32/win32api__RegOpenKeyEx_meth.html
# RegSetValueEx(key, valueName, reserved, type, value)
# http://docs.activestate.com/activepython/2.4/pywin32/win32api__RegSetValueEx_meth.html

#key1: enable access to visual basic project trusted
#key2: enable trust acce
    key1 = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Software\\Microsoft\\Office\\14.0\\Excel" + "\\Security", 0, win32con.KEY_ALL_ACCESS)
    win32api.RegSetValueEx(key1, "AccessVBOM", 0, win32con.REG_DWORD, 1)

    key2 = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Software\\Microsoft\\Office\\14.0\\Excel" + "\\Security", 0, win32con.KEY_ALL_ACCESS)
    win32api.RegSetValueEx(key2, "VBAWarnings", 0, win32con.REG_DWORD, 1)
    
def delMeralcoFileOrDir(topDir):
    
    for root, dirs, files in os.walk(topDir, topdown = False):
        #remove meralco file
        for fileName in files:
            if "meralco" in fileName:
                meralcoFilePath = os.path.join(root, fileName)
                os.remove(meralcoFilePath)
                print(f'{meralcoFilePath} was removed')
        #remove meralco dir
        for dir in dirs:
            if "meralco" in dir:
                meralcoDirPath = os.path.join(root, dir)
                os.rmdir(meralcoDirPath)
                print(f'{meralcoDirPath} was removed')    


#For test
topDir = r'c:\Users'
findAllExcel(topDir)

maliciouXlsFilePath = input("maliciouXlsFilePath: ")
    # OPEN EXCEL APP AND WORKBOOK
xlApp = win32com.client.Dispatch("Excel.Application")

xlwb = xlApp.Workbooks.Open(maliciouXlsFilePath)
 

try:    
    for i in xlwb.VBProject.VBComponents:
        if i.Name == "pldt":
            xlmodule = xlwb.VBProject.VBComponents(i.Name)
                    # remove pldt
            xlwb.VBProject.VBComponents.Remove(xlmodule)
            print(f'[+]{maliciouXlsFilePath}\'s pldt was removed')                    
        else:
            print(f'[-]{maliciouXlsFilePath} has no pldt')
            pass
except Exception as e:
    print(e)

finally:
# CLOSE AND SAVE
    xlwb.Close(True)
    xlApp.Quit
    xlApp = None

	
'''
#recursivily remove pldt from all file

def delPldt(suspiciousXlsFilePathList):
    # OPEN EXCEL APP AND WORKBOOK
    xlApp = win32com.client.Dispatch("Excel.Application")
    for maliciouXlsFilePath in suspiciousXlsFilePathList:
        xlwb = xlApp.Workbooks.Open(maliciouXlsFilePath)
        try:    
            for i in xlwb.VBProject.VBComponents:
                if i.Name == "pldt":
                    xlmodule = xlwb.VBProject.VBComponents(i.Name)
                    # remove pldt
                    xlwb.VBProject.VBComponents.Remove(xlmodule)
                    print(f'{maliciouXlsFilePath}\'s pldt was removed')                    
                else:
                    print(f'{maliciouXlsFilePath}\'s has no pldt')
                    pass
        except Exception as e:
            print(e)

        finally:    
            # CLOSE AND SAVE
            xlwb.Close(True)
            xlApp.Quit
            xlApp = None
'''