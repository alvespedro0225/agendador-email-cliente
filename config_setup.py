from configparser import ConfigParser
from pathlib import Path

path = Path(__file__).parent/"config/config.ini"
config = ConfigParser()
config["SERVER"] ={
    # qual port o servidor usa
    "port": "10_000",
    # o ip do servidor. o mesmo usado no agendador-servidor
    "host": "192.168.0.11"
}

config["EMAILS"] = {
    # lista de emails que vao ser selecionaveis.
    # e.g. "exemplo@exemplo.com.br, exemplo2@exemplo.com"
    # aparacem como opções em uma combo box (select em html)
    "emails": "alvespedro0225@gmail.com, dak7alves74@gmail.com"
}

with open(path, "w") as file:
    config.write(file)