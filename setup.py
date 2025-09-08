from setuptools import setup

APP = ['Pic2WebPic.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['PIL', 'tkinter'],
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'Pic2WebPic',
        'CFBundleDisplayName': 'Pic2WebPic',
        'CFBundleGetInfoString': "Converting images to WebP format",
        'CFBundleIdentifier': "com.pic2webpic",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': u"Copyright © 2025, RicoSuaveDev, All Rights Reserved"
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
