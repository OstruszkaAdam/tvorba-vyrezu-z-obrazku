# https://wiki.python.org/moin/UsingPickle

# Save a dictionary into a pickle file.
import pickle

nazvy_vsech_kloubu = {
    # poradi kloubu je od ukazovacku k malicku (tzn od 2 do 5) a od MCP k DIP
    # klouby zapesti a palce nejsou pro tyto ucely relevantni, a proto jsou vynechany

    # MCP vrstva (nejblize k zapesti)
    0: "MCP-2",  # ukazovacek
    1: "MCP-3",  # prostrednicek
    2: "MCP-4",  # prstenicek
    3: "MCP-5",  # malicek

    # PIP vrstva
    4: "PIP-5",  # ukazovacek
    5: "PIP-4",  # prostrednicek
    6: "PIP-3",  # prstenicek
    7: "PIP-2",  # malicek

    # DIP vrstva (kloub mezi predposlednim a poslednim clankem)
    8: "DIP-2",  # ukazovacek
    9: "DIP-3",  # prostrednicek
    10: "DIP-4",  # prstenicek
    11: "DIP-5"  # malicek
}

favorite_color = {"lion": "yellow", "kitty": "red"}

pickle.dump(nazvy_vsech_kloubu, open("soubor.p", "wb"))
