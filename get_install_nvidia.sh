#!/bin/bash

# Verzeichnis, in dem der Treiber gespeichert wird
DOWNLOAD_DIR="$HOME/Downloads"

# Neueste Treiberversion (bitte bei Bedarf anpassen)
LATEST_VERSION="550.142"

# Download-URL basierend auf der Treiberversion
NVIDIA_URL="https://us.download.nvidia.com/XFree86/Linux-x86_64/${LATEST_VERSION}/NVIDIA-Linux-x86_64-${LATEST_VERSION}.run"

# Erstellen des Download-Verzeichnisses, falls nicht vorhanden
mkdir -p "$DOWNLOAD_DIR"

# Zielpfad der heruntergeladenen Datei
TARGET_FILE="$DOWNLOAD_DIR/NVIDIA-Linux-x86_64-${LATEST_VERSION}.run"

# Herunterladen des Treibers
echo "Lade NVIDIA-Treiber Version $LATEST_VERSION herunter ..."
wget -O "$TARGET_FILE" "$NVIDIA_URL"

if [ $? -eq 0 ]; then
    echo "Download abgeschlossen. Datei gespeichert in: $TARGET_FILE"
    
    # Datei ausführbar machen
    chmod +x "$TARGET_FILE"
    echo "Die Datei wurde ausführbar gemacht."
    
    # Wechseln des Runlevels auf 3 (Multi-User ohne GUI)
    echo "Wechsel in Runlevel 3 (Multi-User ohne GUI)..."
    sudo init 3
    
    if [ $? -eq 0 ]; then
        # Starten der Installation im Runlevel 3
        echo "Starte die NVIDIA-Treiberinstallation..."
        sudo "$TARGET_FILE"
        
        if [ $? -eq 0 ]; then
            echo "Die NVIDIA-Treiberinstallation wurde erfolgreich abgeschlossen."
        else
            echo "Fehler bei der Treiberinstallation."
        fi
    else
        echo "Fehler: Konnte nicht in Runlevel 3 wechseln."
    fi
else
    echo "Fehler: Download fehlgeschlagen."
    exit 1
fi
