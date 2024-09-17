import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    '--windowed',
    '--distpath', 'C:/Users/Daniel/Desktop/Calculadora',  # Diretório de saída
    'calculadora_tkinter.py'  # Nome correto do arquivo da calculadora
])
