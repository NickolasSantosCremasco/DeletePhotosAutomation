import os

adb = r"C:\Users\Nickolas Cremasco\Dropbox\scrcpy-win64-v3.3.4\scrcpy-win64-v3.3.4\adb.exe"

def tap(x, y):
    os.system(f'"{adb}" shell input tap {x} {y}')

def dump_ui():
    os.system(f'"{adb}" shell uiautomator dump')
    os.system(f'"{adb}" pull /sdcard/window_dump.xml')

def swipe(x1, y1, x2, y2, tempo=300):
    os.system(f'"{adb}" shell input swipe {x1} {y1} {x2} {y2} {tempo}')