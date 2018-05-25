# -*- mode: python -*-

block_cipher = None


a = Analysis(['asana-automate.py'],
             pathex=['C:\\Users\\Warehouse170919A\\Desktop\\human-i-t-hard-drive-destruction-automation-21f76eeb54e0\\human-i-t-hard-drive-destruction-automation-21f76eeb54e0'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='asana-automate',
          debug=True,
          strip=False,
          upx=False,
          runtime_tmpdir=None,
          console=True )
