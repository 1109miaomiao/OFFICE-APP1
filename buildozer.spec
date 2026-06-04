[app]

# 你的 App 名称（用户会在手机桌面上看到）
title = 办公自动化工具箱

# 包名（唯一标识，用你的域名倒写）
package.name = officetools
package.domain = com.yourname

# 版本号
version.code = 1
version.string = 1.0.0

# 源代码文件
source.dir = .
source.include_exts = py,png,jpg,kv,ttf

# 构建要求
requirements = python3,kivy,kivymd,pandas,openpyxl,PyPDF2,Pillow,python-docx,plyer

# 权限（文件读写）
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# 图标（准备一个 icon.png 放在这里）
icon.filename = icon.png

# 启动画面
presplash.filename = splash.png

# Android API 级别
android.api = 34
android.minapi = 24
android.ndk = 27
android.sdk = 34

# 打包格式
android.archs = arm64-v8a
android.allow_deprecated = False

# 日志
android.logcat_filters = *:S python:V

[buildozer]
log_level = 2
warn_on_root = 1

# Windows 上使用 WSL Docker
# docker = True
