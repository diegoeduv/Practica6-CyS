# Practica 6 - Keylogger

## Descripción

En esta práctica, se implementará un keylogger utilizando la biblioteca `pynput` para capturar eventos del teclado. El keylogger registrará las teclas presionadas y enviará el registro por correo electrónico a intervalos regulares. Además, se proporcionará un script de limpieza para eliminar cualquier rastro del keylogger después de su uso.

---

## Requisitos

Instalar la biblioteca `pynput` para capturar eventos del teclado:
```bash
pip install pynput
```

---

## Ejecución

Crear ambiente virtual (opcional pero recomendado):
```bash
python3 -m venv venv
source venv/bin/activate  
```

Ejecución del keylogger:
sudo .venv/bin/python keylogger.py

Eliminar el rastro: 
sudo ./Cleanup.sh