import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout, QSizePolicy, QTabWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QComboBox, QGroupBox, QSplitter, QMessageBox, QButtonGroup, QRadioButton, QTimeEdit, QStackedLayout, QFileDialog, QColorDialog, QScrollArea
from PySide6.QtGui import QPalette, QColor, QFont, QPainter, QBrush, QPixmap, QFontDatabase, QCloseEvent, QTextLayout
from PySide6.QtCore import Qt, QRect, QPoint, QTime
# from controle import Ui_MainWindow as Ui_controle

from ColorPicker import ColorPicker_group, ColorPicker, ColorPickerAvecAppliquer_group
from horloges import QTime_perso, Horloge_controle, Horloge_affichage
from qlabels_persos import resizingLabel, _QLabel_proportionnel_au_premier_parent_d_affichage
from constants import DEBUG, NOM_APPLI, ADRESSE_SITE
from fautes import _Fautes
from score import _Score
from equipe import EquipeAffichage

class radio_lineedit(QWidget):
    'objet créé pour une saisie élaborée dans un QButtonGroup : lineedit avec un bouton radio'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.radio = QRadioButton()
        self.qlineedit = QLineEdit()
        self.qlineedit.setClearButtonEnabled(True)
        self.qlineedit.setMaxLength(30)
        self.qlineedit.textChanged.connect(self.radio.click)
        layout.addWidget(self.radio)
        layout.addWidget(self.qlineedit)
        self.setLayout(layout)

class radio_combobox(QWidget):
    'objet créé pour une saisie élaborée dans un QButtonGroup : combobox avec un bouton radio'
    def __init__(self, list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.radio = QRadioButton()
        self.combobox = QComboBox()
        self.combobox.addItems(list)
        self.combobox.activated.connect(self.radio.click)
        layout.addWidget(self.radio)
        layout.addWidget(self.combobox)
        self.setLayout(layout)

class Color(QWidget):
    'classe pratique en debug pour des tests'
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class ImageSelector(QGroupBox):
    def __init__(self, nom):
        super().__init__(nom)
        # self.setWindowTitle("Image Selector")
        # self.setGeometry(100, 100, 300, 200)
        self.layout = QVBoxLayout()
        self.file_path = ""   
        self.image_label = QLabel("No image selected")
        # self.image_label = resizingLabel("No image selected")
        self.image_label.setMinimumSize(0, 100)  # Minimum width of 0 pixels, minimum height 30
        size_policy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.image_label.setSizePolicy(size_policy)
        if DEBUG :
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(255, 0, 0))  # Red color as an example
            self.image_label.setPalette(palette)
            self.image_label.setAutoFillBackground(True)
        self.layout.addWidget(self.image_label)

        self.browse_button = QPushButton("Parcourir")
        self.browse_button.clicked.connect(self.browse_image)
        self.layout.addWidget(self.browse_button)

        checkbox = QWidget()
        checkbox_layout = QHBoxLayout()
        checkbox_label = QLabel("Afficher l'image")
        self.checkbox_checkbox = QCheckBox()
        checkbox_layout.addWidget(self.checkbox_checkbox, 0)
        checkbox_layout.addWidget(checkbox_label, 1)
        checkbox.setLayout(checkbox_layout)
        self.layout.addWidget(checkbox)
        self.setLayout(self.layout)
        # # Connect resize event
        # self.resizeEvent = self.on_resize

    def browse_image(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp *.jpeg)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setViewMode(QFileDialog.List)

        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.file_path = file_path
            pixMap = QPixmap(file_path)
            self.layout.setStretchFactor(self.image_label, 1)
            self.setLayout(self.layout)
            # label_height = self.image_label.height()
            # scaled_pixmap = pixMap.scaledToHeight(label_height)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            # self.image_label.setPixmap(scaled_pixmap)
            # self.afficher_miniature_cote_controle(pixMap)
            self.checkbox_checkbox.setChecked(True)
            self.image_label.setPixmap(pixMap)
            # self.checkbox_checkbox.setChecked(True)
            # self.image_label.repaint()

    # def afficher_miniature_cote_controle(self, pixMap):
    #     self.image_label.setPixmap(pixMap)
    #     # label_width = self.image_label.width()
    #     # label_height = self.image_label.height()
    #     # pixmap_width = pixMap.width()
    #     # pixmap_height = pixMap.height()
    #     # ratio_from_width = pixmap_width/label_width
    #     # ratio_from_height = pixmap_height/label_height
    #     # if ratio_from_height > ratio_from_width :
    #     #     pixMap_controle = pixMap.scaledToWidth(label_width)
    #     # else :
    #     #     pixMap_controle = pixMap.scaledToHeight(label_height)
    #     # self.image_label.setPixmap(pixMap_controle)
    #     # self.prev_size = self.image_label.size()
    #     self.checkbox_checkbox.setChecked(True)

    # def on_resize(self, event):
    #     super().resizeEvent(event)
    #     print(event)
    #     if self.file_path is not None:
    #         print("PAC3")
    #         # Get the new size of the widget
    #         new_size = event.size()
    #         pixmap = QPixmap(self.file_path)
    #         # Calculate the scaled size of the pixmap based on the new size of the widget
    #         scaled_pixmap = pixmap.scaledToWidth(new_size.width())
    #             # scaled(new_size, Qt.KeepAspectRatio)
    #         # Update the pixmap of the label
    #         self.image_label.setPixmap(scaled_pixmap)




    # def paintEvent(self, e):
    #     super().paintEvent(e)
    #     if hasattr(self, 'prev_size'):
    #         if self.file_path is not None:
    #             if self.image_label.size() != self.prev_size:
    #                     self.image_label = QPixmap()
    #                     pixMap = QPixmap(self.file_path)
    #                     self.afficher_miniature_cote_controle(pixMap)

class FenetreAffichage(QWidget):
    """
    Fenêtre "Affichage" destiné à être visualisé par le public sur un écran à part.
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    self.controle donné, contrôle la fenêtre ; n'est utilisé que pour la fermeture jointe.
    self.unite_taille_affichage VARIE et permet de faire fonctionner les _QLabel_proportionnel_au_premier_parent_d_affichage avec largeur_fenetre_unitaire hauteur_fenetre_unitaire fixes
    self.grille_intermediare est un QStackedLayout pour les différents moments du math : hymne, ...
    Ces affichages différents : standard (avec tout), carton pour l'annonce de l'impro, vote, hymne, entracte
    afficher_* permettent de basculer la grille_intermediare
    update_* pour entériner les changements de valeurs affichées ; appelées depuis le contrôle avec transmission de dict.
    clear_* pour vider les champs affichés avant l'arrivée de nouvelles valeurs
    paintEvent repeint.
    closeEvent : gestion de la femreture

    """   
    def __init__(self, fonts, controle):
        """Init avec éléments factorisés dans des méthodes de classe"""
        super().__init__()

        # Calcul de la taille de fenêtre
        # Pour une taille de vidéoproj imaginée à 3840 x 2160, partons sur une taille
        # de fenêtre pour le dev de 1920x1080 -> 960x540 qui serait pour unité_taille_affichage = 1
        # 540 a pour diviseurs : 12, 15, 18
        # Après adaptation 231208 : 0 19 -> 20 colonnes, 0 14 (pas de bandeau) -> 15 lignes
        # self.background_pixmap = QPixmap("./background_light.png")
        self.background_pixmap = QPixmap("./background_wallpaper.jpg")
        self.image_de_fond_affiche = True
        self.couleur_de_fond = QColor("black")
        self.couleur_de_fond_affiche = False

        self.largeur_fenetre_unitaire = 96
        self.hauteur_fenetre_unitaire = 54
        nombre_de_lignes = 15
        nombre_de_colonnes = 20
        self.unite_taille_affichage = 10  # varie : self.unite_taille_affichage = self.width()/self.largeur_fenetre_unitaire
        # attention : self.unite_taille_affichage est aussi utilisé à l'init de _QLabel_proportionnel_au_premier_parent_d_affichage dans fontMaker

        width = self.largeur_fenetre_unitaire*self.unite_taille_affichage  # soit en unitaire : 48
        height = self.hauteur_fenetre_unitaire*self.unite_taille_affichage # soit en unitaire : 36
        self.setMinimumSize(width, height) 

        unite_margin_size= 10
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        largeur_case_pixmap = self.unite_taille_affichage * self.largeur_fenetre_unitaire/nombre_de_colonnes
        hauteur_case_pixmap = self.unite_taille_affichage * self.hauteur_fenetre_unitaire/nombre_de_lignes
        
        self.controle = controle  # Juste pour la fermeture

        # comportement des cases de la grille à l'extension et à la réduction
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        self.equipe_gauche = EquipeAffichage("gauche", fonts["dita"])
        self.equipe_droite = EquipeAffichage("droite", fonts["dita"])
        self.init_des_QLabel_proportionnel_au_premier_parent_d_affichages(sizePolicy, fonts)

        self.temps_impro_standard = Horloge_affichage(fonts)
        self.temps_impro_carton = Horloge_affichage(fonts)
        self.score_gauche = _Score("gauche", fonts["mikodacs"])
        self.score_droit = _Score("droite", fonts["mikodacs"])
        self.score_gauche.setSizePolicy(sizePolicy)
        self.score_droit.setSizePolicy(sizePolicy)
        self.fautes_gauche = _Fautes("gauche")
        self.fautes_droite = _Fautes("droite")
        # self.fautes_gauche.setSizePolicy(sizePolicy)
        self.fautes_droite.setSizePolicy(sizePolicy)

        self.panneau_standard = QWidget()
        self.panneau_carton = QWidget()
        self.panneau_hymne = QWidget()
        self.panneau_vote = QWidget()
        self.panneau_entracte = QWidget()

        self.layout(fonts)

    def init_des_QLabel_proportionnel_au_premier_parent_d_affichages(self, sizePolicy, fonts):
        """
        avec au passage enregistrement de fonts.
        Initialisation des éléments textes de la fenêtre publique. Ce sont des éléments de taille dynamique,
        proportionnels à "unite_taille_affichage" de la fenêtre publique ; au 240127, la largeur.
        """
        # Préparation des fonts en local grâce à QFontDatabase
        # Ceux pour les custom widgets sont gérés en eux-même  

        # Préparation des arguments pour _QLabel_proportionnel_au_premier_parent_d_affichage
        # Choix des paramètres de police
        font_theme_standard_tup = (fonts["komika"], 10, QFont.Bold)
        font_categorie_standard_tup = (fonts["technasans"], 6, QFont.Bold)
        font_one_line_standard_tup = (fonts["technasans"], 4,)
        # font_equipe = (fonts["dita"], 5, QFont.Bold)

        font_nature_carton_tup = (fonts["technasans"], 5, QFont.Bold)
        font_theme_carton_tup = (fonts["technasans"], 10, QFont.Bold)
        font_categorie_carton_tup = (fonts["technasans"], 8, QFont.Bold)
    
        font_nombre_joueurs_carton_tup = (fonts["technasans"], 6, QFont.Bold)

        # Création des qlabel avec qqchose écrit à l'interieur
        # Standard
        self.nature_impro_standard = _QLabel_proportionnel_au_premier_parent_d_affichage("Nature de l'impro : mixte ou comparée", *font_one_line_standard_tup)
        # self.theme_impro_standard = _QLabel_proportionnel_au_premier_parent_d_affichage("Thème de l'impro, qui peut être un titre plutôt long. Qu'en pensez-vous ?", *font_theme_standard_tup)  # , **font_theme_dic)
        self.theme_impro_standard = _QLabel_proportionnel_au_premier_parent_d_affichage("Thème", *font_theme_standard_tup)  # , **font_theme_dic)
        self.categorie_impro_standard = _QLabel_proportionnel_au_premier_parent_d_affichage("Catégorie de l'impro", *font_categorie_standard_tup)
        self.nbre_joueurs_standard = _QLabel_proportionnel_au_premier_parent_d_affichage("Nombre de joueurs", *font_one_line_standard_tup)
        # Carton
        self.nature_impro_carton = _QLabel_proportionnel_au_premier_parent_d_affichage("Nature de l'impro : mixte ou comparée", *font_nature_carton_tup)
        if DEBUG : self.nature_impro_carton.setAutoFillBackground(True)
        self.theme_impro_carton = _QLabel_proportionnel_au_premier_parent_d_affichage("Thème de l'impro, qui peut être un titre plutôt long. Qu'en pensez-vous ", *font_theme_carton_tup)  # , **font_theme_dic)
        if DEBUG : self.theme_impro_carton.setAutoFillBackground(True)
        self.categorie_impro_carton = _QLabel_proportionnel_au_premier_parent_d_affichage("Catégorie de l'impro", *font_categorie_carton_tup)
        if DEBUG : self.categorie_impro_carton.setAutoFillBackground(True)
        self.nbre_joueurs_carton = _QLabel_proportionnel_au_premier_parent_d_affichage("Nombre de joueurs", *font_nombre_joueurs_carton_tup)
        if DEBUG : self.nbre_joueurs_carton.setAutoFillBackground(True)

        # self.temps_impro = _QLabel_proportionnel_au_premier_parent_d_affichage("temps_impro", *font_one_line_standard_tup)
        self.titre_spectacle_vs = _QLabel_proportionnel_au_premier_parent_d_affichage("Titre du spectacle", *font_one_line_standard_tup)
        self.intitule_periode = _QLabel_proportionnel_au_premier_parent_d_affichage("Intitulé de la période", *font_one_line_standard_tup)
        self.temps_periode = _QLabel_proportionnel_au_premier_parent_d_affichage("", *font_one_line_standard_tup)
        
        self.theme_impro_carton.setSizePolicy(sizePolicy)
        self.categorie_impro_carton.setSizePolicy(sizePolicy)
        self.nbre_joueurs_carton.setSizePolicy(sizePolicy)
        self.nature_impro_carton.setSizePolicy(sizePolicy)
        
        
        # self.equipe_gauche.setSizePolicy(sizePolicy)
        # self.equipe_droite.setSizePolicy(sizePolicy)

        # setAlignment
        self.nature_impro_standard.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.theme_impro_standard.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.categorie_impro_standard.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)      
        self.nbre_joueurs_standard.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)       
        self.nature_impro_carton.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.theme_impro_carton.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.categorie_impro_carton.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)      
        self.nbre_joueurs_carton.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)       
        
        # self.equipe_gauche.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        # self.equipe_droite.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.titre_spectacle_vs.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.intitule_periode.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.temps_periode.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    def layout(self, fonts):
        """Ici se définit l'arrangement de la fenêtre avec tous ses éléments'"""
        
        self.grille_intermediare = QStackedLayout(self)
        self._layout_panneau_standard()
        self._layout_panneau_carton()
        self._layout_panneau_hymne(fonts)
        self._layout_panneau_vote(fonts)
        self._layout_panneau_entracte(fonts)

        self.grille_intermediare.addWidget(self.panneau_standard)
        self.grille_intermediare.addWidget(self.panneau_carton)
        self.grille_intermediare.addWidget(self.panneau_hymne)
        self.grille_intermediare.addWidget(self.panneau_vote)
        self.grille_intermediare.addWidget(self.panneau_entracte)
        self.grille_intermediare.setCurrentIndex(0)
    
    def _layout_panneau_standard(self):

        # Blocs Fautes + Scores
        bloc_score_gauche_layout = QVBoxLayout()
        bloc_score_gauche_layout.addWidget(self.score_gauche)
        bloc_score_gauche_layout.addWidget(self.fautes_gauche)
        bloc_score_gauche = QWidget()
        bloc_score_gauche.setLayout(bloc_score_gauche_layout)

        bloc_score_droit_layout = QVBoxLayout()
        bloc_score_droit_layout.addWidget(self.score_droit)
        bloc_score_droit_layout.addWidget(self.fautes_droite)
        bloc_score_droit = QWidget()
        bloc_score_droit.setLayout(bloc_score_droit_layout)

        # Bloc Versus et infos spectacle
        bloc_versus_infos_spectacle_layout = QVBoxLayout()
        bloc_versus_infos_spectacle_layout.addWidget(self.titre_spectacle_vs)
        bloc_versus_infos_spectacle_layout.addWidget(self.intitule_periode)
        bloc_versus_infos_spectacle_layout.addWidget(self.temps_periode)
        bloc_versus_infos_spectacle = QWidget()
        bloc_versus_infos_spectacle.setLayout(bloc_versus_infos_spectacle_layout)

        # bloc nombre_joueurs et temps impro et nature
        
        bloc_nature_nombre_joueurs_layout = QVBoxLayout()
        bloc_nature_nombre_joueurs_layout.addWidget(self.nature_impro_standard)
        bloc_nature_nombre_joueurs_layout.addWidget(self.nbre_joueurs_standard)
        bloc_nature_nombre_joueurs = QWidget()
        bloc_nature_nombre_joueurs.setLayout(bloc_nature_nombre_joueurs_layout)
        bloc_nature_nombre_joueurs_temps_layout = QHBoxLayout()
        bloc_nature_nombre_joueurs_temps_layout.addWidget(bloc_nature_nombre_joueurs)
        bloc_nature_nombre_joueurs_temps_layout.addWidget(self.temps_impro_standard)
        bloc_nature_nombre_joueurs_temps = QWidget()
        bloc_nature_nombre_joueurs_temps.setLayout(bloc_nature_nombre_joueurs_temps_layout)

        # size_policy = self.temps_impro_standard.sizePolicy()
        # # Print the horizontal and vertical size policies
        # print(f"Horizontal size policy: {size_policy.horizontalPolicy()}")
        # print(f"Vertical size policy: {size_policy.verticalPolicy()}")
        # size_policy = self.temps_impro_standard.cadran_analogique.sizePolicy()
        # # Print the horizontal and vertical size policies
        # print(f"Horizontal size policy: {size_policy.horizontalPolicy()}")
        # print(f"Vertical size policy: {size_policy.verticalPolicy()}")

        #Grid
        panneau_standard_layout = QGridLayout()
        # ordonnée, abscisse, rowspan, columnspan,
        panneau_standard_layout.addWidget(bloc_score_gauche, 0, 1, 2, 2)
        panneau_standard_layout.addWidget(bloc_score_droit, 0, 14, 2, 2)
        panneau_standard_layout.addWidget(bloc_versus_infos_spectacle, 0,7,1,3)
        panneau_standard_layout.addWidget(self.equipe_gauche, 3,0,2,4)
        panneau_standard_layout.addWidget(self.equipe_droite, 3,13,2,4)
        panneau_standard_layout.addWidget(bloc_nature_nombre_joueurs_temps, 4, 6, 2, 5)
        panneau_standard_layout.addWidget(self.theme_impro_standard, 6, 2, 1, 13)
        panneau_standard_layout.addWidget(self.categorie_impro_standard, 7,5,1,7)
        

        if DEBUG:
            rowcount = panneau_standard_layout.rowCount()
            columncount = panneau_standard_layout.columnCount()
            # i = 0
            # j = 0
            for i in range(columncount):
                for j in range(rowcount):
                    label = QLabel("(" + str(j) + ", " + str(i) + ")")
                    label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                    panneau_standard_layout.addWidget(label, j, i)
        
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.nature_impro_standard.setSizePolicy(sizePolicy)
        self.categorie_impro_standard.setSizePolicy(sizePolicy)
        self.nbre_joueurs_standard.setSizePolicy(sizePolicy)

        self.panneau_standard.setLayout(panneau_standard_layout)

    def _layout_panneau_carton(self):
        panneau_carton_layout = QGridLayout()
        # nombre_de_colonnes = 16
        
        # # ordonnée, abscisse, yspan, xspan,
        panneau_carton_layout.addWidget(self.nature_impro_carton, 0, 3, 2, 10)
        panneau_carton_layout.addWidget(self.theme_impro_carton, 2, 1, 4, 14)
        panneau_carton_layout.addWidget(self.categorie_impro_carton, 6, 3, 3, 10)
        panneau_carton_layout.addWidget(self.nbre_joueurs_carton, 9, 4, 2, 8)
        panneau_carton_layout.addWidget(self.temps_impro_carton, 11, 6, 2, 4)
        self.panneau_carton.setLayout(panneau_carton_layout)
    
    def _layout_panneau_vote(self, fonts):
        panneau_vote_layout = QVBoxLayout()
        font_vote_tup = (fonts["komika"], 15, QFont.Bold)
        vote_label = _QLabel_proportionnel_au_premier_parent_d_affichage("vote", *font_vote_tup)
        vote_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        panneau_vote_layout.addWidget(vote_label)
        self.panneau_vote.setLayout(panneau_vote_layout)

    def _layout_panneau_hymne(self, fonts):
        panneau_hymne_layout = QVBoxLayout()
        font_hymne_tup = (fonts["komika"], 15, QFont.Bold)
        hymne_label = _QLabel_proportionnel_au_premier_parent_d_affichage("Hymne", *font_hymne_tup)
        hymne_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        panneau_hymne_layout.addWidget(hymne_label)
        self.panneau_hymne.setLayout(panneau_hymne_layout)

    def _layout_panneau_entracte(self, fonts):
        panneau_entracte_layout = QVBoxLayout()
        font_entracte_tup = (fonts["komika"], 15, QFont.Bold)
        entracte_label = _QLabel_proportionnel_au_premier_parent_d_affichage("Entracte", *font_entracte_tup)
        entracte_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        panneau_entracte_layout.addWidget(entracte_label)
        self.panneau_entracte.setLayout(panneau_entracte_layout)

    def afficher_Standard(self):
        self.grille_intermediare.setCurrentIndex(0)

    def afficher_Carton(self):
        self.grille_intermediare.setCurrentIndex(1)

    def afficher_Hymne(self):
        self.grille_intermediare.setCurrentIndex(2)

    def afficher_Vote(self):
        self.grille_intermediare.setCurrentIndex(3)

    def afficher_Entracte(self):
        self.grille_intermediare.setCurrentIndex(4)

    def update_spectacle(self, dict):
        """appélé par le bouton de l'onglet spectacle de la fenêtre de contrôle pour update"""
        self.titre_spectacle_vs.setText(dict["titre_spectacle"])
        nom_gauche = dict['equipeGauche_nom']
        nom_droite = dict['equipeDroite_nom']
        
        self.equipe_gauche.nomAffiche = dict['equipeGauche_nomAffiche']
        self.equipe_droite.nomAffiche = dict['equipeDroite_nomAffiche']
        couleur_texte_gauche = dict['equipeGauche_nomCouleur']
        couleur_texte_droite = dict['equipeDroite_nomCouleur']
        couleur_texte_gauche_css = f"rgb({couleur_texte_gauche.red()}, {couleur_texte_gauche.green()}, {couleur_texte_gauche.blue()})"
        couleur_texte_droite_css = f"rgb({couleur_texte_droite.red()}, {couleur_texte_droite.green()}, {couleur_texte_droite.blue()})"
        self.equipe_gauche.label.setStyleSheet("color: "+ f"{couleur_texte_gauche_css};");
        self.equipe_droite.label.setStyleSheet("color: "+ f"{couleur_texte_droite_css};");
        # self.equipe_gauche.label.palette.setColor(label_palette.Text, Qt.red)

        if dict['equipeGauche_nomAffiche'] and dict['equipeDroite_nomAffiche']:
            # Traitement d'égalité de place
            nom_gauche = dict['equipeGauche_nom']
            nom_droite = dict['equipeDroite_nom']
            longueur_de_chaine = max(len(nom_gauche), len(nom_droite))
            espaces_pour_gauche = longueur_de_chaine-len(nom_gauche)
            nom_gauche = nom_gauche.rjust(2*espaces_pour_gauche)
            # nom_gauche = ('{: >espaces_pour_gauche}'.format(nom_gauche))
            espaces_pour_droite = longueur_de_chaine-len(nom_droite)
            nom_droite = nom_droite.ljust(2*espaces_pour_droite)
            # nom_droite = ('{: >espaces_pour_droite}'.format(nom_droite))

        if self.equipe_gauche.nomAffiche:
            self.equipe_gauche.nom = nom_gauche
            self.equipe_gauche.label.setText(nom_gauche)
        else:
            self.equipe_gauche.nom = ""
            self.equipe_gauche.label.setText("")

        couleurMaillotGauche = dict['equipeGauche_couleurMaillot']
        if couleurMaillotGauche is not None:
            self.equipe_gauche.maillotAffiche = dict['equipeGauche_maillotAffiche']
            if self.equipe_gauche.maillotAffiche:
                self.equipe_gauche.couleurMaillot = couleurMaillotGauche
        else:
            self.equipe_gauche.maillotAffiche = False

        couleurCartonGauche = dict['equipeGauche_couleurCarton']
        if couleurCartonGauche is not None:
            self.equipe_gauche.cartonAffiche = dict['equipeGauche_cartonAffiche']
            if self.equipe_gauche.cartonAffiche:
                self.equipe_gauche.couleurCarton = couleurCartonGauche
        else:
            self.equipe_gauche.cartonAffiche = False
        
        logo_gauche = dict['equipeGauche_logo_file_path']
        if logo_gauche != "":
            self.equipe_gauche.logo = QPixmap(dict['equipeGauche_logo_file_path'])
            self.equipe_gauche.logoAffiche = dict['equipeGauche_logoAffiche']
            self.equipe_gauche.repaint()
        else:
            self.equipe_gauche.logoAffiche = False
        
        if self.equipe_droite.nomAffiche:
            self.equipe_droite.nom = nom_droite
            self.equipe_droite.label.setText(nom_droite)
        else:
            self.equipe_droite.nom = ""
            self.equipe_droite.label.setText("")
        
        couleurMaillotDroite = dict['equipeDroite_couleurMaillot']
        if couleurMaillotDroite is not None:
            self.equipe_droite.maillotAffiche = dict['equipeDroite_maillotAffiche']
            if self.equipe_droite.maillotAffiche:
                self.equipe_droite.couleurMaillot = couleurMaillotDroite
        else:
            self.equipe_droite.maillotAffiche = False

        couleurCartonDroite = dict['equipeDroite_couleurCarton']
        if couleurCartonDroite is not None:
            self.equipe_droite.cartonAffiche = dict['equipeDroite_cartonAffiche']
            if self.equipe_droite.cartonAffiche:
                self.equipe_droite.couleurCarton = couleurCartonDroite
        else:
            self.equipe_droite.cartonAffiche = False
        
        logo_droite = dict['equipeDroite_logo_file_path']
        if logo_droite != "":
            self.equipe_droite.logo = QPixmap(dict['equipeDroite_logo_file_path'])
            self.equipe_droite.logoAffiche = dict['equipeDroite_logoAffiche']
            self.equipe_droite.repaint()
        else:
            self.equipe_droite.logoAffiche = False

        # self.update()
        self.repaint()
    
    def update_periode(self, dict):
        """appélé par le bouton de l'onglet periode de la fenêtre de contrôle pour update"""
        self.intitule_periode.setText(dict["nomPeriode"])
        self.temps_periode.setText(dict["dureePeriode"])

    def update_impro_cote_affichage(self, dict):
        """appélé par le bouton de l'onglet impro de la fenêtre de contrôle pour update"""
        theme = dict["theme"]
        if len(theme) > 22:
            theme_23 = theme[:23] + " (...)"
            self.theme_impro_carton.setText(theme_23)
        else:
            self.theme_impro_carton.setText(theme)
        if len(theme) > 25:
            theme_25 = theme[:25] + " (...)"
            self.theme_impro_standard.setText(theme_25)
        else:
            self.theme_impro_standard.setText(theme)

        categorie = dict["categorie"]
        if categorie == "":
            self.categorie_impro_carton.setText("")
            self.categorie_impro_standard.setText("")
        else:
            self.categorie_impro_carton.setText("Catégorie : " + categorie)
            self.categorie_impro_standard.setText("Catégorie : " + categorie)

        duree = dict["duree_t"]
        if duree != QTime(0, 0, 0, 0):
            self.temps_impro_carton.set_time(dict["duree_t"])
            self.temps_impro_standard.set_time(dict["duree_t"])  
        
        self.nbre_joueurs_carton.setText(dict["nombreDeJoueurs"])
        self.nature_impro_carton.setText(dict["nature"])
        
        self.nbre_joueurs_standard.setText(dict["nombreDeJoueurs"])
        self.nature_impro_standard.setText(dict["nature"])

    def update_couleurs_horloge(self,dict):
        couleur_temps_initial = dict["couleur_temps_initial"]
        self.temps_impro_carton.cadran_analogique.couleur_temps_initial = couleur_temps_initial
        self.temps_impro_standard.cadran_analogique.couleur_temps_initial = couleur_temps_initial

        couleur_temps_écoulé = dict["couleur_temps_écoulé"]
        self.temps_impro_carton.cadran_analogique.couleur_temps_ecoule = couleur_temps_écoulé
        self.temps_impro_standard.cadran_analogique.couleur_temps_ecoule = couleur_temps_écoulé
    
    def update_couleur_score(self,dict):
        couleur_ellipse_score = dict["couleur_ellipse_score"]
        afficher_couleur_ellipse_score = dict["afficher_couleur_ellipse_score"]
        if isinstance(couleur_ellipse_score, QColor):
            if couleur_ellipse_score.isValid() and afficher_couleur_ellipse_score:
                self.score_droit.couleur_ellipse = couleur_ellipse_score
                self.score_droit.repaint()
                self.score_gauche.couleur_ellipse = couleur_ellipse_score
                self.score_gauche.repaint()
    
    def update_arriere_plan(self,dict):    
        couleur_de_fond = dict["couleur_de_fond"]
        couleur_de_fond_affiche = dict["couleur_de_fond_affiche"]
        image_de_fond = dict["image_de_fond"]
        image_de_fond_affiche = dict["image_de_fond_affiche"]

        if image_de_fond is not None and image_de_fond_affiche:
            self.background_pixmap = image_de_fond
            self.image_de_fond_affiche = True
        else:
            self.image_de_fond_affiche = False
            if couleur_de_fond is not None and couleur_de_fond_affiche:
                self.couleur_de_fond = couleur_de_fond
                self.couleur_de_fond_affiche = True
            else:
                self.couleur_de_fond_affiche = False
        self.repaint()
    
    def clear_impro_cote_affichage(self):
        """appélé par le bouton clear de l'onglet impro de la fenêtre de contrôle"""
        self.theme_impro_standard.setText("")
        self.categorie_impro_standard.setText("")
        self.nbre_joueurs_standard.setText("")
        self.nature_impro_standard.setText("")
        self.temps_impro_standard.clear()
        self.theme_impro_carton.setText("")
        self.categorie_impro_carton.setText("")
        self.nbre_joueurs_carton.setText("")
        self.nature_impro_carton.setText("")
        self.temps_impro_carton.clear()

    def clear_periode_cote_affichage(self):
        """appélé par le bouton clear de l'onglet periode de la fenêtre de contrôle"""
        self.intitule_periode.setText("")
        self.temps_periode.setText("")
        
    def paintEvent(self, e):
        painter = QPainter(self)
        largeur = self.width()
        hauteur = self.height()
        if self.image_de_fond_affiche:
            painter.drawPixmap(QRect(0, 0, largeur, hauteur), self.background_pixmap)
        elif self.couleur_de_fond_affiche:
            painter.fillRect(QRect(0, 0, largeur, hauteur), self.couleur_de_fond)
        else:
            painter.fillRect(QRect(0, 0, largeur, hauteur), QColor("black"))
        
        # painter.drawPixmap(self.rect(), self.background_pixmap)  # The rect property equals QRect (0, 0, width() , height()
        # super().paintEvent(e)
        # on recalcule self.unite_taille_affichage par la largeur (on ignore la hauteur). Car largeur ce sont de plus gros nombres
        self.unite_taille_affichage = largeur/self.largeur_fenetre_unitaire
        super().paintEvent(e)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        '''Appelé lorsqu'on ferme la fenêtre. Ferme celle-ci seulement si la fenêtre de contrôle devait déjà être fermée.'''
        if DEBUG == True:
            event.ignore()
            self.controle.close()
        else:
            if self.controle is None:
                event.accept()
            else:
                event.ignore()
                self.controle.close()

    # def _trigger_refresh(self):
    #     self.update()
        
class ControleAffichage(QMainWindow): #, Ui_controle):
    """
    Fenêtre "Contrôle" de la fenêtre "affichage". Composée d'onglets.
    fautes et scores sont stockées ici
    self.unite_taille_affichage = 5 car le premier onglet a des QLabel_proportionnel
    temps_impro_controle est une Horloge_Contrôle
    _init_tab* pour créer les tabs
    Certaines tabs ont tout ce qui faut pour la mise à jour.
    update_impro_cote_controle
    _proxy_score_faute : fonction factorisée pour mettre à jour fautes et scores
    clear_* pour vider les champs côté affichage aussi
    closeEvent pour la fermeture conjointe
    _update_resolution
    _toggle_fullscreen
    paintEvent

    """
    def __init__(self, fonts):
        super().__init__()

        self.setWindowTitle("My App")

        # self.resize(800, 600)

        self.largeur_fenetre_unitaire = 160  # euh... 240129 : ça fait longtemps que j'ai créé le concept. Si self.unite_taille_affichage*self.unite_taille_affichage = 800px alors : 80

        self.derniere_valeur_largeur_affichage = 0
        self.derniere_valeur_hauteur_affichage = 0

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred
            
            # QSizePolicy.Policy.Minimum,
            # QSizePolicy.Policy.Minimum
        )

        self.fautes_gauche = 0
        self.fautes_gauche_nombre_de_clics = 0
        self.fautes_droite = 0
        self.fautes_droite_nombre_de_clics = 0
        self.score_gauche = 0
        self.score_droit = 0

        self.unite_taille_affichage = 5  # varie : self.unite_taille_affichage = self.width()/self.largeur_fenetre_unitaire
        # attention : self.unite_taille_affichage est aussi utilisé à l'init de _QLabel_proportionnel_au_premier_parent_d_affichage dans fontMaker

        self.affichage = FenetreAffichage(fonts, self)
        self.affichage.show()

        tabs = QTabWidget()
        tabs.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred
        )
        tabs.setDocumentMode(True)
        tabs.setTabPosition(QTabWidget.West)
        # tabs.setMovable(True)

        tabs.addTab(self._init_tab_aide(fonts), NOM_APPLI)
        tabs.addTab(self._init_tab_parametres(), "Paramètres")
        tabs.addTab(self._init_tab_spectacle(), "Spectacle")
        tabs.addTab(self._init_tab_periode(), "Période")
        tabs.addTab(self._init_tab_impro(), "Impro")
        if DEBUG == True:
            tabs.setCurrentIndex(4)
        
        # Tab pour les paramètres
        # Choix de résolution avec une liste déroulante mais aussi en saisie libre
        # Choix d'une image de fond
        # Choix des couleurs
        # Save/Load des couleurs

        self.setCentralWidget(tabs)
    
    def _init_tab_aide(self, fonts):
        # font_equipe = (fonts["dita"], 4, QFont.Bold)
        # self.equipe_gauche = _QLabel_proportionnel_au_premier_parent_d_affichage("equipe_gauche", *font_equipe)
        titreTab = QWidget()
        
        font_titre = (fonts["dita"], 5, QFont.Bold)
        self.titre_appli = _QLabel_proportionnel_au_premier_parent_d_affichage(NOM_APPLI, *font_titre)
        self.titre_appli.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        font_auteur = (fonts["liberation"], 2,)
        auteur_appli = _QLabel_proportionnel_au_premier_parent_d_affichage("par BG", *font_auteur)
        auteur_appli.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        font_standard = (fonts["liberation"], 3,)
        adresse_site = _QLabel_proportionnel_au_premier_parent_d_affichage(ADRESSE_SITE, *font_standard)
        adresse_site.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            
        # texte = NOM_APPLI + " est un outil d'affichage de score de match d'impro. Il est composé de deux fenêtres : une fenêtre publique et une fenêtre de contrôle. \n" + \
        # "La fenêtre publique est destinée à être visible par le public, idéalement sur un vidéoprojecteur. On interagira avec la fenêtre de contrôle, cette fenêtre, depuis l'ordinateur relié au vidéoprojecteur."
        # aide = _QLabel_proportionnel_au_premier_parent_d_affichage(texte, *font_standard)
        
        texte = NOM_APPLI + " est un outil d'affichage de score de match d'impro. Il est composé de deux fenêtres : une fenêtre publique et une fenêtre de contrôle. " + \
        "La fenêtre publique est destinée à être visible par le public, idéalement sur un vidéoprojecteur. On interagira avec la fenêtre de contrôle, cette fenêtre, depuis l'ordinateur relié au vidéoprojecteur."
        aide = QLabel(texte)
        aide.setWordWrap(True)
        
        # aide.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        titreTab_layout = QVBoxLayout()
        titreTab_layout.addWidget(self.titre_appli, 2)  # Noter le poids du widget ajouté à la suite.
        titreTab_layout.addWidget(auteur_appli, 1)
        titreTab_layout.addWidget(adresse_site, 1)
        titreTab_layout.addWidget(aide, 8)
        
        # titreTab.setSizePolicy(
        #     QSizePolicy.Policy.MinimumExpanding,
        #     QSizePolicy.Policy.MinimumExpanding,

        # )
        titreTab.setLayout(titreTab_layout)
        return titreTab

    def _init_tab_impro(self):
        # Tab pour les inputs de l'impro
        improTab_splitter = QSplitter(Qt.Horizontal)
        impro_goup = QGroupBox("Impro", improTab_splitter)
        impro_layout = QGridLayout()
        nombre_de_colonnes = 5

        self.mode_standard_button = QPushButton("Passer la fenêtre publique en mode standard")
        self.mode_standard_button.clicked.connect(self.affichage.afficher_Standard)
        impro_layout.addWidget(self.mode_standard_button, 0, 1, 1, 1)
        
        self.mode_carton_button = QPushButton("Passer la fenêtre publique en mode annonce de thème")
        self.mode_carton_button.clicked.connect(self.affichage.afficher_Carton)
        impro_layout.addWidget(self.mode_carton_button, 0, 2, 1, 1)

        self.layout_nature = QHBoxLayout()
        self.qlabel_nature = QLabel("Nature de l'improvisation : ")
        self.buttonGroupe_nature = QButtonGroup()
        self.mixte_button = QRadioButton('Mixte')
        self.comparee_button = QRadioButton('Comparée')
        self.naturePersonnalisable_radio_lineedit = radio_lineedit()
        # self.naturePersonnalisable_button.setPlaceholderText("Selon votre envie")
        self.buttonGroupe_nature.addButton(self.mixte_button)
        self.buttonGroupe_nature.addButton(self.comparee_button)
        self.buttonGroupe_nature.addButton(self.naturePersonnalisable_radio_lineedit.radio)
        self.layout_nature.addWidget(self.qlabel_nature)
        self.layout_nature.addWidget(self.mixte_button)
        self.layout_nature.addWidget(self.comparee_button)
        self.layout_nature.addWidget(self.naturePersonnalisable_radio_lineedit)
        self.widget_nature = QWidget()
        self.widget_nature.setLayout(self.layout_nature)
        impro_layout.addWidget(self.widget_nature, 1, 0, 1, nombre_de_colonnes)

        self.qlabel_theme = QLabel("Thème : ")
        self.qlineedit_theme = QLineEdit()
        self.qlineedit_theme.setMaxLength(120)
        self.qlineedit_theme.setPlaceholderText("Entrez un thème")
        impro_layout.addWidget(self.qlabel_theme, 2, 0)
        impro_layout.addWidget(self.qlineedit_theme, 2, 1, 1, nombre_de_colonnes-1)

        self.qlabel_categorie = QLabel("Catégorie : ")
        self.qlineedit_categorie = QLineEdit()
        self.qlineedit_categorie.setMaxLength(20)
        self.qlineedit_categorie.setPlaceholderText("Entrez une catégorie")
        impro_layout.addWidget(self.qlabel_categorie, 3, 0)
        impro_layout.addWidget(self.qlineedit_categorie, 3, 1, 1, nombre_de_colonnes-1)

        self.temps_impro_controle = Horloge_controle(self.affichage.temps_impro_standard, self.affichage.temps_impro_carton)
        impro_layout.addWidget(self.temps_impro_controle, 4, 0, 1, nombre_de_colonnes-1)
        
        self.layout_nombreDeJoueurs = QHBoxLayout()
        self.qlabel_nombreDeJoueurs = QLabel("Nombre de joueurs : ")
        self.buttonGroupe_nombreDeJoueurs = QButtonGroup()
        self.illimite_button = QRadioButton('Illimité')
        liste_de_nombres_de_joueurs = [
            "1 joueur par équipe",
            "2 joueurs par équipe",
            "3 joueurs par équipe",
            "4 joueurs par équipe",
            "5 joueurs par équipe",
            "6 joueurs par équipe",
            "Tout le monde.",
            ]
        self.joueurs_radio_combobox = radio_combobox(list=liste_de_nombres_de_joueurs)
        self.nombreDeJoueurs_radio_lineedit = radio_lineedit()
        self.buttonGroupe_nombreDeJoueurs.addButton(self.illimite_button)
        self.buttonGroupe_nombreDeJoueurs.addButton(self.joueurs_radio_combobox.radio)
        self.buttonGroupe_nombreDeJoueurs.addButton(self.nombreDeJoueurs_radio_lineedit.radio)
        self.layout_nombreDeJoueurs.addWidget(self.qlabel_nombreDeJoueurs)
        self.layout_nombreDeJoueurs.addWidget(self.illimite_button)
        self.layout_nombreDeJoueurs.addWidget(self.joueurs_radio_combobox)
        self.layout_nombreDeJoueurs.addWidget(self.nombreDeJoueurs_radio_lineedit)
        self.widget_nombreDeJoueurs = QWidget()
        self.widget_nombreDeJoueurs.setLayout(self.layout_nombreDeJoueurs)
        impro_layout.addWidget(self.widget_nombreDeJoueurs, 5, 0, 1, nombre_de_colonnes)

        self.update_impro_button = QPushButton("Afficher sur la fenêtre publique")
        self.clear_impro_button =  QPushButton("Effacer sur la fenêtre publique")
        impro_layout.addWidget(self.update_impro_button, 6, 0, 1, nombre_de_colonnes//2+1)
        self.update_impro_button.clicked.connect(self.update_impro_cote_controle)
        impro_layout.addWidget(self.clear_impro_button, 6, nombre_de_colonnes//2+2, 1, 1)
        self.clear_impro_button.clicked.connect(self.clear_impro_cote_controle)
                
        impro_goup.setLayout(impro_layout)

        partie_droite_widget = QWidget(improTab_splitter)
        partie_droite_layout = QVBoxLayout()
        score_group = QGroupBox("Score")
        score_layout = QGridLayout()
        nombre_de_colonnes = 8

        self.mode_vote_button = QPushButton("Passer la fenêtre publique en mode vote")
        self.mode_vote_button.clicked.connect(self.affichage.afficher_Vote)
        score_layout.addWidget(self.mode_vote_button, 0, 2, 2, 4)
        # plus une ligne vide

        self.score_gauche_label = QLabel("0")
        self.score_gauche_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.score_gauche_plus = QPushButton(text="+   Ajouter un point à gauche")
        # self.score_gauche_plus.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.score_gauche_plus.clicked.connect(lambda:self._proxy_score_faute('score', '+', "gauche"))
        self.score_gauche_moins = QPushButton(text="-   Retirer un point à gauche")
        # self.score_gauche_moins.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.score_gauche_moins.clicked.connect(lambda:self._proxy_score_faute('score', '-', "gauche"))
        self.score_droit_label = QLabel("0")
        self.score_droit_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.score_droit_plus = QPushButton(text="Ajouter un point à droite   +")
        # self.score_droit_plus.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.score_droit_plus.clicked.connect(lambda:self._proxy_score_faute('score', '+', "droite"))
        self.score_droit_moins = QPushButton(text="Retirer un point à droite   -")
        # self.score_droit_moins.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.score_droit_moins.clicked.connect(lambda:self._proxy_score_faute('score', '-', "droite"))
        
        # y,x,yspan,xspan
        score_layout.addWidget(self.score_gauche_label, 3, 0, 2, 1)
        score_layout.addWidget(self.score_gauche_plus, 2, 1, 2, 3)
        score_layout.addWidget(self.score_gauche_moins, 4, 1, 2, 3)
        score_layout.addWidget(self.score_droit_plus, 2, 4, 2, 3)
        score_layout.addWidget(self.score_droit_moins, 4, 4, 2, 3)
        score_layout.addWidget(self.score_droit_label, 3, 7, 2, 1)
        score_group.setLayout(score_layout)
        
        fautes_group = QGroupBox("Fautes")
        fautes_layout = QGridLayout()
        self.fautes_gauche_label = QLabel("0")
        self.fautes_gauche_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.fautes_gauche_plus = QPushButton(text="+   Ajouter une faute à gauche")
        self.fautes_gauche_moins = QPushButton(text="-   Retirer une faute à gauche")
        self.fautes_gauche_plus.clicked.connect(lambda :self._proxy_score_faute('faute', '+', "gauche"))
        self.fautes_gauche_moins.clicked.connect(lambda :self._proxy_score_faute('faute', '-', "gauche"))
        self.fautes_droite_label = QLabel("0")
        self.fautes_droite_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.fautes_droite_plus = QPushButton(text="Ajouter une faute à droite   +")
        self.fautes_droite_moins = QPushButton(text="Retirer une faute à droite   -")
        self.fautes_droite_plus.clicked.connect(lambda :self._proxy_score_faute('faute', '+', "droite"))
        self.fautes_droite_moins.clicked.connect(lambda :self._proxy_score_faute('faute', '-', "droite"))
        fautes_layout.addWidget(self.fautes_gauche_label, 0, 0, 2, 1)
        fautes_layout.addWidget(self.fautes_gauche_plus, 0, 1, 1, 3)
        fautes_layout.addWidget(self.fautes_gauche_moins, 1, 1, 1, 3)
        fautes_layout.addWidget(self.fautes_droite_moins, 1, 5, 1, 3)
        fautes_layout.addWidget(self.fautes_droite_plus, 0, 5, 1, 3)
        fautes_layout.addWidget(self.fautes_droite_label, 0, 8, 2, 1)
        fautes_group.setLayout(fautes_layout)

        partie_droite_layout.addWidget(score_group)
        partie_droite_layout.addWidget(fautes_group)
        partie_droite_widget.setLayout(partie_droite_layout)
        return improTab_splitter

    def _init_tab_spectacle(self):
        # Porte son update lui meme car plus simple que pour impro
        # Tab pour les inputs du spectacle
        spectacleTab_layout = QVBoxLayout()
        
        #Ligne du titre du spectacle
        titre_spectacle_ligne = QWidget()
        titre_spectacle_ligne_layout = QHBoxLayout()
        self.qlabel_titre_spectacle = QLabel("Titre du spectacle : ")
        self.qlineedit_titre_spectacle = QLineEdit()
        self.qlineedit_titre_spectacle.setMaxLength(20)
        self.qlineedit_titre_spectacle.setPlaceholderText("Entrez un titre de spectacle")
        titre_spectacle_ligne_layout.addWidget(self.qlabel_titre_spectacle)
        titre_spectacle_ligne_layout.addWidget(self.qlineedit_titre_spectacle)
        titre_spectacle_ligne.setLayout(titre_spectacle_ligne_layout)
        spectacleTab_layout.addWidget(titre_spectacle_ligne)

        # Layout des équipes
        equipes = QWidget()
        equipes_layout = QHBoxLayout()
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        equipe_gauche_colonne = QWidget()
        equipe_gauche_colonne.setSizePolicy(size_policy)
        equipe_gauche_colonne_layout = QVBoxLayout()
        equipe_droite_colonne = QWidget()
        equipe_droite_colonne.setSizePolicy(size_policy)
        equipe_droite_colonne_layout = QVBoxLayout()
        
        # Noms des équipes
        equipe_gauche_nom = QWidget()
        equipe_gauche_nom_layout = QVBoxLayout()

        equipe_gauche_nom_ligne_nom = QWidget()
        equipe_gauche_nom_ligne_nom_layout = QHBoxLayout()
        self.qlabel_nom_equipeGauche = QLabel("Équipe à gauche :")
        equipe_gauche_nom_ligne_nom_layout.addWidget(self.qlabel_nom_equipeGauche)
        self.qlineedit_nom_equipeGauche = QLineEdit()
        self.qlineedit_nom_equipeGauche.setMaxLength(120)
        self.qlineedit_nom_equipeGauche.setPlaceholderText("Entrez le nom de l'équipe à gauche")
        equipe_gauche_nom_ligne_nom_layout.addWidget(self.qlineedit_nom_equipeGauche, 1)
        equipe_gauche_nom_ligne_nom.setLayout(equipe_gauche_nom_ligne_nom_layout)
        equipe_gauche_nom_layout.addWidget(equipe_gauche_nom_ligne_nom)

        equipe_gauche_nom_ligne_checkbox = QWidget()
        equipe_gauche_nom_ligne_checkbox_layout = QHBoxLayout()
        self.checkbox_nom_equipeGauche = QCheckBox()
        self.qlineedit_nom_equipeGauche.editingFinished.connect(lambda:self.checkbox_nom_equipeGauche.setChecked(True))
        self.checkbox_nom_equipeGauche.setChecked(False)
        checkbox_nom_equipeGauche_label = QLabel("Afficher le nom de l'équipe")
        equipe_gauche_nom_ligne_checkbox_layout.addWidget(self.checkbox_nom_equipeGauche)
        equipe_gauche_nom_ligne_checkbox_layout.addWidget(checkbox_nom_equipeGauche_label, 1)
        equipe_gauche_nom_ligne_checkbox.setLayout(equipe_gauche_nom_ligne_checkbox_layout)
        equipe_gauche_nom_layout.addWidget(equipe_gauche_nom_ligne_checkbox)
        self.equipe_gauche_nom_colorpicker = ColorPicker("couleur du nom", QColor("black"))
        equipe_gauche_nom_layout.addWidget(self.equipe_gauche_nom_colorpicker)
        
        equipe_gauche_nom.setLayout(equipe_gauche_nom_layout)
        equipe_gauche_colonne_layout.addWidget(equipe_gauche_nom)

        equipe_droite_nom = QWidget()
        equipe_droite_nom_layout = QVBoxLayout()

        equipe_droite_nom_ligne_nom = QWidget()
        equipe_droite_nom_ligne_nom_layout = QHBoxLayout()
        self.qlabel_nom_equipeDroite = QLabel("Équipe à droite :")
        equipe_droite_nom_ligne_nom_layout.addWidget(self.qlabel_nom_equipeDroite)
        self.qlineedit_nom_equipeDroite = QLineEdit()
        self.qlineedit_nom_equipeDroite.setMaxLength(120)
        self.qlineedit_nom_equipeDroite.setPlaceholderText("Entrez le nom de l'équipe à droite")
        equipe_droite_nom_ligne_nom_layout.addWidget(self.qlineedit_nom_equipeDroite, 1)
        equipe_droite_nom_ligne_nom.setLayout(equipe_droite_nom_ligne_nom_layout)
        equipe_droite_nom_layout.addWidget(equipe_droite_nom_ligne_nom)

        equipe_droite_nom_ligne_checkbox = QWidget()
        equipe_droite_nom_ligne_checkbox_layout = QHBoxLayout()
        self.checkbox_nom_equipeDroite = QCheckBox()
        self.qlineedit_nom_equipeDroite.editingFinished.connect(lambda:self.checkbox_nom_equipeDroite.setChecked(True))
        self.checkbox_nom_equipeDroite.setChecked(False)
        checkbox_nom_equipeDroite_label = QLabel("Afficher le nom de l'équipe")
        equipe_droite_nom_ligne_checkbox_layout.addWidget(self.checkbox_nom_equipeDroite)
        equipe_droite_nom_ligne_checkbox_layout.addWidget(checkbox_nom_equipeDroite_label, 1)
        equipe_droite_nom_ligne_checkbox.setLayout(equipe_droite_nom_ligne_checkbox_layout)
        equipe_droite_nom_layout.addWidget(equipe_droite_nom_ligne_checkbox)
        self.equipe_droite_nom_colorpicker = ColorPicker("couleur du nom", QColor("black"))
        equipe_droite_nom_layout.addWidget(self.equipe_droite_nom_colorpicker)
        
        equipe_droite_nom.setLayout(equipe_droite_nom_layout)
        equipe_droite_colonne_layout.addWidget(equipe_droite_nom)

        # Logo équipe
        self.image_equipeGauche = ImageSelector("Logo")
        equipe_gauche_colonne_layout.addWidget(self.image_equipeGauche, 1)
        self.image_equipeDroite = ImageSelector("Logo")
        equipe_droite_colonne_layout.addWidget(self.image_equipeDroite, 1)

        # Couleur de maillot
        self.maillot_equipeGauche = ColorPicker_group("couleur de maillot")
        equipe_gauche_colonne_layout.addWidget(self.maillot_equipeGauche)
        self.maillot_equipeDroite = ColorPicker_group("couleur de maillot")
        equipe_droite_colonne_layout.addWidget(self.maillot_equipeDroite)

        # Couleur de carton
        self.carton_equipeGauche = ColorPicker_group("couleur de carton")
        equipe_gauche_colonne_layout.addWidget(self.carton_equipeGauche)
        self.carton_equipeDroite = ColorPicker_group("couleur de carton")
        equipe_droite_colonne_layout.addWidget(self.carton_equipeDroite)

        equipe_gauche_colonne.setLayout(equipe_gauche_colonne_layout)
        equipe_droite_colonne.setLayout(equipe_droite_colonne_layout)
        equipes_layout.addWidget(equipe_gauche_colonne, 1)
        equipes_layout.addWidget(equipe_droite_colonne, 1)
        equipes.setLayout(equipes_layout)
        spectacleTab_layout.addWidget(equipes, 1)

        # Bouton Appliquer
        self.update_spectacle_button = QPushButton("Appliquer")
        spectacleTab_layout.addWidget(self.update_spectacle_button, 0)
        self.update_spectacle_button.clicked.connect(
            lambda: self.affichage.update_spectacle(
                {
                    "titre_spectacle":self.qlineedit_titre_spectacle.text(),
                    
                    'equipeGauche_nomAffiche': self.checkbox_nom_equipeGauche.isChecked(),
                    'equipeGauche_nom': self.qlineedit_nom_equipeGauche.text(),
                    'equipeGauche_nomCouleur': self.equipe_gauche_nom_colorpicker.chosen_color,
                    'equipeGauche_maillotAffiche': self.maillot_equipeGauche.checkbox_checkbox.isChecked(),
                    'equipeGauche_couleurMaillot': self.maillot_equipeGauche.chosen_color,
                    'equipeGauche_cartonAffiche': self.carton_equipeGauche.checkbox_checkbox.isChecked(),
                    'equipeGauche_couleurCarton': self.carton_equipeGauche.chosen_color,
                    'equipeGauche_logo_file_path': self.image_equipeGauche.file_path,
                    'equipeGauche_logoAffiche': self.image_equipeGauche.checkbox_checkbox.isChecked(),
                    
                    'equipeDroite_nomAffiche': self.checkbox_nom_equipeDroite.isChecked(),
                    'equipeDroite_nom': self.qlineedit_nom_equipeDroite.text(),
                    'equipeDroite_nomCouleur': self.equipe_droite_nom_colorpicker.chosen_color,
                    'equipeDroite_maillotAffiche': self.maillot_equipeDroite.checkbox_checkbox.isChecked(),
                    'equipeDroite_couleurMaillot': self.maillot_equipeDroite.chosen_color,
                    'equipeDroite_cartonAffiche': self.carton_equipeDroite.checkbox_checkbox.isChecked(),
                    'equipeDroite_couleurCarton': self.carton_equipeDroite.chosen_color,
                    'equipeDroite_logo_file_path': self.image_equipeDroite.file_path,
                    'equipeDroite_logoAffiche': self.image_equipeDroite.checkbox_checkbox.isChecked(),
                }
            )
        )   

        # 2do Bouton Clear

        spectacleTab = QWidget()
        spectacleTab.setLayout(spectacleTab_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(spectacleTab)
        
        return scroll_area
        
    def _init_tab_periode(self):
        ''' Tab pour les inputs de la période '''
        periodeTab_splitter = QSplitter(Qt.Vertical)
        periode_infos_group = QGroupBox("Période", periodeTab_splitter)
        periode_infos_group_layout = QGridLayout()
        nombre_de_colonne_de_la_grille = 6

        self.qlabel_nomPeriode = QLabel("Inititulé de la période : ")
        self.qlineedit_nomPeriode = QLineEdit()
        self.qlineedit_nomPeriode.setMaxLength(20)
        self.qlineedit_nomPeriode.setPlaceholderText("Entrée un intitulé pour cette partie du spectacle")
        periode_infos_group_layout.addWidget(self.qlabel_nomPeriode, 0, 0, 1, nombre_de_colonne_de_la_grille/3)
        periode_infos_group_layout.addWidget(self.qlineedit_nomPeriode, 0, nombre_de_colonne_de_la_grille/3, 1, 2*nombre_de_colonne_de_la_grille/3)
        self.qlabel_dureePeriode = QLabel("Durée de la période : ")
        self.qlineedit_dureePeriode = QLineEdit()
        self.qlineedit_dureePeriode.setMaxLength(120)
        self.qlineedit_dureePeriode.setPlaceholderText("Entrez une durée pour cette partie du spectacle")
        periode_infos_group_layout.addWidget(self.qlabel_dureePeriode, 1, 0, 1, nombre_de_colonne_de_la_grille/3)
        periode_infos_group_layout.addWidget(self.qlineedit_dureePeriode, 1, nombre_de_colonne_de_la_grille/3, 1, 2*nombre_de_colonne_de_la_grille/3)

        self.update_periode_button = QPushButton("Afficher sur la fenêtre publique")
        periode_infos_group_layout.addWidget(self.update_periode_button, 2, 0, 1, 2*nombre_de_colonne_de_la_grille/3)
        self.update_periode_button.clicked.connect(
            lambda: self.affichage.update_periode(
                {
                    "nomPeriode":self.qlineedit_nomPeriode.text(),
                    "dureePeriode":self.qlineedit_dureePeriode.text(),
                }
            )
        ) 
        self.clear_periode_button = QPushButton("Effacer")
        periode_infos_group_layout.addWidget(self.clear_periode_button, 2, 2*nombre_de_colonne_de_la_grille/3, 1, nombre_de_colonne_de_la_grille/3)
        self.clear_periode_button.clicked.connect(self.clear_periode_cote_controle)
        periode_infos_group.setLayout(periode_infos_group_layout)

        moments_affiches_group = QGroupBox("Mode d'affichage de la fenêtre publique", periodeTab_splitter)
        moments_affiches_group_layout = QHBoxLayout()
        self.hymne_button = QPushButton("Passer la fenêtre publique en mode hymne")
        self.hymne_button.clicked.connect(self.affichage.afficher_Hymne)
        moments_affiches_group_layout.addWidget(self.hymne_button)
        self.entracte_button = QPushButton("Passer la fenêtre publique en mode entracte")
        self.entracte_button.clicked.connect(self.affichage.afficher_Entracte)
        moments_affiches_group_layout.addWidget(self.entracte_button)
        self.mode_impro_button_depuis_periode = QPushButton("Passer la fenêtre publique en mode annonce de thème")
        self.mode_impro_button_depuis_periode.clicked.connect(self.affichage.afficher_Carton)
        moments_affiches_group_layout.addWidget(self.mode_impro_button_depuis_periode)
        moments_affiches_group.setLayout(moments_affiches_group_layout)

        return periodeTab_splitter

    def _init_tab_parametres(self):
        # Tab pour les paramètres
        parametresTab_layout = QVBoxLayout()
        palette_arbitraire = ["#74a498","#bde9e0","#f2f4ea","#e6dbc2","#b193b2"]
        # ["#e8c39e", "#f5e1ce"]
        
        # Résolution
        parametresTab_resolution_group = QGroupBox("Résolution")
        parametresTab_resolution_layout = QHBoxLayout()
        # Checkbox fullscreen
        parametresTab_resolution_layout.addWidget(QLabel("Affichage plein écran :"))
        self.checkbox_plein_ecran = QCheckBox()
        self.checkbox_plein_ecran.setChecked(False)
        self.checkbox_plein_ecran.stateChanged.connect(lambda:self._toggle_fullscreen(self.checkbox_plein_ecran.isChecked()))
        parametresTab_resolution_layout.addWidget(self.checkbox_plein_ecran)
        # Combobox de résolutions usuelles
        self.combobox_resolution = QComboBox()
        resolutions = [
            "800x600", "864x486", "960x540", "960x600", "1024x576", "1024x768", "1152x864", "1280x720", "1280x800", "1280x960", \
                "1368x768", "1400x1050",  "1440x900", "1600x900", "1600x1200", "1680x1050", "1920x1080", "1920x1200", "2560x1440", "2560x1600", "3840x2160", "5120x2880"]
        self.combobox_resolution.addItems(resolutions)
        self.combobox_resolution.currentTextChanged.connect(self._update_resolution)
        parametresTab_resolution_layout.addWidget(self.combobox_resolution)
        # Saisie manuelle
        parametresTab_resolution_layout.addWidget(QLabel("Ou saisissez une résolution manuellement : "))
        self.qlineedit_resolution_manuelle = QLineEdit()
        self.qlineedit_resolution_manuelle.setMaxLength(12)
        self.qlineedit_resolution_manuelle.setPlaceholderText("Entrez une résolution ....x....")
        parametresTab_resolution_layout.addWidget(self.qlineedit_resolution_manuelle)
        # Boutton ok
        self.button_resolution_manuelle = QPushButton("OK")
        self.button_resolution_manuelle.clicked.connect(lambda:self._update_resolution(self.qlineedit_resolution_manuelle.text()))
        parametresTab_resolution_layout.addWidget(self.button_resolution_manuelle)
        parametresTab_resolution_group.setLayout(parametresTab_resolution_layout)
        parametresTab_resolution_group.setStyleSheet("QGroupBox { background-color: "+ f"{palette_arbitraire[2]}" + "; border: 1px solid gray; }")
        parametresTab_layout.addWidget(parametresTab_resolution_group)

        # Arrière-plan
        parametresTab_arriereplan_group = QGroupBox("Arrière-plan")
        arriereplan_group_layout = QVBoxLayout()
        arriereplan_image_ou_couleur_ligne = QWidget()
        arriereplan_image_ou_couleur_ligne_layout = QHBoxLayout()
        self.couleur_fond = ColorPicker_group("couleur de fond")
        self.couleur_fond.setStyleSheet(f"background-color: {palette_arbitraire[1]};")
        self.image_de_fond = ImageSelector("Image de fond")
        self.image_de_fond.setStyleSheet(f"background-color: {palette_arbitraire[0]};")
        # peut-être des options à ajouter
        arriereplan_image_ou_couleur_ligne_layout.addWidget(self.couleur_fond)
        arriereplan_image_ou_couleur_ligne_layout.addWidget(self.image_de_fond)
        arriereplan_image_ou_couleur_ligne.setLayout(arriereplan_image_ou_couleur_ligne_layout)
        arriereplan_group_layout.addWidget(arriereplan_image_ou_couleur_ligne)
        # Bouton Appliquer
        self.update_arriereplan = QPushButton("Appliquer")
        arriereplan_group_layout.addWidget(self.update_arriereplan, 0)
        self.update_arriereplan.clicked.connect(
            lambda: self.affichage.update_arriere_plan(
                {
                    "couleur_de_fond": self.couleur_fond.chosen_color,
                    "couleur_de_fond_affiche": self.couleur_fond.checkbox_checkbox.isChecked(),
                    "image_de_fond": QPixmap(self.image_de_fond.file_path),
                    "image_de_fond_affiche": self.image_de_fond.checkbox_checkbox.isChecked()
                }
            )
        )
        parametresTab_arriereplan_group.setStyleSheet("QGroupBox { background-color: "+ f"{palette_arbitraire[2]}" + ";}")
        parametresTab_arriereplan_group.setLayout(arriereplan_group_layout)
        parametresTab_layout.addWidget(parametresTab_arriereplan_group)
        
        # Couleurs Horloge
        parametresTab_couleurs_horloge__group = QGroupBox("Chrono impro")
        parametresTab_couleurs_horloge_layout = QVBoxLayout()
        parametresTab_couleurs_horloge_line = QWidget()
        parametresTab_couleurs_horloge_line_layout = QHBoxLayout()
        self.couleur_temps_initial = ColorPicker("couleur initiale de l'horloge", QColor("yellow"))
        parametresTab_couleurs_horloge_line_layout.addWidget(self.couleur_temps_initial)
        self.couleur_temps_écoulé = ColorPicker("couleur de l'horloge lorsque le temps est écoulé", QColor("red"))
        parametresTab_couleurs_horloge_line_layout.addWidget(self.couleur_temps_écoulé)
        parametresTab_couleurs_horloge_line.setLayout(parametresTab_couleurs_horloge_line_layout)
        parametresTab_couleurs_horloge_layout.addWidget(parametresTab_couleurs_horloge_line)
        # Bouton Appliquer
        self.update_couleurs_horloge = QPushButton("Appliquer")
        parametresTab_couleurs_horloge_layout.addWidget(self.update_couleurs_horloge, 0)
        self.update_couleurs_horloge.clicked.connect(
            lambda: self.affichage.update_couleurs_horloge(
                {
                    "couleur_temps_initial": self.couleur_temps_initial.chosen_color,
                    "couleur_temps_écoulé": self.couleur_temps_écoulé.chosen_color,
                }
            )
        )
        parametresTab_couleurs_horloge__group.setLayout(parametresTab_couleurs_horloge_layout)
        parametresTab_couleurs_horloge__group.setStyleSheet("QGroupBox { background-color: "+ f"{palette_arbitraire[3]}" + "; border: 1px solid gray; }")
        parametresTab_layout.addWidget(parametresTab_couleurs_horloge__group)

        # Couleurs Score
        self.couleur_score = ColorPickerAvecAppliquer_group("couleur derrière le score")
        self.couleur_score.setStyleSheet("QGroupBox { background-color: "+ f"{palette_arbitraire[2]}" + ";}")
        self.couleur_score.appliquer.clicked.connect(
            lambda: self.affichage.update_couleur_score(
                {
                    "couleur_ellipse_score": self.couleur_score.chosen_color,
                    "afficher_couleur_ellipse_score": self.couleur_score.checkbox_checkbox.isChecked(),
                }
            )
        )
        parametresTab_layout.addWidget(self.couleur_score)




        # 2do Image de fond
        # 2do Save/Load paramètres
        # 2do Comportement des chronos : est-ce qu'on continue en négatif jusqu'au "stop chrono" ou est-ce qu'on s'arrête à zéro ?
        
        # self.qlineedit_nomparametres = QLineEdit()
        # self.qlineedit_nomparametres.setMaxLength(20)
        # self.qlineedit_nomparametres.setPlaceholderText("Entrée un intitulé pour cette partie du spectacle")
        
        # parametresTab_layout.addWidget(self.qlineedit_nomparametres, 0, 1)
        # self.qlabel_dureeparametres = QLabel("Durée de la période : ")
        # self.qlineedit_dureeparametres = QLineEdit()
        # self.qlineedit_dureeparametres.setMaxLength(120)
        # self.qlineedit_dureeparametres.setPlaceholderText("Entrez une durée pour cette partie du spectacle")
        # parametresTab_layout.addWidget(self.qlabel_dureeparametres, 1, 0)
        # parametresTab_layout.addWidget(self.qlineedit_dureeparametres, 1, 1)
        # self.update_parametres_button = QPushButton("Mettre à jour cet onglet")
        # parametresTab_layout.addWidget(self.update_parametres_button, 2, 0, 1, 2)
        # self.update_parametres_button.clicked.connect(
        #     lambda: self.affichage.update_parametres(
        #         {
        #             "nomparametres":self.qlineedit_nomparametres.text(),
        #             "dureeparametres":self.qlineedit_dureeparametres.text(),
        #         }
        #     )
        # )   
        # # raz_button = QPushButton("Remise à zéro de tous les champs de l'impro (cet onglet)")
        # # parametresTab_layout.addWidget(raz_button, n, 0, 1, 2)
        parametresTab = QWidget()
        parametresTab.setLayout(parametresTab_layout)
        return parametresTab

    def clear_impro_cote_controle(self):
            self.temps_impro_controle.endTimer()
            self.temps_impro_controle.start.setEnabled(False)
            self.temps_impro_controle.stop.setEnabled(False)
            self.affichage.clear_impro_cote_affichage()

    def update_impro_cote_controle(self):
        # nature
        if self.mixte_button.isChecked():
            nature = "Improvisation mixte"
        elif self.comparee_button.isChecked():
            nature = "Improvisation comparée"
        else:
            nature = self.naturePersonnalisable_radio_lineedit.qlineedit.text()

        if self.illimite_button.isChecked():
            nombreDeJoueurs = "Nombre de joueurs illimté"
        elif self.joueurs_radio_combobox.radio.isChecked():
            nombreDeJoueurs = self.joueurs_radio_combobox.combobox.currentText()
        else:
            nombreDeJoueurs = self.nombreDeJoueurs_radio_lineedit.qlineedit.text()

        temps_a_chronometrer_t = self.temps_impro_controle.temps_a_chronometrer_input.time()
        self.temps_impro_controle.temps_qui_reste_en_secondes = QTime_perso.en_secondes(temps_a_chronometrer_t)
        self.temps_impro_controle.start.setEnabled(True)
        self.temps_impro_controle.stop.setEnabled(False)

        theme = self.qlineedit_theme.text()
        categorie = self.qlineedit_categorie.text()

        self.affichage.update_impro_cote_affichage(
                {
                    "nature":nature,
                    "theme":theme,
                    "categorie":categorie,
                    "nombreDeJoueurs":nombreDeJoueurs,
                    "duree_t":temps_a_chronometrer_t,
                }
        )

    def _proxy_score_faute(self, nature, signe, lateralite):
        if nature == "score":
            if lateralite == "gauche":
                if signe == '+':
                    self.score_gauche = self.score_gauche+1
                if signe == '-':
                    if self.score_gauche > 0:
                        self.score_gauche = self.score_gauche-1
                self.affichage.score_gauche.score = self.score_gauche
                self.score_gauche_label.setText(str(self.score_gauche))
                self.affichage.score_gauche.label.setText(str(self.score_gauche))
            if lateralite == "droite":
                if signe == '+':
                    self.score_droit = self.score_droit+1
                if signe == '-':
                    if self.score_droit > 0:
                        self.score_droit = self.score_droit-1
                self.affichage.score_droit.score = self.score_droit
                self.score_droit_label.setText(str(self.score_droit))
                self.affichage.score_droit.label.setText(str(self.score_droit))
                # self.affichage.score_droit.update()
        if nature == "faute":
            if lateralite == "gauche":
                if signe == '+':
                    self.fautes_gauche_nombre_de_clics = self.fautes_gauche_nombre_de_clics+1
                    self.affichage.fautes_gauche.ajouter_un_clic_faute()
                if signe == '-':
                    if self.fautes_gauche_nombre_de_clics > 0:
                        self.fautes_gauche_nombre_de_clics = self.fautes_gauche_nombre_de_clics-1
                    self.affichage.fautes_gauche.retirer_un_clic_faute()
                self.fautes_gauche_label.setText(str(_Fautes.convertir_clics_en_fautes(self.fautes_gauche_nombre_de_clics)))
            if lateralite == "droite":
                if signe == '+':
                    self.fautes_droite_nombre_de_clics = self.fautes_droite_nombre_de_clics+1
                    self.affichage.fautes_droite.ajouter_un_clic_faute()
                if signe == '-':
                    if self.fautes_droite_nombre_de_clics > 0:
                        self.fautes_droite_nombre_de_clics = self.fautes_droite_nombre_de_clics-1
                    self.affichage.fautes_droite.retirer_un_clic_faute()
                self.fautes_droite_label.setText(str(_Fautes.convertir_clics_en_fautes(self.fautes_droite_nombre_de_clics)))

    def clear_periode_cote_controle(self):
            self.affichage.clear_periode_cote_affichage()

    def closeEvent(self, event: QCloseEvent) -> None:
        '''Appelé lorsqu'on ferme la fenêtre. Ferme celle-ci avec la fenêtre de contrôle.'''
        if DEBUG == True:
            self.affichage = None
            event.accept()
        else:
            reply = QMessageBox.question(self, self.windowTitle(),
                                            "Êtes-vous sûr de vouloir fermer " + NOM_APPLI + " ?",
                                            QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.affichage = None
                event.accept()
            else:
                event.ignore()

    def _update_resolution(self, resolution):
        try:
            largeur_hauteur = resolution.split('x')
            self.affichage.resize(int(largeur_hauteur[0]), int(largeur_hauteur[1]))
            self.affichage.update()
        except:
            print("Erreur dans la modification de la résolution")

    def _toggle_fullscreen(self, checked):
        if checked:
            self.derniere_valeur_largeur_affichage = self.affichage.width()
            self.derniere_valeur_hauteur_affichage = self.affichage.height()
            self.affichage.setWindowState(Qt.WindowFullScreen)
        else:
            self.affichage.setWindowState(Qt.WindowNoState)
            self.affichage.resize(self.derniere_valeur_largeur_affichage, self.derniere_valeur_hauteur_affichage)

    def paintEvent(self, e):
        'recalcule l unite_taille_affichage au besoin'
        largeur = self.width()
        # on recalcule self.unite_taille_affichage par la largeur (on ignore la hauteur). Car largeur ce sont de plus gros nombres
        self.unite_taille_affichage = largeur/self.largeur_fenetre_unitaire
        super().paintEvent(e)


app = QApplication(sys.argv)

prog_dir = Path(__file__).parent

# Fonts : pour qu'ils soient accessibles partout
Komika_Title_path = str(prog_dir) + "/fonts/KOMTITK_.ttf"
Komika_Title_font_id = QFontDatabase.addApplicationFont(Komika_Title_path)
Komika_Title_font_family = QFontDatabase.applicationFontFamilies(Komika_Title_font_id)
font_Komika = Komika_Title_font_family[0]
TechnaSans_path = str(prog_dir) + "/fonts/TechnaSans-Regular.otf"
TechnaSans_font_id = QFontDatabase.addApplicationFont(TechnaSans_path)
TechnaSans_font_family = QFontDatabase.applicationFontFamilies(TechnaSans_font_id)
font_TechnaSans = TechnaSans_font_family[0]
dita_sweet_path = str(prog_dir) + "/fonts/Dita-Sweet.otf"
dita_sweet_font_id = QFontDatabase.addApplicationFont(dita_sweet_path)
dita_sweet_font_family = QFontDatabase.applicationFontFamilies(dita_sweet_font_id)
font_Dita = dita_sweet_font_family[0]
mikodacs_path = str(prog_dir) + "/fonts/Mikodacs.otf"
mikodacs_font_id = QFontDatabase.addApplicationFont(mikodacs_path)
mikodacs_font_family = QFontDatabase.applicationFontFamilies(mikodacs_font_id)
font_mikodacs = mikodacs_font_family[0]
liberation_path = str(prog_dir) + "/fonts/LiberationSerif-Regular.ttf"
liberation_font_id = QFontDatabase.addApplicationFont(liberation_path)
liberation_font_family = QFontDatabase.applicationFontFamilies(liberation_font_id)
font_liberation = liberation_font_family[0]

fonts = {
    "komika" : font_Komika,
    "technasans" : font_TechnaSans,
    "dita" : font_Dita,
    "mikodacs" : font_mikodacs,
    "liberation" : font_liberation
}
window = ControleAffichage(fonts)
window.setWindowFlag(Qt.Window)
window.show()

app.exec()