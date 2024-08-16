from pathlib import Path

class GlobalConfig:
    def __init__(self):
        # Inizialmente tutti i valori sono None
        self.STRINGS_MODULE_RESUME_PATH: Path = None
        self.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH: Path = None
        self.STRINGS_MODULE_NAME: str = None
        self.STYLES_DIRECTORY: Path = None
        self.OUTPUT_FILE_PATH: Path = None
        self.LOG_OUTPUT_FILE_PATH: Path = None
        self.API_KEY: str = None

# Creazione dell'istanza globale
global_config = GlobalConfig()
