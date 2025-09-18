import sys
import requests
from PyQt5.QtWidgets import (QApplication ,     QWidget   , QLabel
                            , QLineEdit , QPushButton , QVBoxLayout
                            , QGraphicsPixmapItem
                            )
from PyQt5.QtGui import QPixmap, QFont ,QFontDatabase
from PyQt5.QtCore import Qt

class pokemonguesser(QWidget):
    def __init__(self):
        super().__init__()
        self.pokemonlabel = QLabel('enter pokemon name' , self)
        self.pokemon_input = QLineEdit(self)
        self.pokemon_logo = QLabel(self)
        pixmap = QPixmap('pokemon_guesser/pokeball.png')
        self.pokemon_logo.setPixmap(pixmap)
        scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.pokemon_logo.setPixmap(scaled_pixmap)
        self.pokemon_button = QPushButton('Get Data',self)
        self.pokemon_description = QLabel(self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Pokemon Encyclopedia')
        vbox = QVBoxLayout()
        vbox.addWidget(self.pokemonlabel)
        vbox.addWidget(self.pokemon_input)
        vbox.addWidget(self.pokemon_logo)
        vbox.addWidget(self.pokemon_button)
        vbox.addWidget(self.pokemon_description)
        self.setLayout(vbox)

        self.pokemonlabel.setAlignment(Qt.AlignCenter)
        self.pokemon_input.setAlignment(Qt.AlignCenter)
        self.pokemon_logo.setAlignment(Qt.AlignCenter)
        self.pokemon_description.setAlignment(Qt.AlignCenter)

        self.pokemonlabel.setObjectName('pokemonlabel')
        self.pokemon_input.setObjectName('pokemon_input')
        self.pokemon_button.setObjectName('pokemon_button')
        self.pokemon_description.setObjectName('pokemon_description')
        #id = QFontDatabase.addApplicationFont("/PATH/party.ttf")
        #_fontstr = QFontDatabase.applicationFontFamilies(id).at(0)
        #_font = QFont(_fontstr, 8)
        #app.setFont(font)
        id = QFontDatabase.addApplicationFont('pokemon_guesser/Pokemon_font.ttf')
        fontstr = QFontDatabase.applicationFontFamilies(id)[0]
        font = QFont(fontstr,20)
        self.pokemonlabel.setFont(font)
        font = QFont(fontstr,10)
        self.pokemon_button.setFont(font)
        font = QFont('Calibri', 16)
        self.pokemon_description.setFont(font)
        
        self.setStyleSheet('''
                        
                       QWidget {
                           background-color : #fc3030;
                           
                        }
                        QLineEdit#pokemon_input{
                            font-size: 40px;
                            background-color: #ff4444;
                            color: white;
                            border-radius: 10px;
                            padding: 10px;
                           }
                           QPushButton#pokemon_button{
                           background-color : #9c9292;
                           
                           }
                           QLabel#pokemon_description{
                            font-weight: bold;
                           }
                
                        


''')
         #self.get_weather_button.clicked.connect(self.get_weather)
        self.pokemon_button.clicked.connect(self.get_pokemon_data)
    def get_pokemon_data(self):
        try:
            pokemon = self.pokemon_input.text()
            url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
            response = requests.get(url)
            data = response.json()
            self.display_pokemon(data)
        except requests.exceptions.JSONDecodeError:
            self.display_error('Pokemon not found')
        except KeyError:
            self.display_error('Please enter a name')
        except requests.exceptions.ConnectionError:
            self.display_error('Connection lost')

    def display_pokemon(self, data):
       height = data['height']/10
       weight = data['weight']/10
       abilities = [a['ability']['name'] for a in data['abilities']]
       abilities_text = ', '.join(abilities)
       moves = [h['move']['name'] for h in data['moves'][:5]]
       move_text = ', '.join(moves)
       
       desc = f'height = {height}m, weight = {weight}kg \nabilities = {abilities_text} \n moves = {move_text}'

       self.pokemon_description.setText(desc)
    def display_error(self,message):
        self.pokemon_description.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pokemon_app = pokemonguesser()
    pokemon_app.show()
    sys.exit(app.exec())