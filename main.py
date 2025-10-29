import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
from pystyle import Center, Colors, Colorate

# ======================================================================================================================

proxy_url = ""
twitch_username = ""
proxy_count = 0


def initialize():
    """Initialisation du programme et saisie des informations utilisateur"""
    global proxy_url, twitch_username, proxy_count
    os.system('cls')
    os.system(f"title WaXeD - TTVBotZzz ")
    print(Colorate.Vertical(Colors.red_to_purple, Center.XCenter("""
            ██╗    ██╗ █████╗ ██╗  ██╗███████╗██████╗     
            ██║    ██║██╔══██╗╚██╗██╔╝██╔════╝██╔══██╗    
            ██║ █╗ ██║███████║ ╚███╔╝ █████╗  ██║  ██║    
            ██║███╗██║██╔══██║ ██╔██╗ ██╔══╝  ██║  ██║    
            ╚███╔███╔╝██║  ██║██╔╝ ██╗███████╗██████╔╝    
             ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝     
            Github : https://github.com/Wadecx
    """)))

    proxyList = {
        1: "https://www.blockaway.net",
    }

    print(Colorate.Vertical(Colors.red_to_blue, "Proxy Server :"))
    choix_proxy = int(input("> Sélectionnez un numéro de proxy (1, Recommandé) : "))
    proxy_url = proxyList.get(choix_proxy)
    twitch_username = input(Colorate.Vertical(Colors.red_to_blue, "Username Twitch : "))
    proxy_count = int(input(Colorate.Vertical(Colors.red_to_blue, "Nombre de viewers : ")))
    os.system('cls')


def accept_cookies_proxy(driver):
    """Sur le premier onglet : attend 2s puis clique sur le bouton cookies du proxy."""
    try:
        time.sleep(2)
        consent_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fc-cta-consent"))
        )
        consent_button.click()
        print("[🍪] Cookies proxy acceptés.")
        time.sleep(1)
    except Exception:
        print("[ℹ️] Aucun popup cookies détecté sur le proxy.")


def accept_cookies_twitch(driver):
    """Clique sur le bouton cookies Twitch (classe .gxYeIp) si présent."""
    try:
        WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "gxYeIp"))
        )
        twitch_cookies = driver.find_element(By.CLASS_NAME, "gxYeIp")
        twitch_cookies.click()
        print("[🍪] Cookies Twitch acceptés.")
        time.sleep(1)
    except Exception:
        print("[ℹ️] Aucun popup cookies Twitch détecté.")


def main():
    """Fonction principale pour exécuter le bot."""
    global proxy_url, twitch_username, proxy_count

    print(Colorate.Vertical(Colors.red_to_purple, Center.XCenter("""
            ██╗    ██╗ █████╗ ██╗  ██╗███████╗██████╗     
            ██║    ██║██╔══██╗╚██╗██╔╝██╔════╝██╔══██╗    
            ██║ █╗ ██║███████║ ╚███╔╝ █████╗  ██║  ██║    
            ██║███╗██║██╔══██║ ██╔██╗ ██╔══╝  ██║  ██║    
            ╚███╔███╔╝██║  ██║██╔╝ ██╗███████╗██████╔╝    
             ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝     
            Status : Viewers sending !                                                     
    """)))

    # === Configuration Chrome ===
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')  # Décommente pour le mode invisible

    extension_path = 'adblock.crx'
    if os.path.exists(extension_path):
        chrome_options.add_extension(extension_path)

    driver = webdriver.Chrome(options=chrome_options)

    for i in range(proxy_count):
        driver.execute_script(f"window.open('{proxy_url}')")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(proxy_url)

        # Accepter cookies du proxy seulement sur le premier onglet
        if i == 0:
            accept_cookies_proxy(driver)

        try:
            # attendre que le champ URL du proxy soit cliquable
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "url"))
            )
            text_box = driver.find_element(By.ID, "url")
            text_box.clear()
            text_box.send_keys(f"https://www.twitch.tv/{twitch_username}")
            text_box.send_keys(Keys.RETURN)
            print(f"[✅] Onglet {i+1} ouvert vers Twitch : {twitch_username}")

            # ✅ Cliquer sur les cookies Twitch à chaque fois
            accept_cookies_twitch(driver)

        except Exception as e:
            print(f"[❌] Erreur sur l'onglet {i+1} : {e}")
            continue

    wait_time = 120
    print(f"\n⏳ Attente de {wait_time} secondes avant fermeture automatique...")
    time.sleep(wait_time)

    driver.quit()
    print("[✔] Session terminée.\n")


# === Lancement ===
initialize()

if __name__ == '__main__':
    while True:
        main()
        print("🔁 Redémarrage du programme dans 3 secondes...")
        time.sleep(3)
