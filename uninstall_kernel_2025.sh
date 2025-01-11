#!/bin/bash
# Funktion zum Abrufen der installierten Kernelversionen
get_installed_kernels() {
    dpkg -l | grep '^ii' | grep linux-image | awk '{print $2}' | grep -v 'dbg' | sort -Vr | head -n 3
}

# Funktion zum Deinstallieren eines ausgewählten Kernels
uninstall_kernel() {
    local kernel_package="$1"
    sudo apt-get remove "$kernel_package"
}

# Hauptfunktion
main() {
    clear
    local installed_kernels=($(get_installed_kernels))

    if [ ${#installed_kernels[@]} -eq 0 ]; then
        echo "Keine installierten Kernelversionen gefunden."
        exit 1
    fi

    echo "Aktiver Kernel (NICHT DEINSTALLIEREN!):" && uname -r
    echo ""
    echo "Aktuell installierte Kernelversionen:"
    for ((i=0; i<${#installed_kernels[@]}; i++)); do
        echo "$i: ${installed_kernels[$i]}"
    done

    while true; do
        read -p "Bitte wählen Sie die Nummer des zu deinstallierenden Kernels (x oder X zum Beenden): " choice

        if [[ "$choice" == [xX] ]]; then
            echo "Abbruch."
            exit 0
        elif (( choice >= 0 && choice < ${#installed_kernels[@]} )); then
            selected_kernel="${installed_kernels[$choice]}"
            echo "Ausgewählter Kernel zum Deinstallieren: $selected_kernel"
            uninstall_kernel "$selected_kernel"
            break
        else
            echo "Ungültige Auswahl. Bitte wählen Sie eine gültige Nummer oder x/X zum Beenden."
        fi
    done
}

# Aufruf der Hauptfunktion
main
