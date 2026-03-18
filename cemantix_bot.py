from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class CemantixBot:
    def __init__(self):
        # Initialise le driver proprement
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://cemantix.certitudes.org/")
        time.sleep(2)
        self._close_welcome_popup()
        self._accepter_cookies()
        self._fermer_tuto()

    def _accepter_cookies(self):
        try:
            # On attend maximum 5 secondes que le bouton soit cliquable
            # Le sélecteur CSS ci-dessous est très courant pour ces fenêtres
            bouton_autoriser = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent"))
            )
            bouton_autoriser.click()
            print("Cookies acceptés.")
        except Exception:
            print("Pas de fenêtre de cookies détectée ou sélecteur différent.")

    def _close_welcome_popup(self):
        """Ferme la fenêtre de bienvenue au démarrage."""
        try:
            # Sélecteur typique pour le bouton "OK" ou "Fermer"
            close_btn = self.driver.find_element(By.ID, "cemantix-start")
            close_btn.click()
        except:
            print("Pas de pop-up au démarrage.")
        
    def _fermer_tuto(self):
        try:
            # On attend que la croix de fermeture soit là
            bouton_close = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "dialog-close"))
            )
            bouton_close.click()
            print("Fenêtre explicative fermée via 'dialog-close'.")
        except Exception:
            try:
                # Si 'dialog-close' échoue, on tente le bouton "Démarrer"
                bouton_start = self.driver.find_element(By.ID, "cemantix-start")
                bouton_start.click()
                print("Fenêtre fermée via 'cemantix-start'.")
            except:
                print("Le tuto semble déjà fermé ou l'ID a changé.")

    def recuperer_temperature(self):
        try:
            # On cible la ligne d'ID "guessed" (la dernière tentative)
            # Puis on cherche la 3ème cellule (td) qui contient la température
            element_score = self.driver.find_element(By.CSS_SELECTOR, "#guessed td.number:nth-child(3)")
            
            # Récupération du texte (ex: "-17,14")
            score_brut = element_score.text
            
            # Nettoyage pour Python :
            # 1. Remplacer la virgule par un point
            # 2. Supprimer les espaces bizarres
            score_clean = score_brut.replace(',', '.').strip()
            
            return float(score_clean)
            
        except Exception as e:
            print(f"Erreur lors de la récupération du score : {e}")
            return None

    def envoyer_mot(self, mot):
        """Envoie le mot et récupère le score."""
        try:
            input_field = self.driver.find_element(By.ID, "guess")
            input_field.clear()
            input_field.send_keys(mot)
            input_field.send_keys(Keys.ENTER)
            
            time.sleep(1.5) # Temps de réponse du serveur
            
            return self.recuperer_temperature()
            
        except Exception as e:
            print(f"Erreur avec le mot '{mot}': {e}")
            return None

    def fermer(self):
        self.driver.quit()


if __name__ == "__main__":
    # 1. On initialise le bot
    print("Démarrage du test...")
    mon_bot = CemantixBot()

    try:
        # 2. On teste une liste de mots
        mots_a_tester = ["maison", "soleil", "manger"]
        
        for m in mots_a_tester:
            print(f"Test du mot : {m}")
            score = mon_bot.envoyer_mot(m)
            print(f"Score reçu : {score}")
            
        print("Test terminé avec succès !")
        
    except Exception as e:
        print(f"Le test a échoué : {e}")
    
    finally:
        # 3. On attend un peu pour voir le résultat avant de fermer
        input("Appuie sur Entrée pour fermer le navigateur...")
        mon_bot.fermer()