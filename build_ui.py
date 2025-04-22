import PyInstaller.__main__

tkinter_app = "ui.py"
extra_import = "pyodbc"
icon_name = "csv.ico"

options = [
    '--onefile',
    '-w',
    '--name', 'UC Export',
    f'--icon={icon_name}',
    f'--hidden-import={extra_import}',
    '--add-data', '.env;.',
    '--add-data', f'{icon_name};.',
    f'{tkinter_app}'
]

PyInstaller.__main__.run(options)
