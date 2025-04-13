from configparser import ConfigParser
from pathlib import Path

path = Path(__file__).parent/"config/config.ini"
config = ConfigParser()
config["SERVER"] ={
    # qual port o servidor usa
    "port": "",
    # o ip do servidor. o mesmo usado no agendador-servidor
    "host": ""
}

config["EMAILS"] = {
    # lista de emails que vao ser selecionaveis.
    # e.g. "exemplo@exemplo.com.br, exemplo2@exemplo.com"
    # aparacem como opções em uma combo box (select em html)
    "emails": ""
}

with open(path, "w") as file:
    config.write(file)
