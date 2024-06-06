from PySide6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QLabel, QColorDialog
from PySide6.QtGui import QPalette, QColor

class ColorPickerAvecAppliquer_group(QGroupBox):
    def __init__(self, nom_de_groupe_en_minuscule):
        super().__init__(nom_de_groupe_en_minuscule.capitalize())

        # self.setWindowTitle("Color Picker")
        # self.setGeometry(100, 100, 300, 200)
        self.chosen_color = None
        self.appliquer = QPushButton("Appliquer")
        self.color_button = QPushButton("Choisir une couleur")
        self.color_button.clicked.connect(self.choose_color)
        
        checkbox = QWidget()
        checkbox_layout = QHBoxLayout()
        checkbox_label = QLabel("Afficher la " + nom_de_groupe_en_minuscule)
        self.checkbox_checkbox = QCheckBox()
        checkbox_layout.addWidget(self.checkbox_checkbox, 0)
        checkbox_layout.addWidget(checkbox_label, 1)
        checkbox.setLayout(checkbox_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.color_button)
        layout.addWidget(checkbox)
        layout.addWidget(self.appliquer)

        self.setLayout(layout)

    def choose_color(self):
        color_dialog = QColorDialog(self)
        color = color_dialog.getColor()
        if color.isValid():
            self.chosen_color = color
            opposite_color = QColor(255-color.red(), 255-color.green(), 255-color.blue())
            button_palette = self.color_button.palette()
            button_palette.setColor(QPalette.Button, color)
            button_palette.setColor(QPalette.ButtonText, opposite_color)
            self.color_button.setPalette(button_palette)
            self.checkbox_checkbox.setChecked(True)

class ColorPicker_group(QGroupBox):
    def __init__(self, nom_de_groupe_en_minuscule):
        super().__init__(nom_de_groupe_en_minuscule.capitalize())

        # self.setWindowTitle("Color Picker")
        # self.setGeometry(100, 100, 300, 200)
        self.chosen_color = None
        self.color_button = QPushButton("Choisir une couleur")
        self.color_button.clicked.connect(self.choose_color)
        
        checkbox = QWidget()
        checkbox_layout = QHBoxLayout()
        checkbox_label = QLabel("Afficher la " + nom_de_groupe_en_minuscule)
        self.checkbox_checkbox = QCheckBox()
        checkbox_layout.addWidget(self.checkbox_checkbox, 0)
        checkbox_layout.addWidget(checkbox_label, 1)
        checkbox.setLayout(checkbox_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.color_button)
        layout.addWidget(checkbox)

        self.setLayout(layout)

    def choose_color(self):
        color_dialog = QColorDialog(self)
        color = color_dialog.getColor()
        if color.isValid():
            self.chosen_color = color
            opposite_color = QColor(255-color.red(), 255-color.green(), 255-color.blue())
            button_palette = self.color_button.palette()
            button_palette.setColor(QPalette.Button, color)
            button_palette.setColor(QPalette.ButtonText, opposite_color)
            self.color_button.setPalette(button_palette)
            self.checkbox_checkbox.setChecked(True)

class ColorPicker(QWidget):
    def __init__(self, intitule="", color=QColor("red")):
        super().__init__()
        self.chosen_color = color
        layout = QVBoxLayout()
        if intitule =="":
            self.color_button = QPushButton("Choisir la couleur")
        else:
            self.color_button = QPushButton("Choisir la "+intitule)
        self.color_button.clicked.connect(self.choose_color)
        layout.addWidget(self.color_button)
        self.setLayout(layout)

    def choose_color(self):
        color_dialog = QColorDialog(self)
        color = color_dialog.getColor()
        if color.isValid():
            self.chosen_color = color
            opposite_color = QColor(255-color.red(), 255-color.green(), 255-color.blue())
            button_palette = self.color_button.palette()
            button_palette.setColor(QPalette.Button, color)
            button_palette.setColor(QPalette.ButtonText, opposite_color)
            self.color_button.setPalette(button_palette)
