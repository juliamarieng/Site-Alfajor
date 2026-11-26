import os


class Config:
    
    WHATSAPP_NUMERO = os.getenv("WHATSAPP_NUMERO", "5561996352399")
    LOJA_NOME = os.getenv("LOJA_NOME", "Ju Alfajor")
