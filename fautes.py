from constants import DEBUG
from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QColor, QPainter, QBrush, QFont
from PySide6.QtCore import QPoint
from PySide6.QtCore import Qt

class _Fautes(QWidget):
    '''Affichage des fautes
    self.lateralite = 1 si gauche, droite -1 ; comme pour _Score
    self.nombre_de_clics_fautes est la valuer stockée centrale au niveau de l'objet, tout en découle
    modifié par la MÉTHODE ajouter_un_clic_faute et retirer_un_clic_faute
    la FONCTION convertir_clics_en_fautes calcule nombre_de_fautes_total qui varie de 0 à plus de 3 évidemment
    la MÉTHODE fautes_affichees traduit en nombre de fautes de 0 à 3 ! -> 3 !comme ça on voit bien les toris fautes avant passage à 0
    paintEvent c'est le dessin
    '''
    def __init__(self, lateralite, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )
        if lateralite == "gauche":
            self.lateralite = 1
        else:
            self.lateralite = -1
        # On tient le compte du nombre de clics sur le bouton 'fautes'
        # pour pouvoir afficher 0, 1, 2 ou 3 fautes -> %4
        self.nombre_de_clics_fautes = 0

        if DEBUG:
            # Pour visualiser l'ensemble du widget
            self.setAutoFillBackground(True)
            self.a = False

    def convertir_clics_en_fautes(nombre_de_clics_fautes):
        nombre_de_fautes_total = (nombre_de_clics_fautes//4)*3 + nombre_de_clics_fautes%4
        return nombre_de_fautes_total
    
    def fautes_affichees(self):
        fautes_affichees = self.nombre_de_clics_fautes%4
        return fautes_affichees
    
    def ajouter_un_clic_faute(self):
        self.nombre_de_clics_fautes = self.nombre_de_clics_fautes+1
        if DEBUG:
            self.a = True
        self.update()

    def retirer_un_clic_faute(self):
        n = self.nombre_de_clics_fautes
        if n > 0:
            self.nombre_de_clics_fautes = n-1
            if DEBUG:
                self.a = True
            self.update()
        
    # def _trigger_refresh(self):
    #     self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        # Fond
        brush = QBrush()
        # brush.setColor(QColor('white'))
        brush.setStyle(Qt.SolidPattern)
        # rect = QRect(0, 0, painter.device().width(), hauteur)
        # painter.fillRect(rect, brush)
        
        pen = painter.pen()
        pen.setColor(QColor('red'))
        painter.setPen(pen)
        brush.setColor(QColor('red'))
        painter.setBrush(brush)

        # Dimensions du widget
        largeur = self.width()
        hauteur = self.height()

        # Tracé
        hauteur_carton_faute = int(hauteur/2)
        largeur_carton_faute = int(largeur/8)
        y_coin_haut_gauche_rectangle = int(hauteur/4)

        fautes_affichees = self.fautes_affichees()
        if fautes_affichees > 0:
            if DEBUG and self.a :
                print("clic")
                print("nombre_de_clics_fautes : "+ str(self.nombre_de_clics_fautes))
                print("nombre_de_fautes_total : "+ str(_Fautes.convertir_clics_en_fautes(self.nombre_de_clics_fautes)))
                print("fautes_affichees : "+ str(self.fautes_affichees()))
            for numero_fautes in range(fautes_affichees):
                if self.lateralite == 1:  # gauche
                    x_coin_haut_gauche_rectangle = int(largeur-2*numero_fautes*largeur_carton_faute-2*largeur_carton_faute)
                    painter.drawRect(x_coin_haut_gauche_rectangle, y_coin_haut_gauche_rectangle, largeur_carton_faute, hauteur_carton_faute)
                else:
                    x_coin_haut_gauche_rectangle = int(2*numero_fautes*largeur_carton_faute+2*largeur_carton_faute)
                    painter.drawRect(x_coin_haut_gauche_rectangle-largeur_carton_faute, y_coin_haut_gauche_rectangle, largeur_carton_faute, hauteur_carton_faute)
        else:
            if DEBUG and self.a :
                print("clic")
                print("nombre_de_clics_fautes : "+ str(self.nombre_de_clics_fautes))
                print("fautes_affichees : "+ str(self.fautes_affichees()))
                print("range : NON" )
        if DEBUG and self.a :
                self.a = False
        painter.end()

