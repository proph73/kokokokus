from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from constants import DEBUG

class _QLabel_proportionnel_au_premier_parent_d_affichage(QLabel):
    '''QLabel dont la taille varie avec la taille du parent
    Un parent doit être pourvu d'une unite_taille_affichage qui varie dans le paintEvent. '''
    def __init__(self, string_a_ecrire, police, coefficient_taille_police, *args, **kwargs):
        # args[0] : police
        # args[1] : coefficient_taille_police
        # args[2:] : police_args ; args à partir de l'indice 2 inclus https://www.w3schools.com/python/python_tuples_access.asp
        super().__init__(string_a_ecrire)
        # on stocke police et le coefficient_taille_police dont on va avoir besoin pour régénérer le qfont à chaque changement de taille
        self.police = police
        self.coefficient_taille_police = coefficient_taille_police
        # on stocke les args et kwargs qui ne varient pas mais dont on a besoin à chaque instanciation de qfont
        self.police_args = args[0:]  # cf police_args c'est args à partir de l'indice 2 inclus https://www.w3schools.com/python/python_tuples_access.asp
        self.police_kwargs = kwargs
        # gestion de la typo du Qlabel
        font = self.fontMaker()
        self.setFont(font)
        # SizePolicy
        # self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # Pour visualiser l'ensemble du widget
        if DEBUG == True:
            self.setAutoFillBackground(True)

    def fontMaker(self):
        '''génère un font, nécessaire à chaque fois que la typo doit changer '''
        # alpha est une constante, donc c'est la même pour tous les _QLabel_proportionnel_au_premier_parent_d_affichage et ne varie jamais.
        # Sa valeur arbitraire est fixé par moi pour adapter au jugé en dev ; plus pratique de manipuler alpha et coefficient_taille_police, que alpha*coefficient_taille_police même si cette autre solution aurait été possible
        alpha = 0.5
        # coefficient_taille_police est une constante, un coefficient propre à un qlabel donné selon la taille relative de sa police vis à vis de de celles d'autre QLabel
        if self.parent() == None :
            taille_en_points = int(alpha*self.coefficient_taille_police*10)
        else:
            parent = self.parent() 
            while not hasattr(parent, "unite_taille_affichage"):
                parent = parent.parent()
            taille_en_points = int(alpha*self.coefficient_taille_police*parent.unite_taille_affichage)
        font = QFont(self.police, taille_en_points, *(self.police_args), **(self.police_kwargs))
        return font

    def paintEvent(self, e):
        # ?? lors de l'appel par PySide6.QtWidgets.QWidget.resizeEvent(event)
        # adapte la taille d'écriture, pour cela génère un nouveau QFont
        font = self.fontMaker()
        self.setFont(font)
        # quelle taille de fenêtre ?
        # setfont pour changer la taille
        super().paintEvent(e)
    
    # def resizeEvent(self, event):
    #     font = self.fontMaker()
    #     self.setFont(font)
    #     # Call the base class implementation
    #     super().resizeEvent(event)

class resizingLabel(QLabel):
    # ça m'a lair de marcher ce truc
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixmap = None
        self.setMinimumSize(1, 1)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        # # Connect resize event
        # self.resizeEvent = self.on_resize

    def resizeEvent(self, event):
        # Call the base class implementation
        super().resizeEvent(event)
        if self.pixmap is not None:
            # Get the new size of the widget
            new_size = event.size()

            # Calculate the scaled size of the pixmap based on the new size of the widget
            scaled_pixmap = self.pixmap.scaled(new_size, Qt.KeepAspectRatio)

            # Update the pixmap of the label
            self.setPixmapFromResize(scaled_pixmap)

    def setPixmapFromResize(self, pixMap):
        if self.pixmap is None:
            self.pixmap = pixMap
        #     size = 3*self.size()
        # else :
        #     size = self.size()
        size = self.size()
        scaled_pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio)
        self.setPixmap(scaled_pixmap)

