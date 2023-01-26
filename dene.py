import requests

def dosyaIndrime(url=str,name=str):
    # Url Raw olarak gerekli
    response = requests.get(url)

    if response.status_code == 200:
        open("./duygularım/"+name, "wb").write(response.content)
        print("Dosya indirildi.")
    else:
        print("Url Hatası Mevcut:", response.status_code)


def versionKontrol():
    version = 2.0

    response = requests.get("https://raw.githubusercontent.com/bedelcemaxim/XSfdEtApBgJtpy/main/version.json")
    data = response.json()
    newVersion = data['version']

    if version == newVersion:
        print('Güncel Version: ',version)
        return True
    else:
        print("Sürümünüz güncel değil.")
        return False

versionKontrol()
