import os.path
from random import shuffle
import sys
from urllib.parse import quote , unquote
import json
import base64
from colorama import Fore , Style
import time

dosya_adi = "veriler.json"
filename = "user.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
#nt (new technology) stands for Windows, and 'cls' is used to clear the terminal. In Linux or Macos, 'clear' is used for the same purpose.

def AddPassword(key,value):
    # Eğer dosya varsa, içindeki verileri oku (bu okuma ekrana yazdırmalık bir okuma değildir sadece bu python dosyasna veriyi çeker.)
    try:
        with open(dosya_adi, 'r') as file:
            my_dict = json.load(file)
            # daha önce oluşturulan dict dosyasını python dosyasına dahil eder.
    except FileNotFoundError:
        # Dosya bulunamazsa yeni bir dosya ve dictionary  oluştur.
        with open(dosya_adi, 'w') as new_file:
            new_file.write("{}")
            my_dict = {}

    key = Encoder(key)
    value = Encoder(value)
    my_dict[key] = value

    # Dictionary'yi JSON dosyasına yaz
    with open(dosya_adi, 'w') as file:
        json.dump(my_dict, file)

def randomsifre():
    #random sifre oluşturmak için
    sayidizisi = ["0","1","2","3","4","5","6","7","8","9"]
    lowecase = [chr(i) for i in range(ord('a'), ord('z')+1)]
    uppercase = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    punctuation = '!"#$%&()*+,-./:;<=>?@[]^_`{|}~'
    punc_list = list()
    for i in punctuation:
        punc_list.append(i)

    #butun listeleri birleştirme
    full_list = lowecase + uppercase + punc_list + sayidizisi
    shuffle(full_list)
    passlist = list()

    for i in range(14):
        a = full_list[i]
        passlist.append(a)

    password = ''.join(passlist)
    encoded_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    return encoded_password

def printthecontext():
    try:
        with open(dosya_adi, 'r') as file:
            my_dict = json.load(file)
            # burada bu dict sınıfının her bir elemanının decryption'ı gerçekleştirilmeli
            i = 1
            for key, value in my_dict.items():
                print(f"{i} | ",end="")
                print(Decoder(key) + " : " + Decoder(value))
                i += 1

    except FileNotFoundError:
        print(f"    No password found creating {dosya_adi}")
        # Dosyayı oluştur ve içine boş bir dictionary yaz
        with open(dosya_adi, 'w') as new_file:
            new_file.write("{}")

def reseter():
    #yok olup olmadığına bakmak için
    if os.path.exists(dosya_adi):
        with open(dosya_adi, "w")as dosya:
            dosya.write(json.dumps({}))
            print("     File Reseted")
    else:
        #burası yok olduğu durum , yok olduğu durumda oluşturmak gerekir
        with open(dosya_adi, "w") as dosya:
            dosya.write(json.dumps({}))
            #dosya oluşturuldu ve içine boş bir dict objesi eklendi
            print("     File Reseted")

def IsPassStrong(sifre):
    # sifre 4 karakterden kısaysa sifre gucsuz desin
    count = 0
    for sayi in "0123456789":
        if sayi in sifre:
            count += 1
    for sembol in '!"#$%&()*+,-./:;<=>?@[]^_`{|}~':
        for sembol in sifre:
            count += 1

    if len(sifre) <= 4:
        print(Fore.LIGHTMAGENTA_EX + "     Password is very weak! " + Style.RESET_ALL)
    elif len(sifre) < 8 and len(sifre) > 4:
        if count <= 2:
            print(Fore.LIGHTMAGENTA_EX + "     Password is weak! " + Style.RESET_ALL)
        if count > 2:
            print(Fore.LIGHTMAGENTA_EX + "     Password is mid! " + Style.RESET_ALL)
    elif len(sifre) >= 8:
        if count >= 5:
            print(Fore.LIGHTMAGENTA_EX + "     Password is alright! " + Style.RESET_ALL)
        if count < 5 and count > 3:
            print(Fore.LIGHTMAGENTA_EX + "     Password is well done!" + Style.RESET_ALL)
        if count <= 3:
            print(Fore.LIGHTMAGENTA_EX + "     Password is so well done!" + Style.RESET_ALL)

def Encoder(value):
    value = quote(value)
    value = value + "26"
    value = value[::-1]
    return value

def Decoder(value):
    value = value[::-1]
    value = value[:-2]
    value = unquote(value)
    return value

def Updater(key,value):
    #ilk dosyayı okuyup bir credentiallere bakması lazım
    try:
        with open(dosya_adi, 'r') as file:
            my_dict = json.load(file)
            # burada bu dict sınıfının her bir elemanının decryption'ı gerçekleştirilmeli
            key = Encoder(key)
            value = Encoder(value)
            if key in my_dict:
                my_dict[key] = value
                with open(dosya_adi, "w")as file:
                    json.dump(my_dict,file)
                    print(Fore.BLUE + "     File Updated " + Style.RESET_ALL)
            else:
                print(Fore.RED + "     No credential found" + Style.RESET_ALL)

    except FileNotFoundError:
        print(f"    No password found creating {file}")
        # Dosyayı oluştur ve içine boş bir dictionary yaz
        with open(dosya_adi, 'w') as new_file:
            new_file.write("{}")

    except json.JSONDecodeError as e:
        print(Fore.RED + f"     {dosya_adi} is inappropriate file !!" + Style.RESET_ALL)

def Remove(key):
    #ilk dosyayı okuyup bir credentiallere bakması lazım
    try:
        with open(dosya_adi, 'r') as file:
            my_dict = json.load(file)
            # burada bu dict sınıfının her bir elemanının decryption'ı gerçekleştirilmeli
            key = Encoder(key)
            if key in my_dict:
                del my_dict[key]
                print(Fore.CYAN + f"{Decoder(key)} credential removed" + Style.RESET_ALL)
                with open(dosya_adi, "w")as file:
                    json.dump(my_dict,file)
                    print(Fore.LIGHTMAGENTA_EX + "     Updated" + Style.RESET_ALL)
            else:
                print(Fore.RED + "     No credential found" + Style.RESET_ALL)

    except FileNotFoundError:
        print(f"    No password found creating {file}")
        # Dosyayı oluştur ve içine boş bir dictionary yaz
        with open(dosya_adi, 'w') as new_file:
            new_file.write("{}")

    except json.JSONDecodeError as e:
        print(Fore.RED + f"     {dosya_adi} is inappropriate file !!" + Style.RESET_ALL)

def check_file(filename):
    if not os.path.exists(filename):
        return 1
    else:
        with open(filename, 'r')as file:
            try:
                data = json.load(file)
                if not data or not isinstance(data, dict): # dosya varsa ve içindeki dict yoksa veya boşsa
                    return 2
                else: # dosya varsa ve içindeki dict doluysa
                    return 3
            except json.JSONDecodeError:
                return 2 #bir hata oluştu

def Settle(result):
    if result == 1:
        # dosya oluşturucaz ve içine boş bir dict ekleyecez
        with open(filename, 'w')as file:
            json.dump({}, file)
        return "not exist"
    elif result == 2:
        with open(filename, 'w')as file:
            json.dump({}, file)
        return "not exist"
    elif result == 3:
        return "already exist"

result = check_file(filename)

clear_screen()

if Settle(result) == 'not exist':
    # kullanıcı uyarılır ve ilk defa kullanıcıdan şifre alınır. iki kere. alınan şifreler dict in içine eklenir
    print(Fore.RED + "\n    !!!      Warning this password is your main password.    !!!\n    !!!  So don't forget & don't delete the user.json file   !!!\n" + Style.RESET_ALL)
    while True:
        sifre = input(Fore.LIGHTYELLOW_EX + "     Password : " + Style.RESET_ALL)
        dogrulama = input(Fore.LIGHTYELLOW_EX + "     Password again : " + Style.RESET_ALL)

        if len(sifre) < 5:
            print(Fore.RED + "     pass is too short !! \n" + Style.RESET_ALL)
        else:
            if sifre != dogrulama:
                print(Fore.RED + "     Passes aren't matching try again !!!\n" + Style.RESET_ALL)
            elif sifre == dogrulama:
                break

    with open(filename)as file:
        #ilk önce mevcut içeriği kontrol etmek gerekir.
        existing_data = json.load(file)

    existing_data["Password"] = Encoder(sifre)

    #güncellenmiş dict objesini dosyaya tekrar yazdırmak :
    with open(filename, 'w')as file:
        json.dump(existing_data, file)
    clear_screen()
    time.sleep(1)
    print(Fore.LIGHTYELLOW_EX + "Succesfull login" + Style.RESET_ALL)

elif Settle(result) == 'already exist':
    # kullanıcıdan zaten kayıtlı olan bir şifre kontrol edilir eğer eşleşiyosa program çalışır eşleşmezse tekrar sorulur.

    with open(filename, 'r')as file:
        existing_data2 = json.load(file)
        existing = existing_data2["Password"]
        existing = Decoder(existing)

    while True:
        sifre = input(Fore.LIGHTYELLOW_EX + "     Enter your main password : " + Style.RESET_ALL)
        if sifre == existing:
            clear_screen()
            time.sleep(1)
            print(Fore.LIGHTYELLOW_EX + "Succesfull login" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "     Password is wrong try again !!!\n" + Style.RESET_ALL)

isim = '''
_     _           
/ _  _ |    ,--.   ██████╗  █ █   /  ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗    \\   █ █
(  @  @ )   / ,-'  ██╔══██╗      |   ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗    |
 \\  _T_/-._( (     ██████╔╝     /    ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝     \\ 
 /         `. \\    ██╔═══╝      \\    ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██╔══██╗     /
|         _  \\ |   ██║           |   ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║    |
 \\ \\ ,  /      |   ╚═╝            \\  ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝    /
  || |-_\\__   /     ___________________________Created by Yiğit Durbak__________________________________
 ((_/`(____,-          
'''

def red_text(text):
    print(Fore.RED + text + Style.RESET_ALL)

for satir in isim.split('\n'):
    red_text(satir)

while True:

    print(Fore.CYAN + "   [1] Create Password   [2] Show passwords   [3] Reset Passwords\n   [4] My Pass strong?   [5] Update Password  [q] Quit\n" + Style.RESET_ALL)

    girdi = input(Fore.LIGHTGREEN_EX + "Choose one : " + Style.RESET_ALL)

    if girdi == '1':
        print("")
        print(Fore.LIGHTMAGENTA_EX + "     1- We set a password for you" + Style.RESET_ALL)
        print(Fore.LIGHTMAGENTA_EX + "     2- Set your own password" + Style.RESET_ALL)
        print("")
        secim = input(Fore.LIGHTGREEN_EX + "Choose one : " + Style.RESET_ALL)
        print("")
        if secim == '1':
            clear_screen()
            platformisim = input(Fore.LIGHTGREEN_EX + "Save password for this platform : " + Style.RESET_ALL)
            randvalue = randomsifre()   #bu gerçek şifre ve şifrelenmesi gerekir.
            AddPassword(platformisim,randvalue)
            print(f"     Your password : {randvalue}")
        if secim == '2':
            clear_screen()
            platformisim = input(Fore.LIGHTGREEN_EX + "Save password for this platform : " + Style.RESET_ALL)
            while True:
                sifre = input(Fore.LIGHTGREEN_EX + "Create your password : " + Style.RESET_ALL)
                if len(sifre) < 8:
                    print("     Pass is to short!!")
                else:
                    AddPassword(platformisim,sifre)
                    print("")
                    break
    elif girdi == '2':
        clear_screen()
        print("")
        printthecontext()
        print("")
    elif girdi == '3':
        clear_screen()
        print("")
        userinput = input(Fore.LIGHTGREEN_EX + "All your credentials will be deleted are you sure Y/n :" + Style.RESET_ALL)
        if userinput == 'y' or userinput == 'Y':
            reseter()
            print("")
        elif userinput == 'n' or userinput == 'N':
            print("     Passwords didn't deleted\n")
        else:
            print("     You suppose to choose y or n !!!\n")
    elif girdi == '4':
        clear_screen()
        test = input(Fore.LIGHTGREEN_EX + "Enter your password : " + Style.RESET_ALL)
        IsPassStrong(test)
    elif girdi == '5':
        clear_screen()
        print("")
        print("     [1] Remove the credential    [2] Update the Value\n")
        uinput = input(Fore.LIGHTGREEN_EX + "Choose option : " + Style.RESET_ALL)
        printthecontext()
        if uinput == '1':
            cred = input("what credential you want to remove : ")
            Remove(cred)
            print("")
            printthecontext()
            print("")
        elif uinput == '2':
            cred = input(Fore.LIGHTGREEN_EX + "what credential you want to update : " + Style.RESET_ALL)
            while True:
                value = input("New password for this credential : ")
                if len(value) < 8:
                    print(Fore.RED + "     Password is too short " + Style.RESET_ALL)
                else:
                    Updater(cred,value)
                    print("")
                    break
            printthecontext()
            print("")
    elif girdi == 'q' or girdi == 'Q':
        sys.exit()