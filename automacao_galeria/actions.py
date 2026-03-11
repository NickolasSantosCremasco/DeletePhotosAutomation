import os

adb = r"C:\Users\Nickolas Cremasco\Dropbox\scrcpy-win64-v3.3.4\scrcpy-win64-v3.3.4\adb.exe"

def tap(x, y):
    os.system(f'"{adb}" shell input tap {x} {y}')