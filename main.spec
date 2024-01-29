# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_submodules
from kivy_deps import sdl2, glew

a = Analysis(
    ['main.py'],
    pathex=['D:\\mini project\\pythonProject1login - Copy'],  # Specify the path to your project
    binaries=[],
    datas=collect_data_files('kivy', include_py_files=True) + [
        ('D:\\mini project\\pythonProject1login - Copy\\images/*', 'images'),  # Include all files in the 'images' folder
        ('D:\\mini project\\pythonProject1login - Copy/*.py', '.'),  # Include all Python files in the root directory
        ('D:\\mini project\\pythonProject1login - Copy/*.kv', '.'),  # Include all Kivy language files in the root directory

        ('D:\mini project\pythonProject1login - Copy/*.db', '.'),  # Include SQLite database files
    ],
    hiddenimports=collect_submodules('plyer') + ['email_module', 'openai_module', 'apscheduler_module', 'smtplib','requests'],
    # Add the following line to include the sqlite3 module
    hiddenimports=['sqlite3'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DoDone',  # Change the name to 'DoDone'
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DoDone',  # Change the name to 'DoDone'
)
