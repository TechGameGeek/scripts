#!/usr/bin/env python3
import sys
import subprocess
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QInputDialog, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TGG-Debian-Setup-Assistent")
        self.setMinimumSize(800, 300)  # Setze eine minimale Größe für das Fenster

        # Zentrales Widget und horizontales Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Rand auf 0 setzen

        # Vertikales Layout für die linke Spalte
        left_layout = QVBoxLayout()

        # Überschrift für die linke Spalte
        left_label = QLabel("W A R T U N G")
        left_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(left_label)

        # Buttons für die linke Spalte hinzufügen
        left_button_info = [
            ("Wichtige Informationen", "okular ~/Dokumente/Debianultimate_202405_1.pdf"),
            ("Neues Kernel installieren (Backports)", "sudo /usr/bin/install_kernel.sh"),
            ("Kernel deinstallieren", "sudo /usr/bin/uninstall_kernel.sh"),
            ("Bereinige nicht verwendete Pakete (apt-get autoremove)", "sudo apt-get autoremove && read -p 'Taste drücken...'"),
            ("Paketquellen aktualisieren (apt-get update)", "sudo apt-get update && read -p 'Taste drücken...'"),
            ("Pakete aktualisieren (apt-get update + upgrade)", "sudo apt-get update && sudo apt-get upgrade && read -p 'Taste drücken...'"),
            ("Paketcache leeren (apt-get clean)", "sudo apt-get clean && read -p 'Taste drücken...'")
        ]

        for text, command in left_button_info:
            button = QPushButton(text)
            button.setFixedHeight(30)  # Setze die Höhe der Buttons
            left_layout.addWidget(button)
            button.clicked.connect(lambda _, cmd=command: self.open_terminal(cmd))

        # Vertikales Layout für die rechte Spalte
        right_layout = QVBoxLayout()

        # Überschrift für die rechte Spalte
        right_label = QLabel("W E R K Z E U G E")
        right_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(right_label)

        # Button "Datensicherung einrichten" hinzufügen
        backup_button = QPushButton("Datensicherung einrichten (Snapshots)")
        backup_button.setFixedHeight(30)
        backup_button.clicked.connect(lambda: self.open_timeshift())
        right_layout.addWidget(backup_button)

        # Button "Optische Anpassung" hinzufügen
        styling_button = QPushButton("Systemeinstellungen")
        styling_button.setFixedHeight(30)
        styling_button.clicked.connect(lambda: self.open_plasma_styles())
        right_layout.addWidget(styling_button)

        # Button "Nachtfarbenverwaltung unter KDE starten" hinzufügen
        night_mode_button = QPushButton("Nachtfarbenverwaltung unter KDE starten")
        night_mode_button.setFixedHeight(30)
        night_mode_button.clicked.connect(lambda: self.start_night_mode())
        right_layout.addWidget(night_mode_button)

        # Button "Steam Installer starten" hinzufügen
        steam_button = QPushButton("Steam Installer starten")
        steam_button.setFixedHeight(30)
        steam_button.clicked.connect(lambda: self.start_steam_installer())
        right_layout.addWidget(steam_button)

        # Button "NVIDIA DETECT + INSTALL [BETA!]" hinzufügen
        nvidia_button = QPushButton("NVIDIA-DETECT")
        nvidia_button.setFixedHeight(30)
        nvidia_button.clicked.connect(lambda: self.nvidia_detect_install())
        right_layout.addWidget(nvidia_button)

        # Button "Grafikinfo" hinzufügen
        graphics_info_button = QPushButton("Grafikinfo")
        graphics_info_button.setFixedHeight(30)
        graphics_info_button.clicked.connect(lambda: self.display_graphics_info())
        right_layout.addWidget(graphics_info_button)

        # Button "Beenden" hinzufügen
        exit_button = QPushButton("Beenden")
        exit_button.setFixedHeight(30)
        exit_button.clicked.connect(lambda: self.close())
        right_layout.addWidget(exit_button)

        # Vertikale Layouts dem zentralen horizontalen Layout hinzufügen
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

    def open_terminal(self, command):
        try:
            subprocess.Popen(["konsole", "-e", "bash", "-c", command])
        except Exception as e:
            print("Fehler beim Öffnen des Terminals:", e)

    def open_timeshift(self):
        password, ok = self.get_password()
        if ok:
            try:
                subprocess.Popen(["sudo", "-S", "timeshift-gtk"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(input=(password + "\n").encode())
            except Exception as e:
                print("Fehler beim Öffnen von Timeshift:", e)

    def get_password(self):
        password, ok = QInputDialog.getText(self, "Passwort eingeben", "Bitte geben Sie Ihr Passwort ein:", QLineEdit.Password)
        if ok:
            return password, True
        return None, False

    def open_plasma_styles(self):
        try:
             subprocess.Popen(["systemsettings5", "appearance"])
        except Exception as e:
             print("Fehler beim Öffnen der Plasma-Stile:", e)

    def nvidia_detect_install(self):
        try:
            command = 'nvidia-detect && read -p "Taste drücken"'
            subprocess.Popen(["konsole", "-e", "bash", "-c", command])
        except Exception as e:
            print("Fehler bei der Ausführung von nvidia-detect:", e)

    def start_steam_installer(self):
        try:
            subprocess.Popen(["/usr/games/steam"])
        except Exception as e:
            print("Fehler beim Starten des Steam Installers:", e)

    def start_night_mode(self):
        try:
            subprocess.Popen(["systemsettings5", "kcm_nightcolor"])
        except Exception as e:
            print("Fehler beim Starten der Nachtfarbenverwaltung:", e)

    def display_graphics_info(self):
        try:
            subprocess.Popen(["konsole", "-e", "/usr/bin/vgainfo.sh"])
        except Exception as e:
            print("Fehler beim Öffnen des Terminalfensters für vgainfo.sh:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
