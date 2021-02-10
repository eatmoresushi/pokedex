import requests
import pandas as pd


def str_break(word):
    '''Break strings at upper case'''
    list = [x for x in word]
    for char_ind in range(1, len(list)):
        if list[char_ind].isupper():
            list[char_ind] = '' + list[char_ind]
    fin_list = ''.join(list).split()
    return fin_list


def str_bracket(word):
    if "Mr. " in word:
        if word == "Mr. Mime Galarian Mr. Mime":
            return "Mr. Mime (Galarian Mr. Mime)"
        else:
            return word
    elif word == 'Type: Null' or word == 'Mime Jr.':
        return word
    else:
        words = word.split(' ', 1)
        if len(words) > 1:
            name, form = words
            form = '(' + form + ')'
            return name + ' ' + form
        else:
            return word


def main():
    url = 'https://pokemondb.net/pokedex/all'
    page = requests.get(url)
    # https://stackoverflow.com/a/61448317
    df = pd.read_html(page.text)[0]
    df['Type'] = df['Type'].apply(str_break)
    df['Name'] = df['Name'].apply(str_bracket)
    print(df.head())
    df.to_json('PokemonData.json')


if __name__ == "__main__":
    main()
