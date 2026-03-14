[app]
title = JARVIS MARK AI
package.name = jarvis_ai
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy==2.3.0,edge-tts,pygame,speechrecognition,pyjnius,certifi

# Logo aur Splash Screen (Humne yahan add kar diya hai)
icon.filename = icon.png
presplash.filename = icon.png

# Permissions
android.permissions = INTERNET, RECORD_AUDIO, CALL_PHONE, SEND_SMS, SYSTEM_ALERT_WINDOW

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1