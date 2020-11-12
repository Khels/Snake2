from cx_Freeze import setup, Executable

executables = [Executable('Snake.py',
               targetName='Snake.exe',
               base='Win32GUI',
               icon='icon.ico')]

includes = ['pygame', 'random', 'sys', 'os']

include_files = ['font', 'img', 'snds', 'LICENSE']

options = {
    'build_exe': {
        'include_msvcr': True,
        'includes': includes,
        'build_exe': 'build_windows',
        'include_files': include_files,
    }
}

setup(name='Snake',
      version='4.0',
      description='My masterpiece.',
      executables=executables,
      options=options)
