#!/bin/bash

# Funktion zum Anzeigen von Grafikkarteninformationen
display_gpu_info() {
    echo "Grafikkarteninformationen:"
    echo "---------------------------"
    lspci | grep -i vga
}

# Funktion zum Anzeigen des verwendeten Grafikkartenmoduls
display_gpu_module() {
    echo "Verwendetes Grafikkartenmodul:"
    echo "------------------------------"
    lspci -nnk | grep -i vga -A 2
}

# Hauptfunktion zum Aufrufen der anderen Funktionen
main() {
    display_gpu_info
    echo ""
    display_gpu_module
    read -p "Taste drücken"
}

# Aufrufen der Hauptfunktion
main
