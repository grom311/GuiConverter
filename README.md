# Convert to one exe
pyinstaller --onefile -w start.py --name=SFConverter --icon=Icons/rose1.png  

pyinstaller --onefile -w start.py --name=SFConverter   --icon=Icons\\rose1.ico

# UI convert
pyuic5 main.ui -o main.py
