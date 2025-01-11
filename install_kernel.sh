#!/bin/bash

# Funktion zum Abrufen der Architektur des Systems
get_architecture() {
    dpkg --print-architecture
}

# Funktion zum Aktualisieren der Paketliste für die Backports
update_package_list() {
    sudo apt-get update -t bookworm-backports
}

# Funktion zum Suchen der neuesten Kernelversionen im Backports-Repository
get_backports_kernels() {
    local arch="$1"
    apt-cache -t bookworm-backports search '^linux-image-[0-9]' | grep "bpo-${arch}" | grep -v 'dbg' | awk '{print $1}'
}

# Funktion zum Installieren eines ausgewählten Kernels
install_kernel() {
    local kernel_package="$1"
    sudo apt-get install -t bookworm-backports "$kernel_package"
}

# Hauptfunktion
main() {
    local arch=$(get_architecture)
    echo "Aktuelle Architektur: $arch"

    update_package_list

    local kernels=($(get_backports_kernels "$arch"))

    if [ ${#kernels[@]} -eq 0 ]; then
        echo "Keine Kernel-Versionen im Backports-Repository gefunden."
        exit 1
    fi
    clear
    echo "Verfügbare Kernel-Versionen (unsigned = kein signierter Bootloader = kein Secureboot!:"
    for ((i=0; i<${#kernels[@]}; i++)); do
        echo "$i: ${kernels[$i]}"
    done

    read -p "Bitte wählen Sie die Nummer des zu installierenden Kernels (9 zum Beenden): " choice

    if [ "$choice" -eq 9 ]; then
        echo "Abbruch."
        exit 0
    fi

    if (( choice >= 0 && choice < ${#kernels[@]} )); then
        selected_kernel="${kernels[$choice]}"
        echo "Ausgewählter Kernel: $selected_kernel"
        install_kernel "$selected_kernel"
    else
        echo "Ungültige Auswahl."
        exit 1
    fi
}

# Aufruf der Hauptfunktion
main
