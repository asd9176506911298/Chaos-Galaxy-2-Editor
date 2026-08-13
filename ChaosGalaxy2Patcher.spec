# -*- mode: python ; coding: utf-8 -*-
import os
import UnityPy

# 動態獲取 UnityPy 的安裝路徑，把它的資源資料夾包進去
unitypy_path = os.path.dirname(UnityPy.__file__)
unitypy_datas = [
    (os.path.join(unitypy_path, 'resources'), 'UnityPy/resources'),
]

a = Analysis(
    ['ChaosGalaxy2Patcher.py'],
    pathex=[],
    binaries=[],
    datas=unitypy_datas,  # <-- 1. 這裡加入了 UnityPy 的資源資料夾
    hiddenimports=[
        'UnityPy.resources',  # <-- 2. 這裡強迫引入找不到的子模組
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ChaosGalaxy2Patcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)