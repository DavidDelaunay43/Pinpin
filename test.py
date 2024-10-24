import logging
import colorama
from colorama import Fore, Style

# Initialiser Colorama pour une compatibilité Windows
colorama.init(autoreset=True)

# Définir un format personnalisé pour les logs
class ColorFormatter(logging.Formatter):
    """Custom formatter for coloring logs based on log level."""
    
    # Dictionnaire associant les niveaux de log à des couleurs ANSI
    COLORS = {
        logging.DEBUG: Fore.BLUE,      # Bleu pour DEBUG
        logging.INFO: Fore.GREEN,      # Vert pour INFO
        logging.WARNING: Fore.YELLOW,  # Jaune pour WARNING
        logging.ERROR: Fore.RED,       # Rouge pour ERROR
        logging.CRITICAL: Fore.MAGENTA,  # Rouge souligné pour CRITICAL
    }
    
    def format(self, record):
        # Appliquer la couleur en fonction du niveau de log
        log_color = self.COLORS.get(record.levelno, Style.RESET_ALL)
        
        # Formatter par défaut
        log_message = super().format(record)
        
        # Retourner le message avec la couleur associée
        return f"{log_color}{log_message}{Style.RESET_ALL}"

# Configurer le logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Créer un handler de console
console_handler = logging.StreamHandler()

# Appliquer le formatteur coloré
formatter = ColorFormatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Ajouter le handler au logger
logger.addHandler(console_handler)

# Logs de test
logger.debug("Ceci est un message de DEBUG.")
logger.info("Ceci est un message d'INFO.")
logger.warning("Ceci est un message de WARNING.")
logger.error("Ceci est un message d'ERROR.")
logger.critical("Ceci est un message CRITICAL.")
