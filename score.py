from constants import DEBUG
from qlabels_persos import _QLabel_proportionnel_au_premier_parent_d_affichage
from PySide6.QtWidgets import QWidget, QSizePolicy, QHBoxLayout
from PySide6.QtGui import QColor, QPainter, QBrush, QFont
from PySide6.QtCore import Qt, QPoint
from math import cos, sin, pi

class _Score(QWidget):
    '''Affichage du Score
    self.lateralite = 1 si gauche, droite -1 ; comme pour _Fautes
    police : type fonts["mikodacs"]
    self.score
    modifié directement par l'extérieur
    paintEvent c'est le dessin
    '''
     
    def __init__(self, lateralite, police, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )
        if lateralite == "gauche":
            self.lateralite = 1
        else:
            self.lateralite = -1
        coefficient_taille_police = 7
        self.couleur_ellipse = QColor('yellow')
        self.label = _QLabel_proportionnel_au_premier_parent_d_affichage('0', police, coefficient_taille_police)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)  # Alignement centré
        layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Pour visualiser l'ensemble du widget
        if DEBUG == True:
            self.setAutoFillBackground(True)
        
    # def _trigger_refresh(self):
    #     self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        
        # Dimensions du widget
        largeur = painter.device().width()
        hauteur = painter.device().height()

        # Fond
        brush = QBrush()
        # brush.setColor(QColor('white'))
        brush.setStyle(Qt.SolidPattern)
        # rect = QRect(0, 0, painter.device().width(), hauteur)
        # painter.fillRect(rect, brush)
        
        # dessin d'une ellipse
        # Couleur de l'ellipse
        pen = painter.pen()
        pen.setColor(self.couleur_ellipse)
        painter.setPen(pen)
        brush.setColor(self.couleur_ellipse)
        painter.setBrush(brush)

        # Calcul des inputs pour une ellipse définie par son centre et ses deux radii :
        # x_centre_rot, y_centre_rot, rx_trans, ry_trans
        # x_centre_base(latéralité)
        
        if self.lateralite == 1:  # gauche
            x_centre_base = int(125*largeur/200)
        elif self.lateralite == -1:  # droite
            x_centre_base = int(75*largeur/200)

        # translation verticale (pour que l'ellipse soit un peu en dessous du score lui-même)
        facteur_trans = 7  # translation définie proportionnellement au juger
        y_centre_trans = int(hauteur/2+facteur_trans*hauteur/100)
        ry_trans = int(8*hauteur/20 -facteur_trans*hauteur/100)
        rx_trans = int(8*largeur/20 -facteur_trans*largeur/100)

        #rotation
        angle_deg = self.lateralite*10 # clockwise
        angle = -angle_deg * pi/180  # anti clockwise
        painter.rotate(angle_deg)
        x_centre_rot = x_centre_base * cos(angle) - y_centre_trans * sin(angle)
        y_centre_rot = x_centre_base * sin(angle) + y_centre_trans * cos(angle)
        painter.drawEllipse(QPoint(x_centre_rot, y_centre_rot), rx_trans, ry_trans)
                        # # dérotation
                        # painter.rotate(-angle_deg)
        
                        # # écriture du score
                        # pen.setColor(QColor('black'))
                        # painter.setPen(pen)
                        # # Font
                        # # print("Available font families:", font_family)  # Print the available font families
                        # font_size = int(3*hauteur/4)
                        # font = QFont(self.police, font_size)
                        # painter.setFont(font)

                        # y_coin_haut_rectangle = 0
                        # if self.lateralite == 1:  # gauche
                        #     x_coin_haut_rectangle = x_centre_rot
                        #     painter.drawText(x_coin_haut_rectangle, y_coin_haut_rectangle, rx_trans, hauteur, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, str(self.score))
                        # elif self.lateralite == -1:  # droite
                        #     x_coin_haut_rectangle = x_centre_rot-rx_trans+int(largeur/20)  #largeur/20 ajouté arbitrairement ; x_centre_rot n'est sûrement pas le même selon la latéralité
                        #     painter.drawText(x_coin_haut_rectangle, y_coin_haut_rectangle, rx_trans, hauteur, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, str(self.score))
                        # painter.end()

                        # # Get current state.
                        # # dial = self.parent()._dial
                        # # vmin, vmax = dial.minimum(), dial.maximum()
# value = dial.value()
      
