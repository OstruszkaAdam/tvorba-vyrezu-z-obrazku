# Load the dictionary back from the pickle file.
import pickle

nazvy_vsech_kloubu = pickle.load(open("soubor.p", "rb"))
print(nazvy_vsech_kloubu)
# favorite_color is now { "lion": "yellow", "kitty": "red" }
