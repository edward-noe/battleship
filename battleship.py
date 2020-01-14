import tkinter as tk
from functools import partial
from random import randint

# NOTE: App does not yet fully support changing number and size of ships.
SHIPS_BUILT = [5, 4, 3, 3, 2]
OCEAN_COLOR = 'blue4'
SHIP_COLOR = 'gray'
HIT_COLOR = 'red2'


class Battle(tk.Tk):

    # Initializes the Battleship application.
    def __init__(self):

        # Creates a container for frames.
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Creates dictionary of all frames.
        self.frames = {}

        # Adds dictionary entry for main screen.
        frame = MainScreen(container, self)
        self.frames[MainScreen] = frame
        frame.grid(row=0, column=0, sticky='nsew')

        # Displays the main screen.
        self.show_frame(MainScreen)

    # Brings a frame to the foreground.
    def show_frame(self, name):

        frame = self.frames[name]
        frame.tkraise()


class MainScreen(tk.Frame):

    # Initializes the main screen.
    def __init__(self, parent, controller):

        # Initializes the frame.
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Creates dictionary for all buttons. More configuration of this dictionary done later.
        self.buttons = {}
        self.buttons['player'] = {}
        self.buttons['enemy'] = {}

        self.pressed_buttons = []

        self.ships = {}
        self.ships['player'] = {}
        self.ships['enemy'] = {}

        # Creates AI board to keep track of hit attempts.
        self.AI_board = []
        for i in range(10):
            self.AI_board.append([0] * 10)

        # Sets 'state' of the main button to false. check_confirm checks this variable when run.
        self.button_state = tk.BooleanVar()
        self.button_state.set(False)

        # Creates text variable.
        self.main_text = tk.StringVar()
        self.main_text.set('Press "Confirm" to start the game.')
        self.sub_text = tk.StringVar()
        self.sub_text.set('')

        # Creates main container for all other elements.
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky='nsew')

        # Configures relative row heights.
        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=8)
        container.grid_rowconfigure(2, weight=2)
        container.grid_columnconfigure(0, weight=1)

        # Creates top bar element.
        top_bar = tk.Frame(container)
        top_bar.grid(row=0, column=0, sticky='nsew')

        # Configures relative column widths for top bar.
        top_bar.grid_rowconfigure(0, weight=1)
        top_bar.grid_columnconfigure(0, weight=2)
        top_bar.grid_columnconfigure(1, weight=7)
        top_bar.grid_columnconfigure(2, weight=2)
        top_bar.grid_columnconfigure(3, weight=7)
        top_bar.grid_columnconfigure(4, weight=2)

        # Creates player and enemy ships header.
        tk.Label(top_bar, width=4).grid(row=0, column=0)
        tk.Label(top_bar, width=4).grid(row=0, column=2)
        tk.Label(top_bar, width=4).grid(row=0, column=4)
        player_title = tk.Label(top_bar, text='Player Ships', font=(None, 20), width=10, pady=10)
        player_title.grid(row=0, column=1)
        enemy_title = tk.Label(top_bar, text='Enemy Ships', font=(None, 20), width=10, pady=10)
        enemy_title.grid(row=0, column=3)

        # Creates container for the two ship grids.
        ship_grids = tk.Frame(container)
        ship_grids.grid(row=1, column=0, sticky='nsew')

        # Configures relative column widths for ship grids.
        ship_grids.grid_rowconfigure(0, weight=1)
        ship_grids.grid_columnconfigure(0, weight=2)
        ship_grids.grid_columnconfigure(1, weight=7)
        ship_grids.grid_columnconfigure(2, weight=2)
        ship_grids.grid_columnconfigure(3, weight=7)
        ship_grids.grid_columnconfigure(4, weight=2)

        # Creates player and enemy ship grids.
        player_ships = tk.Frame(ship_grids)
        player_ships.grid(row=0, column=1, sticky='nsew')
        enemy_ships = tk.Frame(ship_grids)
        enemy_ships.grid(row=0, column=3, sticky='nsew')
        tk.Label(ship_grids, width=4).grid(row=0, column=0)
        tk.Label(ship_grids, width=4).grid(row=0, column=2)
        tk.Label(ship_grids, width=4).grid(row=0, column=4)

        # Creates 10x10 grid of buttons per grid and configures relative widths and heights.
        for grid in self.buttons:

            # Creates empy dictionary in each row.
            for row_num in range(10):

                self.buttons[grid][row_num] = {}

                player_ships.grid_rowconfigure(row_num, weight=1)
                player_ships.grid_columnconfigure(row_num, weight=1)
                enemy_ships.grid_rowconfigure(row_num, weight=1)
                enemy_ships.grid_columnconfigure(row_num, weight=1)

                # Places button in column in row in grid.
                for column_num in range(10):

                    if grid == 'player':
                        self.buttons[grid][row_num][column_num] = tk.Button(player_ships,
                                                                            command=partial(self.button_press, 'player',
                                                                                            row_num, column_num),
                                                                            width=1, bg=OCEAN_COLOR)
                        self.buttons[grid][row_num][column_num].grid(row=row_num, column=column_num, sticky='nsew')

                    if grid == 'enemy':
                        self.buttons[grid][row_num][column_num] = tk.Button(enemy_ships,
                                                                            command=partial(self.button_press, 'enemy',
                                                                                            row_num, column_num),
                                                                            width=1, bg=OCEAN_COLOR, state='disabled')
                        self.buttons[grid][row_num][column_num].grid(row=row_num, column=column_num, sticky='nsew')

        # Creates bottom bar element.
        bottom_bar = tk.Frame(container)
        bottom_bar.grid(row=2, column=0, sticky='nsew')

        # Configures relative widths and heights.
        bottom_bar.grid_rowconfigure(0, weight=1)
        bottom_bar.grid_rowconfigure(1, weight=1)
        bottom_bar.grid_rowconfigure(2, weight=1)
        bottom_bar.grid_rowconfigure(3, weight=1)
        bottom_bar.grid_columnconfigure(0, weight=3)
        bottom_bar.grid_columnconfigure(1, weight=1)

        # Creates bottom text footer.
        tk.Label(bottom_bar, width=24, height=2).grid(row=0, column=0)
        bottom_text = tk.Label(bottom_bar, textvariable=self.main_text, width=24, height=1)
        bottom_text.grid(row=1, column=0, sticky='sew')
        lower_text = tk.Label(bottom_bar, textvariable=self.sub_text, width=24, height=1)
        lower_text.grid(row=2, column=0, sticky='new')
        tk.Label(bottom_bar, width=24, height=2).grid(row=3, column=0)

        # Creates main button.
        self.main_button = tk.Button(bottom_bar, text='Confirm', font=(None, 10), width=16, height=2,
                                     command=self.place_ships)
        self.main_button.grid(row=0, column=1, rowspan=4)

    # Manages button press.
    def button_press(self, grid, row, column):

        # Checks if button is already registered as press. If it has been, it is registered a unpressed.
        if (row, column) in self.pressed_buttons:

            location = self.pressed_buttons.index((row, column))
            del self.pressed_buttons[location]
            self.buttons[grid][row][column].configure(bg=OCEAN_COLOR)

        # Otherwise, button is added to the list of pressed buttons.
        else:

            self.pressed_buttons.append((row, column))
            self.buttons[grid][row][column].configure(bg=SHIP_COLOR)

    # Manages player attack attempt.
    def attack_press(self, row, column):

        hit = False
        victory = True

        # Checks if any tile in any ship was hit.
        for ship in self.ships['enemy']:

            if (row, column) in self.ships['enemy'][ship]:

                # Disables tile that was hit.
                self.buttons['enemy'][row][column].configure(bg=HIT_COLOR, state='disabled')
                self.main_text.set('You hit an enemy battleship.')

                # Deletes ship tile entry from ships dictionary.
                location = self.ships['enemy'][ship].index((row, column))
                del self.ships['enemy'][ship][location]
                hit = True

            # Sets victory to false unless every ship is destroyed.
            if self.ships['enemy'][ship] != []:

                victory = False

        # Ends game is victory is True.
        if victory == True:

            self.end_game(True)

        # Handles misses.
        if hit == False:

            self.buttons['enemy'][row][column].configure(text='X', fg='white', state='disabled')
            self.main_text.set('You missed the enemy ships.')

        # Runs the enemy turn.
        self.enemy_turn()

    def enemy_turn(self):

        # Randomly generates row and column guess.
        row = randint(0, 9)
        column = randint(0, 9)

        victory = True
        miss = True

        # If row column pair has already been guessed, tries again.
        if self.AI_board[row][column] == 1:

            self.enemy_turn()

        # Adds row column pair to AI board to prevent guessing the same location twice.
        self.AI_board[row][column] = 1

        # Checks if the location was a hit on any ship.
        for ship in self.ships['player']:

            if (row, column) in self.ships['player'][ship]:

                # Changes color of tile on player board.
                self.buttons['player'][row][column].configure(bg=HIT_COLOR)
                self.sub_text.set('The enemy hit your battleship.')

                # Deletes point entry from ships dictionary
                location = self.ships['player'][ship].index((row, column))
                del self.ships['player'][ship][location]

                # Sets miss to False to prevent miss condition from running.
                miss = False

            # Sets victory equal to True if all player ship entries are empty.
            if self.ships['player'][ship] != []:
                victory = False

        # Handles AI miss.
        if miss == True:

            if self.buttons['player'][row][column]['bg'] != HIT_COLOR:

                self.buttons['player'][row][column].configure(text='X', fg='white')
                self.sub_text.set('The enemy missed your ships.')

        if victory == True:

            self.end_game(False)

    # Changes state of button_state variable on press of main_button.
    def state_change(self):

        # Switches state of button_state varibale. Used by other functions to wait for user confirmation.
        if self.button_state.get() == False:

            self.button_state.set(True)

        else:

            self.button_state.set(False)

    # Places player ships on the board.
    def place_ships(self):

        # Reconfigures main button.
        self.main_button.configure(command=self.state_change)

        number_words = ['first', 'second', 'third', 'fourth', 'fifth']
        tile_words = ['five', 'four', 'three', 'three', 'two']

        def create_ship(ship_number):

            # Waits for press of main button.
            app.wait_variable(self.button_state)

            # Adds all buttons pressed during cycle to the ships dictionary.

            if len(self.pressed_buttons) == SHIPS_BUILT[ship_number]:

                self.ships['player'][ship_number] = self.pressed_buttons

            else:

                self.main_text.set(
                    'Incorrect number of ship tiles. The ship must have a length of ' + tile_words[ship_number] + '.')

                # Restarts create_ship function.
                create_ship(ship_number)

            # if self.pressed_buttons
            ascending_row = []
            ascending_column = []

            # Creates lists of row and column number in ascending order used by try-except loop.
            for i in range(len(self.pressed_buttons)):

                row = self.pressed_buttons[i][0]
                column = self.pressed_buttons[i][1]
                ascending_row.append(row)
                ascending_column.append(column)
                ascending_row.sort()
                ascending_column.sort()

            # Tests for adjacency.
            try:

                # Loops for length of ship - 1.
                for i in range(len(ascending_row) - 1):

                    # Checks if the ship is horizontal.
                    if ascending_row[i] == ascending_row[i + 1]:

                        # Checks to ensure each value in the ascending list is 1 greater than the last.
                        if ascending_column[i] + 1 != ascending_column[i + 1]:

                            raise ValueError

                    if ascending_column[i] == ascending_column[i + 1]:

                        if ascending_row[i] + 1 != ascending_row[i + 1]:

                            raise ValueError

                    # Checks to ensure the ship is horizontal or vertical at all. If not, raises exception.
                    if ascending_row[i] != ascending_row[i + 1] and ascending_column[i] != ascending_column[i + 1]:

                        raise ValueError

                    if ascending_row[i] != ascending_row[i - 1] and ascending_column[i] != ascending_column[i - 1]:

                        raise ValueError

            except ValueError:

                self.main_text.set('The ' + tile_words[ship_number] + ' ship tiles must be adjacent.')

                # Restarts create_ship function.
                create_ship(ship_number)

            # Disables pressed buttons.
            for i in range(len(self.pressed_buttons)):

                row = self.pressed_buttons[i][0]
                column = self.pressed_buttons[i][1]
                self.buttons['player'][row][column].configure(state='disabled')

            self.pressed_buttons = []

        for ship_number in range(len(SHIPS_BUILT)):

            # Changes main text.
            self.main_text.set('Place your ' + number_words[ship_number] + ' ship by selecting any ' + tile_words[
                ship_number] + ' adjacent, unoccupied tiles.')

            create_ship(ship_number)

        # Disables all player buttons.
        for row_num in range(10):

            for column_num in range(10):

                self.buttons['player'][row_num][column_num].config(state='disabled')

        # Begins next stage.
        self.create_ships()

    # Places enemy ships on the board.
    def create_ships(self):

        # Creates used_tiles to keep track of where ships have already been placed.
        used_tiles = []
        for i in range(10):

            used_tiles.append([0] * 10)

        # Creates a ship of a given length based on global constant.
        for ship in range(len(SHIPS_BUILT)):

            def build_ship():

                row = randint(0, 9)
                column = randint(0, 9)
                config = randint(0, 3)

                length = SHIPS_BUILT[ship]

                # Checks to ensure all tiles of new ship placement are unused.
                def test_ship():

                    try:

                        for i in range(length - 1):

                            # If the tile has already been used, test_ship returns False.
                            if used_tiles[row][column] == 1:

                                raise IndexError

                            # Checks for initial tile and all additionally generated tiles.
                            if config == 0 and (column + i + 1 < 0 or used_tiles[row][column + i + 1] != 0):

                                raise IndexError

                            if config == 1 and (column - i - 1 < 0 or used_tiles[row][column - i - 1] != 0):

                                raise IndexError

                            if config == 2 and (row + i + 1 < 0 or used_tiles[row + i + 1][column] != 0):

                                raise IndexError

                            if config == 3 and (row - i - 1 < 0 or used_tiles[row - i - 1][column] != 0):

                                raise IndexError

                    except IndexError:

                        return False

                    return True

                # Starts over building the ship if test_ship return False.
                if test_ship() == False:

                    build_ship()

                # If test is successful, places ship into ships dictionary.
                else:

                    # Sets tile as used and adds initial coordinate to ships dictionary.
                    used_tiles[row][column] = 1
                    self.ships['enemy'][ship] = []
                    self.ships['enemy'][ship].append((row, column))

                    for i in range(length - 1):

                        # Based on config, adds additional coordinates to ships dictionary.
                        if config == 0:

                            self.ships['enemy'][ship].append((row, column + i + 1))
                            used_tiles[row][column + i + 1] = 1

                        if config == 1:

                            self.ships['enemy'][ship].append((row, column - i - 1))
                            used_tiles[row][column - i - 1] = 1

                        if config == 2:

                            self.ships['enemy'][ship].append((row + i + 1, column))
                            used_tiles[row + i + 1][column] = 1

                        if config == 3:

                            self.ships['enemy'][ship].append((row - i - 1, column))
                            used_tiles[row - i - 1][column] = 1

            # Builds the ship. This is repeated as part of the main for loop for the number of ships required.
            build_ship()

        self.main_game()

    def main_game(self):

        # Sets enemy buttons to attack_press command.
        for row_num in range(10):

            for column_num in range(10):

                self.buttons['enemy'][row_num][column_num].configure(
                    command=partial(self.attack_press, row_num, column_num), state='normal')

        self.main_text.set('Select the enemy tile you want to fire on.')

    def end_game(self, victory):

        # Disables all buttons.
        for row_num in range(10):

            for column_num in range(10):

                self.buttons['enemy'][row_num][column_num].configure(state='disabled')

        # Handles victory.
        if victory == True:

            self.main_text.set('You win.')
            self.sub_text.set(' ')

        # Handles loss.
        if victory == False:

            self.main_text.set('You lose.')
            self.sub_text.set(' ')


# Configures and runs main application class, Battle.
app = Battle()
app.title('Battleship')
app.minsize(width=800, height=500)
app.mainloop()
