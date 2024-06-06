from constants import DEBUG
from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTimeEdit
from PySide6.QtCore import QSize, QRectF, QTimer, QTime
from PySide6.QtGui import QPainter, QBrush, QColor
from qlabels_persos import _QLabel_proportionnel_au_premier_parent_d_affichage
from PySide6.QtCore import Qt

class Cadran_analogique(QWidget):
    '''Temps qui s écoule dessiné.
        Affiché ou non selon self.affiche
        update_angle permet de mettre à jour le dessin
        Affiché avec set_time de Horloge_affichage parent mais le reste par Horloge_controle
    '''

    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Minimum,
            QSizePolicy.Minimum
        )
        self.angle_qui_reste = None
        self.affiche = False
        self.couleur_temps_ecoule = QColor('red')
        self.couleur_temps_initial = QColor('yellow')
        
        # Pour visualiser l'ensemble du widget
        if DEBUG == True:
            self.setAutoFillBackground(True)

        

    # def sizeHint(self):
    #     return QSize(40,120)
    
    # def _trigger_refresh(self):
    #     self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        # Dimensions du widget
        largeur = painter.device().width()
        hauteur = painter.device().height()
        cote_carre = min(largeur, hauteur)
        
        if self.affiche:
            # pinceau
            pen = painter.pen()
            pen.setColor(self.couleur_temps_ecoule)
            painter.setPen(pen)
            brush = QBrush()
            brush.setStyle(Qt.SolidPattern)
            
            # ICI
            brush.setColor(self.couleur_temps_ecoule)
            painter.setBrush(brush)

            # rotation pour ne pas avoir un 0 à 15h
            painter.translate(largeur/2, hauteur/2)
            painter.rotate(-90)
            painter.translate(hauteur/2, -largeur/2)
            # On a ainsi un repère de centre le coin en haut à gauche avec pour la saisie d'abord : ordonnée vers le haut puis abscisse vers la droite (c'est tout comme)
            # cercle de fond
            rectangle = QRectF(-(hauteur/2-cote_carre/2), (largeur/2-cote_carre/2), -cote_carre, cote_carre)
            # painter.drawRect(rectangle)
            painter.drawPie(rectangle, 0, 360*16)
            # le temps s'écoule
            pen2 = painter.pen()
            # ICI
            pen2.setColor(self.couleur_temps_initial)
            brush.setColor(self.couleur_temps_initial)
            painter.setPen(pen2)
            painter.setBrush(brush)
            painter.drawPie(rectangle, 0, self.angle_qui_reste)
        # else:  # pour qu'autant d'espace soit pris lorsque le cadran n'est pas affiché
        #     # pinceau
        #     pen = painter.pen()
        #     pen.setColor(QColor('red'))
        #     painter.setPen(pen)
        #     brush = QBrush()
        #     brush.setStyle(Qt.SolidPattern)
        #     brush.setColor(QColor('red'))
        #     painter.setBrush(brush)

        #     # rotation pour ne pas avoir un 0 à 15h
        #     painter.translate(largeur/2, hauteur/2)
        #     painter.rotate(-90)
        #     painter.translate(hauteur/2, -largeur/2)
        #     # On a ainsi un repère de centre le coin en haut à gauche avec pour la saisie d'abord : ordonnée vers le haut puis abscisse vers la droite (c'est tout comme)
        #     # cercle de fond
        #     rectangle = QRectF(-(hauteur/2-cote_carre/2), (largeur/2-cote_carre/2), -cote_carre, cote_carre)
        #     # painter.drawRect(rectangle)
        #     painter.drawPie(rectangle, 0, 360*16)
        #     # le temps s'écoule
        #     pen2 = painter.pen()
        #     pen2.setColor(QColor('yellow'))
        #     brush.setColor(QColor('yellow'))
        #     painter.setPen(pen2)
        #     painter.setBrush(brush)
        #     painter.drawPie(rectangle, 0, self.angle_qui_reste)
        painter.end()

    def update_angle(self, temps_qui_reste):
        self.angle_qui_reste = temps_qui_reste*360*16/int(self.parent().temps_a_chronometrer_en_secondes)
        self.update()

class Horloge_affichage(QWidget):
    '''
    Horloge côté affichage contrôlé par une Horloge_controle, qui peut elle en contrôler plusieurs.
    = label + horloge analogique
    La MÉTHODE set_time initialise le label avec le temps_a_chronometrer_en_secondes transmis
    '''
    def __init__(self, fonts):
        super().__init__()
        font_one_line_standard_tup = (fonts["technasans"], 2,)
        self.temps_a_chronometrer_en_secondes = None
        # self.affiche = False
        self.temps_a_chronometrer_label = _QLabel_proportionnel_au_premier_parent_d_affichage("", *font_one_line_standard_tup)
        self.temps_a_chronometrer_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.cadran_analogique = Cadran_analogique()
        layout = QVBoxLayout()
        layout.addWidget(self.temps_a_chronometrer_label)
        layout.addWidget(self.cadran_analogique)
        self.setLayout(layout)
    
    def set_time(self, temps_a_chronometrer_t):
        '''Fonction pour initialiser le temps avant décompte : le cadran devient visible et le label rempli
        Attention le dessin de l'cadran_analogique est mis ensuite à jour directement par l Horloge_controle
        '''
        if DEBUG : print(temps_a_chronometrer_t)
        temps_a_chronometrer_en_secondes = QTime_perso.en_secondes(temps_a_chronometrer_t)
        if DEBUG : print(temps_a_chronometrer_en_secondes)
        self.temps_a_chronometrer_en_secondes = temps_a_chronometrer_en_secondes
        self.cadran_analogique.update_angle(int(self.temps_a_chronometrer_en_secondes))
        # self.affiche = True
        self.cadran_analogique.affiche = True
        self.temps_a_chronometrer_label.setText(QTime_perso.afficher(temps_a_chronometrer_t))
        # self._trigger_refresh()

    def clear(self):
        # self.affiche = False
        self.cadran_analogique.affiche = False
        self.temps_a_chronometrer_label.setText("")
        # self._trigger_refresh()

    # def _trigger_refresh(self):
    #     self.update()
    #     self.cadran_analogique._trigger_refresh()

class Horloge_controle(QWidget):
    '''
    Horloge côté contrôle contrôlant LES Horloge_affichage qui sont ses seuls arguments. En effet l'affichage Carton et Standard ne peuvent partager un même widget horloge.
    = label + QTimeEdit
    Timer de 1000ms qui se répète pour mettre à jour.
    self.temps_qui_reste_en_secondes
    self.display ne semble pas manipulé après sa création ?!
    '''
    def __init__(self, *horloges):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding
        )
        self.horloges_affichage = horloges
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.everySecond)
        self.temps_qui_reste_en_secondes = None
        
        self.label = QLabel("Temps : ")
        self.temps_a_chronometrer_input = QTimeEdit()
        self.temps_a_chronometrer_input.setDisplayFormat(("mm:ss"))
        
        self.start = QPushButton(text="Start")
        self.stop = QPushButton(text="Stop")
        self.start.setEnabled(False)
        self.stop.setEnabled(False)
        self.display = QLabel()

        self.start.clicked.connect(self.startTimer)
        self.stop.clicked.connect(self.endTimer)
        self.layout()

    def layout(self):
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.temps_a_chronometrer_input)
        layout.addWidget(self.start)
        layout.addWidget(self.display)
        layout.addWidget(self.stop)
        self.setLayout(layout)

    def startTimer(self):
        self.timer.start()
        self.start.setEnabled(False)
        self.stop.setEnabled(True)

    def endTimer(self):
        self.timer.stop()
        self.start.setEnabled(False)
        self.stop.setEnabled(False)

    def everySecond(self):
        if self.temps_qui_reste_en_secondes > 0:   
            self.temps_qui_reste_en_secondes = self.temps_qui_reste_en_secondes-1
            for horloge in self.horloges_affichage:
                horloge.cadran_analogique.update_angle(self.temps_qui_reste_en_secondes)
        else:   
            self.timer.stop()
        # self._trigger_refresh()


class QTime_perso(QTime):
    '''
    QTime enrichi d'une fonction pour affichage et d'une fonction pour avoir la quantité de seocndes.
    la FONCTION en_secondes renvoie la quantité de secondes
    la FONCTION afficher renvoie une string human readable pour être exploitée
    '''
    def en_secondes(t):
        secondes = t.hour()*3600+t.minute()*60+t.second()
        return secondes
    
    def afficher(t):
        string = ""
        heure = t.hour()
        minute = t.minute()
        seconde = t.second()
        if heure > 0:
            if heure > 1 :
                string+= str(heure) + " heures"
            else:
                string+= str(heure) + " heure"
            if minute + seconde >0 :
                string+= " et "
        if minute > 0:
            if minute > 1 :
                string+= str(minute) + " minutes"
            else:
                string+= str(minute) + " minute"
            if seconde >0 :
                string+= " et "
        if seconde > 0:
            if seconde > 1 :
                string+= str(seconde) + " secondes"
            else:
                string+= str(seconde) + " seconde"
        return string
