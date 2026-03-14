[app]
android.accept_sdk_license = True
# (str) Title of your application
title = Jarvis AI

# (str) Package name
package.name = jarvisai

# (str) Package domain (needed for android packaging)
package.domain = org.shouryacr7

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Yahan sirf basic libraries rakhi hain taaki build fail na ho
requirements = python3,kivy==2.3.0,hostpython3,requests,certifi,urllib3

# (str) Icon of the application
icon.filename = icon.png

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup
android.allow_backup = True

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = no, 1 = yes)
warn_on_root = 1
