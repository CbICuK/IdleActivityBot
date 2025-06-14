# bot.spec
# Команда сборки: pyinstaller bot.spec

block_cipher = None

a = Analysis(
    ['IdleActivityBot.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['ctypes', 'pyautogui', 'psutil', 'threading', 'os', 'time', 'random', 'logging'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='work_time_bot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # без консоли
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='work_time_bot'
)
