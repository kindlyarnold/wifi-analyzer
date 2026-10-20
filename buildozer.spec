[app]
title = Deriv Trader Demo First
package.name = derivtrader
package.domain = org.example
source.dir = .
source.include_exts = py
version = 1.0.0
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,idna,charset-normalizer,websockets
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WAKE_LOCK
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
