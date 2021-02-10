import pandas as pd
import sys
from urllib.request import urlopen, Request
from PySide6 import QtCore, QtWidgets, QtGui


def int_to_str(number):
    return str(number).zfill(3)


class PokeDex(QtWidgets.QWidget):
    def __init__(self):
        super(PokeDex, self).__init__()
        self.initUI()

    def initUI(self):
        """
        initial UI
        """
        # Grid Layout
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        # Parse JSON for dataframe
        self.df = pd.read_json('PokemonData.json')
        self.df = self.df.sort_values('#')
        self.df['#'] = self.df['#'].apply(int_to_str)
        self.df['Index'] = self.df['#'] + ' ' + self.df['Name']
        # self.df = self.df.set_index(['#'])

        # Drop Down
        self.dropdown = QtWidgets.QComboBox(self)
        self.names = self.df['Name'].values
        self.index = self.df['Index'].values
        self.dropdown.addItems(self.index)
        self.dropdown.currentIndexChanged.connect(self.show_stats)
        self.grid.addWidget(self.dropdown, 0, 0, 1, 1)

        # Search bar
        self.completer = QtWidgets.QCompleter(self.index)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setFilterMode(QtCore.Qt.MatchContains)
        self.searchbar = QtWidgets.QLineEdit(self)
        self.searchbar.setCompleter(self.completer)
        self.grid.addWidget(self.searchbar, 0, 1, 1, 1)
        self.searchbtn = QtWidgets.QPushButton('Search', self)
        self.grid.addWidget(self.searchbtn, 0, 2, 1, 1)
        self.searchbtn.clicked.connect(self.show_stats)

        # Image
        self.img_label = QtWidgets.QLabel()
        img_url = 'https://img.pokemondb.net/artwork/bulbasaur.jpg'
        req = Request(img_url, headers={'User-Agent': "Mozilla/5.0"})
        data = urlopen(req).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        self.img_label.setPixmap(QtGui.QPixmap(image))
        self.grid.addWidget(self.img_label, 1, 1, 1, 2)

        # Data
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText(
            '\nName:\n\nType:\n\nHP:\n\nAttack\n\nSp. Attack\n\nDefense:\n\nSp. Defense:\n\nSpeed:\n\nTotal:')
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.label, 1, 0, 1, 1)

        # Set values
        name = 'Name:\t\t\t' + 'Bulbasaur' + '\n\n'
        ty = 'Type:\t\t\t' + 'Grass, Poison' + '\n\n'
        hp = 'HP:\t\t\t' + '45' + '\n\n'
        atk = 'Attack:\t\t\t' + '49' + '\n\n'
        satk = 'Sp. Attack:\t\t' + '65' + '\n\n'
        deff = 'Defense:\t\t\t' + '49' + '\n\n'
        sdef = 'Sp. Defense:\t\t' + '65' + '\n\n'
        speed = 'Speed:\t\t\t' + '45' + '\n\n'
        total = 'Total:\t\t\t' + '318' + '\n\n'

        # Add text
        final = name + ty + hp + atk + satk + deff + sdef + speed + total
        self.label.setText(final)
        self.label.setAlignment(QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.label, 1, 0, 1, 1)

    def show_stats(self):
        sending_source = self.sender()
        val = ''
        # QComboBox has the attribute 'currentText' while QPushButton does not
        try:
            assert str(sending_source.currentText())
            index = self.dropdown.currentIndex()
            val = self.names[index]
        except AttributeError as e:
            # From QPushButton
            searchbar_txt = self.searchbar.text()
            val = searchbar_txt.split()[1]
        cond = self.df['Name'] == val
        # Image
        base = 'https://img.pokemondb.net/artwork/'
        # index_value = str(self.df[cond].index.values[0])
        img_addition = ''
        if val == "Nidoran\u2640":
            img_addition = "nidoran-f" + '.jpg'
        elif val == "Nidoran\u2642":
            img_addition = "nidoran-m" + '.jpg'
        elif val == 'Farfetch\'d':
            img_addition = 'farfetchd.jpg'
        elif val == "Type: Null":
            img_addition = 'type-null.jpg'
        elif val == "Mime Jr." or val == "Mr. Mime" or val == "Mr. Rime":
            name = val.replace('. ', '-').lower()
            img_addition = name + '.jpg'
        elif val == "Mr. Mime (Galarian Mr. Mime)":
            img_addition = 'mr-mime-galarian.jpg'
        elif '(' in val and ')' in val:
            form = val[val.find("(")+1:val.find(")")].lower()
            name = val.split(' ', 1)[0].lower()
            if 'partner' in form:
                img_addition = name + '-lets-go.jpg'
            elif name == 'greninja':
                img_addition = 'greninja-ash.jpg'
            elif form == "pa'u style":
                img_addition = 'oricorio-pau.jpg'
            elif form == "galarian farfetch'd":
                img_addition = 'farfetchd-galarian.jpg'
            elif name == 'pumpkaboo' or name == 'pumpkaboo' or name == 'rockruff':
                img_addition = name + '.jpg'
            elif name == 'hoopa':
                img_addition = form.replace(' ', '-') + '.jpg'
            elif name == 'zacian' or name == 'zamazenta':
                form_des = form.split(' ')[0]
                img_addition = name + '-' + form_des + '.jpg'
            elif name == 'calyrex':
                img_addition = name + '-' + form.replace(' ', '-') + '.jpg'
            elif name == "zygarde" and 'complete' not in form:
                img_addition = name + '-' + form[0:2] + '.jpg'
            elif name == "eternatus":
                # TODO right now using an external picture
                pass
            elif 'mega' in form:
                words = form.split()
                if len(words) == 3 and words[2] == 'x':
                    img_addition = name + '-mega-x' + '.jpg'
                elif len(words) == 3 and words[2] == 'y':
                    img_addition = name + '-mega-y' + '.jpg'
                else:
                    img_addition = name + '-mega' + '.jpg'
            else:
                fin_des = ''
                if ' ' in form:
                    form_des = form.split()
                    form_des.pop()
                    fin_des = '-'.join(form_des)
                else:
                    fin_des = form
                if name == "castform":
                    img_addition = 'vector/' + name + '-' + fin_des + '.png'
                else:
                    img_addition = name + '-' + fin_des + '.jpg'
        else:
            img_addition = val.lower() + '.jpg'
        img_url = base + img_addition
        if val == "Eternatus (Eternamax)":
            img_url = "https://static.wikia.nocookie.net/villains/images/7/76/HOME890E.png"
        # print(img_url)
        req = Request(img_url, headers={'User-Agent': "Mozilla/5.0"})
        data = urlopen(req).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        self.img_label.setPixmap(QtGui.QPixmap(image))

        # Set values
        name = 'Name:\t\t\t' + val + '\n\n'
        ty = 'Type:\t\t\t' + \
            ', '.join(self.df[cond]['Type'].values[0]) + '\n\n'
        hp = 'HP:\t\t\t' + str(self.df[cond]['HP'].values[0]) + '\n\n'
        atk = 'Attack:\t\t\t' + str(self.df[cond]['Attack'].values[0]) + '\n\n'
        satk = 'Sp. Attack:\t\t' + \
            str(self.df[cond]['Sp. Atk'].values[0]) + '\n\n'
        deff = 'Defense:\t\t\t' + \
            str(self.df[cond]['Defense'].values[0]) + '\n\n'
        sdef = 'Sp. Defense:\t\t' + \
            str(self.df[cond]['Sp. Def'].values[0]) + '\n\n'
        speed = 'Speed:\t\t\t' + str(self.df[cond]['Speed'].values[0]) + '\n\n'
        total = 'Total:\t\t\t' + str(self.df[cond]['Total'].values[0]) + '\n\n'

        # Add text
        final = name + ty + hp + atk + satk + deff + sdef + speed + total
        self.label.setText(final)

        # Clean searchbar
        self.searchbar.clear()


def main():
    '''Codes for running GUI'''
    # todo search
    app = QtWidgets.QApplication([])

    widget = PokeDex()
    widget.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
