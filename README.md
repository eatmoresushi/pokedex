# Pokédex

A fun weekend project I did. Basically it is a Pokédex written by Python. I used Qt for Python [(PySide6)](https://wiki.qt.io/Qt_for_Python) for the GUI. All Pokédex data is scrapped from [PokémonDB](https://pokemondb.net/pokedex/all). The GUI displays a picture and its statis for each Pokémon and supports searching by dex number or name.

`pokedex.py` is the file scrapping data and `pokedex_gui.py` is for the GUI implementation.

I was insipred from [here](https://towardsdatascience.com/diy-pokedex-with-python-be32e5e3006e) and I included the origrial tutorial in the `Tutorial` folder. The original code does not address special cases for Pokédex names (For example, Galarian Darmanitan Standard Mode) and no search function. I addressed both of them in mine.
