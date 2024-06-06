from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QLabel
from PySide6.QtGui import QColor, QFont, QPainter, QBrush, QPixmap
from PySide6.QtCore import Qt, QRect
from qlabels_persos import _QLabel_proportionnel_au_premier_parent_d_affichage
from constants import DEBUG

class EquipeAffichage(QWidget):
    def __init__(self, lateralite, police):
        super().__init__()
        coefficient_taille_police = 3
        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )
        self.couleurNom = QColor("black")
        
        if lateralite == "gauche":
            self.lateralite = lateralite
            self.nom = "Équipe à gauche"
            self.couleurMaillot = QColor('red')
            self.couleurCarton = QColor('magenta')
            self.label = _QLabel_proportionnel_au_premier_parent_d_affichage(self.nom, police, coefficient_taille_police)
            self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignRight)
        else:
            self.lateralite = lateralite
            self.nom = "Équipe à droite"
            self.couleurMaillot = QColor('blue')
            self.couleurCarton = QColor('cyan')
            self.label = _QLabel_proportionnel_au_premier_parent_d_affichage(self.nom, police, coefficient_taille_police)
            self.label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignLeft)

        self.nomAffiche = True
        self.maillotAffiche = True
        self.cartonAffiche = True
        self.pourcentage_carton_largeur = 10
        self.logo = QPixmap()
        self.logoAffiche = False

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
        brush = QBrush()
        pen = painter.pen()

        largeur = self.width()
        hauteur = self.height()

        #Maillot
        if self.maillotAffiche:
            # Choix des crayons
            brush.setStyle(Qt.SolidPattern)
            brush.setColor(self.couleurMaillot)
            painter.setBrush(brush)
            pen = painter.pen()
            pen.setColor(self.couleurMaillot)
            # Dessin
            # x, y coordinates and a width and height of the rectangle, xradius, yradius
            painter.drawRoundedRect(0, 0, largeur, hauteur, largeur/10, largeur/10)

        #Logo
        pourcentageLogoSiMaillot = 80
        if self.logoAffiche:
            if self.maillotAffiche:
                # largeur_logo_alechel = largeur*pourcentageLogoSiMaillot/100
                hauteur_logo_alechel = hauteur*pourcentageLogoSiMaillot/100
                # scaled_pixmap = self.logo.scaled(QSize(largeur_logo_alechel, hauteur_logo_alechel), Qt.KeepAspectRatio)
                scaled_pixmap = self.logo.scaledToHeight(hauteur_logo_alechel)
                x_debutDessin = (largeur-scaled_pixmap.width())/2
                # pourcentageLogoSiMaillot/100*largeur/2
                y_debutDessin = (hauteur-hauteur_logo_alechel)/2
                # pourcentageLogoSiMaillot/100*hauteur/2
                # rectangle = QRect(x_debutDessin, y_debutDessin, largeur_logo_alechel, hauteur_logo_alechel)
                painter.drawPixmap(x_debutDessin,y_debutDessin, scaled_pixmap)
                # painter.drawPixmap(rectangle, scaled_pixmap)
            else:
                # scaled_pixmap = self.logo.scaled(QSize(largeur, hauteur), Qt.KeepAspectRatio)
                scaled_pixmap = self.logo.scaledToHeight(hauteur)
                largeur_logo = scaled_pixmap.width()
                painter.drawPixmap((largeur-largeur_logo)/2,0, scaled_pixmap)
        
        #Nom Géré dans l'update
        if self.cartonAffiche:
            pourcentagesCarton = (40, self.pourcentage_carton_largeur)
        else : pourcentagesCarton = (0,0)

        # if self.nomAffiche:
        #     pass
            # print("pourcentagesCarton[1] : "+str(pourcentagesCarton[1]))
            # self.label_nom.setFixedWidth((100-pourcentagesCarton[1])*largeur)
            # self.label_nom.setText(self.nom)
        # else:
        #     self.label_nom.setText("")

            

                        # #Nom
                        # if self.nomAffiche:
                        #     pen.setColor(self.nomCouleur)
                        #     painter.setPen(pen)
                        #     brush.setStyle(Qt.NoBrush)
                        #     brush.setColor(self.couleurCarton)
                        #     painter.setBrush(brush)
                        #     # Font
                        #     font_size_base = int(hauteur/4)
                        #     font = QFont(self.police, font_size_base)
                        #     # font = QFont(self.police)
                        #     painter.setFont(font)
                        #     # Calcul
                        #     pourcentageNom = 80
                        #     if self.maillotAffiche:
                        #         proportion = pourcentageNom
                        #     else :
                        #         proportion = 100
                        #     largeur_rectangle = largeur*proportion/100 -largeur*pourcentageCarton/100
                        #     hauteur_rectangle = hauteur*proportion/100
                        #     if self.lateralite == "gauche":
                        #         x_coin_haut_rectangle = (100-proportion)*largeur/100  #+pourcentageCarton*largeur/100
                        #     elif self.lateralite== "droite":
                        #         x_coin_haut_rectangle = (100-proportion)*largeur/100-pourcentageCarton*largeur/100
                        #     y_coin_haut_rectangle = (100-proportion)*hauteur/100
                        #     # Écriture
                        #     if DEBUG : painter.drawRect(x_coin_haut_rectangle, y_coin_haut_rectangle, largeur_rectangle, hauteur_rectangle)
                        #     painter.drawText(x_coin_haut_rectangle, y_coin_haut_rectangle, largeur_rectangle, hauteur_rectangle, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, self.nom)
                        #     # if self.lateralite == "gauche":
                        #     #     alignment = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                        #     # elif self.lateralite== "droite":
                        #     #     alignment = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                        #     # painter.drawText(x_coin_haut_rectangle, y_coin_haut_rectangle, largeur_rectangle, hauteur_rectangle, alignment, self.nom)
                        #     # painter.drawText(x_coin_haut_rectangle, y_coin_haut_rectangle, largeur_rectangle, hauteur_rectangle, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, self.nom)

        #Carton
        # Dimensions du widget
        largeur = painter.device().width()
        hauteur = painter.device().height()
        if self.cartonAffiche:
            # Choix des crayons
            brush.setStyle(Qt.SolidPattern)
            brush.setColor(self.couleurCarton)
            painter.setBrush(brush)
            pen.setColor('black')
            # Calcul
            largeur_rectangle = largeur*pourcentagesCarton[1]/100
            hauteur_rectangle = hauteur*pourcentagesCarton[0]/100
            if self.lateralite == "gauche":
                x_coin_haut_rectangle = 0
            elif self.lateralite == 'droite':
                x_coin_haut_rectangle = largeur-pourcentagesCarton[1]*largeur/100
            y_coin_haut_rectangle = 0
            # Dessin
            # x, y coordinates and a width and height of the rectangle
            painter.drawRect(x_coin_haut_rectangle, y_coin_haut_rectangle, largeur_rectangle, hauteur_rectangle)

        if DEBUG:
            #Test de fin de widget à droite, pour être sûr qu'on le voit entièremenr
            brush.setStyle(Qt.SolidPattern)
            brush.setColor(QColor('yellow'))
            painter.setBrush(brush)
            largeur_rectangle = largeur/2
            if self.lateralite == "gauche":
                x_coin_haut_rectangle = largeur_rectangle
            elif self.lateralite == 'droite':
                x_coin_haut_rectangle = 0
            painter.drawRect(x_coin_haut_rectangle, 0, largeur_rectangle, hauteur)
            
        painter.end()
    
