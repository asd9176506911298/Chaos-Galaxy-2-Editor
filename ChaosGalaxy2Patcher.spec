# -*- mode: python ; coding: utf-8 -*-
import os
import UnityPy

# 動態獲取 UnityPy 的安裝路徑，把它的資源資料夾包進去
unitypy_path = os.path.dirname(UnityPy.__file__)
unitypy_datas = [
    (os.path.join(unitypy_path, 'resources'), 'UnityPy/resources'),
]

# Win7 相容轉接 DLL
win7_dlls = [
    ('api-ms-win-core-path-l1-1-0.dll', '.'),
]

a = Analysis(
    ['ChaosGalaxy2Patcher.py'],
    pathex=[],
    binaries=win7_dlls,  # <-- 這裡把轉接 DLL 打包進 EXE 根目錄
    datas=unitypy_datas,
    hiddenimports=[
        'UnityPy.resources',
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
