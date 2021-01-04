# -*- mode: python -*-

block_cipher = None


a = Analysis(['F:\\A+Music\\src\\main\\python\\main.py'],
             pathex=['F:\\A+Music\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['f:\\a+music\\venv\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['F:\\A+Music\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='A+Music',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='F:\\A+Music\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='A+Music')
