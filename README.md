# Kokokokus
Logiciel d'affichage pour le spectacle du match d'improvisation théâtrale, porté notamment par un site bientôt en ligne. À votre disposition pour vos spectacles. Bisous.

### Features
+ Utilisation de deux écrans : fenêtre de contrôle distincte de la fenêtre d'affichage. Cela permet de contrôler en invisible l'affichage sur un vidéoprojecteur.
+ Affichage "Carton d'arbitre" avec seulement ce qui concerne l'impro en cours, ou affichage complet
+ Chronomètre affiché
+ Compteurs de score et de fautes
+ Logo des équipes ou noms
+ Arrière-plan et couleurs personnalisables
+ Résolution aisément modifiable

#### Features à venir
+ Sauvegarde des préférences d'une session à l'autre

## L'esprit
Pour nous l'improvisation est synonyme de vivre ensemble et de partage. Tant-pis pour les fragiles égoïstes. Il était donc logique d'adopter une licence GPL. Cela signifie que tous peuvent l'utiliser librement pour leurs spectacles.

## Pour contribuer
Tout le monde est bienvenu pour contribuer à l'amélioration de cet outil.
Cela inclue même aujourd'hui un travail de restructuration du code pour le rendre plus "github-compatible". Cette première version suit parfois des pratiques divergentes. Notamment dans l'usage du français et de l'anglais en même temps.
La version de python utilisée est la 3.10.12 et celle de pyside la 6.6.1

## Build Windows

### Bibliothèques python
```
altgraph==0.17.4
distlib==0.3.8
filelock==3.13.1
ordered-set==4.1.0
packaging==23.2
pefile==2023.2.7
platformdirs==4.1.0
pyinstaller==6.3.0
pyinstaller-hooks-contrib==2024.0
PySide6==6.6.1
PySide6-Addons==6.6.1
PySide6-Essentials==6.6.1
pywin32-ctypes==0.2.2
shiboken6==6.6.1
virtualenv==20.25.0
zstandard==0.22.0
```

### Le bat à exécuter
Modifier dans constants.py : DEBUG=FALSE. Pyinstaller 6.3.0.

```
SET programme=kokokokus
 
IF EXIST build RMDIR /S /Q build
IF EXIST dist RMDIR /S /Q dist
 
python -m  PyInstaller ^
--clean ^
--noconfirm ^
--onefile ^
--noupx ^
--noconsole ^
--icon ".\icon.ico" ^
--add-data=.\background_wallpaper.jpg:. ^
--add-data=.\fonts\*:.\fonts\ ^
--add-data=.\ColorPicker.py:. ^
--add-data=.\constants.py:. ^
--add-data=.\equipe.py:. ^
--add-data=.\fautes.py:. ^
--add-data=.\horloges.py:. ^
--add-data=.\qlabels_persos.py:. ^
--add-data=.\score.py:. ^
.\%programme%.py
PAUSE
.\dist\\%programme%.exe
```
