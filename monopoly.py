from random import randint
from random import shuffle
from re import L
import textwrap

class Player:
    def __init__(self, player_name, player_token):
        """Create a player from input"""
        self.name = player_name
        self.token = player_token
        self.money = 1500
        self.properties = []
        self.railroads_owned = 0
        self.utilities_owned = 0
        self.die1 = 0
        self.die2 = 0
        self.last_roll = 0
        self.in_jail = False
        self.is_turn = False
        self.jail_time = 0
    
    def __repr__(self):
        """Return description of player"""
        return f'''\
            This player, {self.name}, is playing as the {self.token}. 
            {self.name} has ${self.money}, is currently on {monopoly_board.player_positions[monopoly_board.player_list.index(self)]}, and owns these properties: 
            {self.properties}
            '''
    def roll_dice(self):
        """Roll two dice and return the results"""
        self.die1 = randint(1,6)
        self.die2 = randint(1,6)
        self.last_roll = self.die1 + self.die2
        if self.last_roll == 8 or self.last_roll == 11:
            print(f"{self.name} rolled an {self.last_roll}! ({self.die1} + {self.die2})")
        else:
            print(f"{self.name} rolled a {self.last_roll}! ({self.die1} + {self.die2})")
        return (self.die1, self.die2, self.last_roll)
    
    def take_turn(self):
        """Roll dice and repeat if doubles are achieved, unless it's done three times in a row"""
        self.is_turn = True
        turn_count = 0
        while self.is_turn or turn_count < 3:
            turn_count += 1
            self.update_position()
            if self.is_turn and turn_count < 3:
                print(f"{self.name} rolled doubles! {self.name} goes again!")
            elif turn_count >= 3:
                print(f"{self.name} rolled doubles three times in a row! {self.name} goes to jail!")
                self.position = 10
                self.in_jail = True
                self.is_turn = False
    
class Property:
    def __init__(self, name, cost, house_cost, rent, mortgage):
        """Create property from input"""
        self.name = name
        self.cost = cost
        self.house_cost = house_cost
        self.houses = 0
        self.rent = rent
        self.mortgage = mortgage
        self.is_mortgaged = False
        self.is_owned = False
    
    def __repr__(self):
        """Return Title Deed information"""
        return f'''\
            {self.name}: ${self.cost}. 
            Rent ${self.rent[0]}. 
            With 1 House: ${self.rent[1]}. 
            With 2 Houses: ${self.rent[2]}. 
            With 3 Houses: ${self.rent[3]}. 
            With 4 Houses: ${self.rent[4]}. 
            With Hotel: ${self.rent[5]}. 
            
            Mortgage Value: ${self.mortgage}. 
            Houses cost ${self.house_cost} each. 
            Hotels, ${self.house_cost} plus 4 houses. 
            If a player owns ALL the lots in any Color-Group, the rent is Doubled on Unimproved Lots in that group.
            '''
    
    def buy_property(self, player, board):
        """Append property to player property list"""
        if player.money < self.cost:
            print(f"You don't have enough money to afford this property.")
            print("Putting up property for auction.")
            self.auction(player, board)
            return
        else:
            print(f"{player.name} purchases {self.name} for ${self.cost}.")
            player.money -= self.cost
            player.properties.append(self)
            self.is_owned = True
            self.owner = player

    def auction(self, player, board):
        auction_list = []
        for entry in board.player_list:
            auction_list.append(entry)
        while auction_list[0] != player:
            auction_list.append(auction_list.pop(0))
        bid = 0
        while len(auction_list) > 1:
            for entry in auction_list:
                print(f"{entry.name}, you have ${entry.money}. How much would you like to bid?")
                print("Enter 0 to drop out of the auction.")
                entry_bid = ""
                valid_entry = False
                while type(entry_bid) != int:
                    try:
                        entry_bid = int(input())
                    except:
                        print("Please input a number.")
                while not valid_entry:
                    if entry_bid == 0:
                        print(f"{entry.name} dropped out of the auction.")
                        auction_list.pop(auction_list.index(entry))
                        valid_entry = True
                        continue
                    elif entry_bid <= entry.money and entry_bid > bid:
                        valid_entry = True
                        bid = entry_bid
                        continue
                    elif entry_bid > entry.money:
                        print(f"You attempted to bid more than you own. Please enter a number higher than ${bid} but equal to or lower than the amount of money you have, ${entry.money}.")
                        print(f"Otherwise, enter 0 to drop out of the auction.")
                    elif entry_bid < bid:
                        print(f"Entry was below current highest bid. Please enter a number higher than ${bid} or enter 0 to drop out of the auction.")
                    entry_bid = ""
                    while type(entry_bid) != int:
                        try:
                            entry_bid = int(input())
                        except:
                            print("Please input a number.")
        print(f"Auction completed. {auction_list[0].name} purchases the property for ${bid}.")
        auction_list[0].money -= bid
        auction_list[0].properties.append(self)        

    def buy_house(self, player):
        """Place houses on property"""
        if player.money < self.house_cost:
            print(f"You don't have enough money to afford a house here.")
            return
        else:
            if self.houses < 5:
                self.houses += 1
            else:
                print(f"This property already has a hotel.")
        
    def charge_rent(self, renter):
        """Take money from player who lands on owned property"""
        self.owner.money += self.rent[self.houses]
        renter.money -= self.rent[self.houses]
        print(f"{renter.name} landed on {self.name}. Rent with {self.houses} houses costs ${self.rent[self.houses]}.")
        print(f"{renter.name} paid {self.owner.name} ${self.rent[self.houses]}.")

    def interact(self, player, board):
        if self.is_owned == False:
            print("Would you like to put this property up for auction?")
            response = str(input()).title()
            while response != "Yes" and response != "No":
                print("Please enter Yes or No.")
                response = str(input()).title()
            if response == "Yes":
                self.auction(player, board)
            else:
                self.buy_property(player, board)
        else:
            if self.owner == player:
                print("You own this property.")
                return
            self.charge_rent(player)

class Railroad():
    def __init__(self, name):
        """Create Railroad property from input"""
        self.name = name
        self.cost = 200
        self.rent = [25, 50, 100, 200]
        self.mortgage = 100
        self.is_mortgaged = False
        self.is_owned = False
    
    def __repr__(self):
        """Return Title Deed information"""
        return f'''\
            {self.name}: ${self.cost}
            Rent: ${self.rent[0]}
            If 2 R.R.'s are owned: ${self.rent[1]}
            If 3 R.R.'s are owned: ${self.rent[2]}
            If 4 R.R.'s are owned: ${self.rent[3]}

            Mortgage Value: ${self.mortgage}
            '''
    
    def buy_property(self, player, board):
        """Append railroad to player property list"""
        if player.money < self.cost:
            print(f"You don't have enough money to afford this railroad.")
            print("Putting up property for auction.")
            self.auction(player, board)
            return
        else:
            print(f"{player.name} purchases {self.name} for ${self.cost}.")
            player.money -= self.cost
            player.properties.append(self)
            player.railroads_owned += 1
            self.is_owned = True
            self.owner = player

    def auction(self, player, board):
        auction_list = []
        for entry in board.player_list:
            auction_list.append(entry)
        while auction_list[0] != player:
            auction_list.append(auction_list.pop(0))
        bid = 0
        while len(auction_list) > 1:
            for entry in auction_list:
                print(f"{entry.name}, you have ${entry.money}. How much would you like to bid?")
                print("Enter 0 to drop out of the auction.")
                entry_bid = ""
                valid_entry = False
                while type(entry_bid) != int:
                    try:
                        entry_bid = int(input())
                    except:
                        print("Please input a number.")
                while not valid_entry:
                    if entry_bid == 0:
                        print(f"{entry.name} dropped out of the auction.")
                        auction_list.pop(auction_list.index(entry))
                        valid_entry = True
                        continue
                    elif entry_bid <= entry.money and entry_bid > bid:
                        valid_entry = True
                        bid = entry_bid
                        continue
                    elif entry_bid > entry.money:
                        print(f"You attempted to bid more than you own. Please enter a number higher than ${bid} but equal to or lower than the amount of money you have, ${entry.money}.")
                        print(f"Otherwise, enter 0 to drop out of the auction.")
                    elif entry_bid < bid:
                        print(f"Entry was below current highest bid. Please enter a number higher than ${bid} or enter 0 to drop out of the auction.")
                    entry_bid = ""
                    while type(entry_bid) != int:
                        try:
                            entry_bid = int(input())
                        except:
                            print("Please input a number.")
        print(f"Auction completed. {auction_list[0].name} purchases the property for ${bid}.")
        auction_list[0].money -= bid
        auction_list[0].properties.append(self)

    def charge_rent(self, renter, chance_card = False):
        """Take money from player who lands on owned railroad"""
        if chance_card == True:
            self.owner.money += self.rent[self.owner.railroads_owned-1] * 2
            renter.money -= self.rent[self.owner.railroads_owned-1] * 2
            if self.owner.railroads_owned == 1:
                print(f"You landed on {self.name}. Rent with {self.owner.railroads_owned} railroad owned costs ${self.rent[self.owner.railroads_owned-1]}, times 2, for a total of ${self.rent[self.owner.railroads_owned-1] * 2}.")
            else:
                print(f"You landed on {self.name}. Rent with {self.owner.railroads_owned} railroads owned costs ${self.rent[self.owner.railroads_owned-1]}, times 2, for a total of ${self.rent[self.owner.railroads_owned-1] * 2}.")
            return
        self.owner.money += self.rent[self.owner.railroads_owned-1]
        renter.money -= self.rent[self.owner.railroads_owned-1]
        if self.owner.railroads_owned == 1:
            print(f"{renter.name} landed on {self.name}. Rent with {self.owner.railroads_owned} railroad owned costs ${self.rent[self.owner.railroads_owned-1]}.")
        else:
            print(f"{renter.name} landed on {self.name}. Rent with {self.owner.railroads_owned} railroads owned costs ${self.rent[self.owner.railroads_owned-1]}.")
        print(f"{renter.name} paid {self.owner.name} ${self.rent[self.owner.railroads_owned-1]}.")

    def interact(self, player, board):
        if self.is_owned == False:
            print("Would you like to put this property up for auction?")
            response = str(input()).title()
            while response != "Yes" and response != "No":
                print("Please enter Yes or No.")
                response = str(input()).title()
            if response == "Yes":
                self.auction(player, board)
            else:
                self.buy_property(player, board)
        else:
            self.charge_rent(player)

class Utility():
    def __init__(self, name):
        """Create Utility property from input"""
        self.name = name
        self.cost = 150
        self.rent = 0
        self.mortgage = 75
        self.is_mortgaged = False
        self.is_owned = False
    
    def __repr__(self):
        """Return Title Deed information"""
        return f'''\
            {self.name}: {self.cost}
            If one "Utility" is owned
            rent is 4 times amount shown on dice.
            If both "Utilities" are owned
            rent is 10 times amount shown on dice.

            Mortgage Value: ${self.mortgage}
            '''
    
    def buy_property(self, player, board):
        """Append utility to player property list"""
        if player.money < self.cost:
            print(f"You don't have enough money to afford this railroad.")
            print("Putting up property for auction.")
            self.auction(player, board)
            return
        else:
            print(f"{player.name} purchases {self.name} for ${self.cost}.")
            player.money -= self.cost
            player.properties.append(self)
            player.utilities_owned += 1
            self.is_owned = True
            self.owner = player

    def auction(self, player, board):
        auction_list = []
        for entry in board.player_list:
            auction_list.append(entry)
        while auction_list[0] != player:
            auction_list.append(auction_list.pop(0))
        bid = 0
        while len(auction_list) > 1:
            for entry in auction_list:
                print(f"{entry.name}, you have ${entry.money}. How much would you like to bid?")
                print("Enter 0 to drop out of the auction.")
                entry_bid = ""
                valid_entry = False
                while type(entry_bid) != int:
                    try:
                        entry_bid = int(input())
                    except:
                        print("Please input a number.")
                while not valid_entry:
                    if entry_bid == 0:
                        print(f"{entry.name} dropped out of the auction.")
                        auction_list.pop(auction_list.index(entry))
                        valid_entry = True
                        continue
                    elif entry_bid <= entry.money and entry_bid > bid:
                        valid_entry = True
                        bid = entry_bid
                        continue
                    elif entry_bid > entry.money:
                        print(f"You attempted to bid more than you own. Please enter a number higher than ${bid} but equal to or lower than the amount of money you have, ${entry.money}.")
                        print(f"Otherwise, enter 0 to drop out of the auction.")
                    elif entry_bid < bid:
                        print(f"Entry was below current highest bid. Please enter a number higher than ${bid} or enter 0 to drop out of the auction.")
                    entry_bid = ""
                    while type(entry_bid) != int:
                        try:
                            entry_bid = int(input())
                        except:
                            print("Please input a number.")
        print(f"Auction completed. {auction_list[0].name} purchases the property for ${bid}.")
        auction_list[0].money -= bid
        auction_list[0].properties.append(self)
    
    def charge_rent(self, renter, chance_card = False):
        """Take money from player who lands on owned utility"""
        if chance_card == True:
            self.rent = renter.last_roll * 10
            print(f"{renter.name} landed on {self.name}. Rent costs 10 * your roll, {renter.last_roll}, ${self.rent}.")
        elif self.owner.utilities_owned == 1:
            self.rent = renter.last_roll * 4
            print(f"{renter.name} landed on {self.name}. Rent with {self.owner.utilities_owned} utility owned costs 4 * the last roll, {renter.last_roll}, ${self.rent}.")
        elif self.owner.utilities_owned == 2:
            self.rent = renter.last_roll * 10
            print(f"{renter.name} landed on {self.name}. Rent with {self.owner.utilities_owned} utilities owned costs 10 * the last roll, {renter.last_roll}, ${self.rent}.")
        self.owner.money += self.rent
        renter.money -= self.rent
        print(f"{renter.name} paid {self.owner.name} ${self.rent}.")
    
    def interact(self, player, board):
        if self.is_owned == False:
            print("Would you like to put this property up for auction?")
            response = str(input()).title()
            while response != "Yes" and response != "No":
                print("Please enter Yes or No.")
                response = str(input()).title()
            if response == "Yes":
                self.auction(player, board)
            else:
                self.buy_property(player, board)
        else:
            self.charge_rent(player)

class Board():
    def __init__(self, layout):
        """Create Board object from list"""
        self.layout = layout
        self.length = len(layout)
        self.player_list = []
        self.player_positions = []
        self.player_turn = 0

    def update_position(self, player, die1 = 0, die2 = 0, spaces_to_move = 0):
        """Move players around board"""
        player_index = self.player_list.index(player)
        while spaces_to_move > 0:
            self.player_positions[player_index] += 1
            spaces_to_move -= 1
            # Wrap around board
            if self.player_positions[player_index] >= self.length:
                self.player_positions[player_index] = 0
                player.money += 200
                print(f"{player.name} passed Go and collects $200.")
        return

    def go_to_jail(self, player):
        self.player_positions[self.player_list.index(player)] = self.layout.index(jail)
        print(f"{player.name} is on space {self.player_positions[self.player_list.index(player)]} and is in Jail.")
        player.in_jail = True
        player.jail_time = 0
        player.die1 = 0

class Chance:
    def __init__(self, name, card_list):
        self.name = name
        self.card_list = card_list
        self.active_card = {}
        shuffle(self.card_list)
        self.jailbreak = {"owner": "None"}
    
    def draw_card(self, player, board):
        self.active_card = self.card_list.pop(0)
        print(f"{player.name} draws a card!")
        print(f'{self.active_card["text"]}')
        if self.active_card["type"] == "movement":
            self.movement_card(player, board)
        elif self.active_card["type"] == "payment":
            self.payment_card(player)
        elif self.active_card["type"] == "collection":
            self.collection_card(player, board)
        elif self.active_card["type"] == "jail":
            self.jail_card(player, board)
        elif self.active_card["type"] == "jailbreak":
            self.jailbreak_card(player)
        elif self.active_card["type"] == "utility":
            self.utility_card(player, board)
        elif self.active_card["type"] == "railroad":
            self.railroad_card(player, board)
        elif self.active_card["type"] == "x_spaces":
            self.move_x_spaces(player, board)

    def movement_card(self, player, board):
        current_space = board.player_positions[board.player_list.index(player)]
        target_space = board.layout.index(self.active_card["target"])
        spaces_to_move = 0
        if target_space > current_space:
            spaces_to_move = target_space - current_space
        else:
            spaces_to_move = board.length - (current_space - target_space)
        board.update_position(player = player, spaces_to_move = spaces_to_move)
        current_position = board.player_positions[board.player_list.index(player)]
        print(f"{player.name} landed on space {current_position}, {board.layout[current_position].name}.")
        board.layout[current_position].interact(player = player, board = board)
        self.card_list.append(self.active_card)
        self.active_card = {}
    
    def move_x_spaces(self, player, board):
        player_index = board.player_list.index(player)
        board.player_positions[player_index] += self.active_card["target"]
        current_position = board.player_positions[player_index]
        print(f"{player.name} landed on space {current_position}, {board.layout[current_position].name}.")
        board.layout[current_position].interact(player = player, board = board)
        self.card_list.append(self.active_card)
        self.active_card = {}
    
    def payment_card(self, player):
        player.money += self.active_card["amount"]
        self.card_list.append(self.active_card)
        self.active_card = {}
    
    def collection_card(self, active_player, board):
        for player in board.player_list:
            player.money -= self.active_card["amount"]
            active_player.money += self.active_card["amount"]
        self.card_list.append(self.active_card)
        self.active_card = {}
    
    def jail_card(self, player, board):
        board.go_to_jail(player)
        self.card_list.append(self.active_card)
        self.active_card = {}
    
    def jailbreak_card(self, player):
        self.jailbreak = self.active_card
        self.jailbreak["owner"] = player
        self.active_card = {}
    
    def utility_card(self, player, board):
        is_utility = False
        while not is_utility:
            board.update_position(player = player, spaces_to_move = 1)
            if type(board.layout[board.player_positions[board.player_list.index(player)]]) == Utility:
                is_utility = True
        current_position = board.player_positions[board.player_list.index(player)]
        active_utility = board.layout[board.player_positions[board.player_list.index(player)]]
        if active_utility.is_owned:
            temp_die1 = player.die1
            temp_die2 = player.die2
            temp_last_roll = player.last_roll
            player.roll_dice()
            active_utility.charge_rent(renter = player, chance_card = True)
            player.die1 = temp_die1
            player.die2 = temp_die2
            player.last_roll = temp_last_roll
        else:
            print(f"{player.name} landed on space {current_position}, {board.layout[current_position].name}.")
            board.layout[current_position].interact(player = player, board = board)
    
    def railroad_card(self, player, board):
        is_railroad = False
        while not is_railroad:
            board.update_position(player = player, spaces_to_move = 1)
            if type(board.layout[board.player_positions[board.player_list.index(player)]]) == Railroad:
                is_railroad = True
        current_position = board.player_positions[board.player_list.index(player)]
        active_railroad = board.layout[board.player_positions[board.player_list.index(player)]]
        if active_railroad.is_owned:
            active_railroad.charge_rent(renter = player, chance_card = True)
        else:
            print(f"{player.name} landed on space {current_position}, {monopoly_board.layout[current_position].name}.")
            monopoly_board.layout[current_position].interact(player = player, board = monopoly_board)
    
    def interact(self, player, board):
        self.draw_card(player = player, board = board)

class Miscellaneous:
    def __init__ (self, name):
        self.name = name
    
    def interact (self, player, board):
        if self.name == "Go":
            return
        elif self.name == "Income Tax":
            print(f"{player.name} pays Income Tax of $200.")
            player.money -= 200
        elif self.name == "Jail":
            print(f"Just Visiting!")
        elif self.name == "Free Parking":
            print(f"Nothing interesting happens.")
        elif self.name == "Go To Jail":
            board.go_to_jail(player)
        elif self.name == "Luxury Tax":
            print(f"{player.name} pays Luxury Tax of $75.")
            player.money -= 75

mediterranean_ave = Property(name="Mediterranean Avenue", cost=60, house_cost=50, rent=[2, 10, 30, 90, 160, 250], mortgage=30)
baltic_ave = Property(name="Baltic Avenue", cost=60, house_cost=50, rent=[4, 20, 60, 180, 320, 450], mortgage=30)
oriental_ave = Property(name="Oriental Avenue", cost=100, house_cost=50, rent=[6, 30, 90, 270, 400, 550], mortgage=50)
vermont_ave = Property(name="Vermont Avenue", cost=100, house_cost=50, rent=[6, 30, 90, 270, 400, 550], mortgage=50)
connecticut_ave = Property(name="Connecticut Avenue", cost=120, house_cost=50, rent=[8, 40, 100, 300, 450, 600], mortgage=60)
st_charles_place = Property(name="St. Charles Place", cost=140, house_cost=100, rent=[10, 50, 150, 450, 625, 750], mortgage=70)
states_ave = Property(name="States Avenue", cost=140, house_cost=100, rent=[10, 50, 150, 450, 625, 750], mortgage=70)
virginia_ave = Property(name="Virginia Avenue", cost=160, house_cost=100, rent=[12, 60, 180, 500, 700, 900], mortgage=80)
st_james_place = Property(name="St. James Place", cost=180, house_cost=100, rent=[14, 70, 200, 550, 750, 950], mortgage=90)
tennessee_ave = Property(name="Tennessee Avenue", cost=180, house_cost=100, rent=[14, 70, 200, 550, 750, 950], mortgage=90)
new_york_ave = Property(name="New York Avenue", cost=200, house_cost=100, rent=[16, 80, 220, 600, 800, 1000], mortgage=100)
kentucky_ave = Property(name="Kentucky Avenue", cost=220, house_cost=150, rent=[18, 90, 250, 700, 875, 1050], mortgage=110)
indiana_ave = Property(name="Indiana Avenue", cost=220, house_cost=150, rent=[18, 90, 250, 700, 875, 1050], mortgage=110)
illinois_ave = Property(name="Illinois Avenue", cost=240, house_cost=150, rent=[20, 100, 300, 750, 925, 1100], mortgage=120)
atlantic_ave = Property(name="Atlantic Avenue", cost=260, house_cost=150, rent=[22, 110, 330, 800, 975, 1150], mortgage=130)
ventnor_ave = Property(name="Ventnor Avenue", cost=260, house_cost=150, rent=[22, 110, 330, 800, 975, 1150], mortgage=130)
marvin_gardens = Property(name="Marvin Gardens", cost=280, house_cost=150, rent=[24, 120, 360, 850, 1025, 1200], mortgage=140)
pacific_ave = Property(name="Pacific Avenue", cost=300, house_cost=200, rent=[26, 130, 390, 900, 1100, 1275], mortgage=150)
north_carolina_ave = Property(name="North Carolina Avenue", cost=300, house_cost=200, rent=[26, 130, 390, 900, 1100, 1275], mortgage=150)
pennsylvania_ave = Property(name="Pennsylvania Avenue", cost=320, house_cost=200, rent=[28, 150, 450, 1000, 1200, 1400], mortgage=160)
park_place = Property(name="Park Place", cost=350, house_cost=200, rent=[35, 175, 500, 1100, 1300, 1500], mortgage=175)
boardwalk = Property(name="Boardwalk", cost=400, house_cost=200, rent=[50, 200, 600, 1400, 1700, 2000], mortgage=200)

reading_rr = Railroad(name="Reading Railroad")
pennsylvania_rr = Railroad(name="Pennsylvania Railroad")
b_and_o_rr = Railroad(name="B. & O. Railroad")
short_line_rr = Railroad(name="Short Line")

electric_company = Utility(name="Electric Company")
water_works = Utility(name="Water Works")

go_space = Miscellaneous("Go")
income_tax = Miscellaneous("Income Tax")
jail = Miscellaneous("Jail")
free_parking = Miscellaneous("Free Parking")
go_to_jail = Miscellaneous("Go To Jail")
luxury_tax = Miscellaneous("Luxury Tax")

chance = Chance("Chance", [
    {"text": 'Advance to "Go". \n(Collect $200)', "type": "movement", "target": go_space},
    {"text": 'Advance to Illinois Ave.', "type": "movement", "target": illinois_ave},
    {"text": 'Advance to St. Charles Place.', "type": "movement", "target": st_charles_place},
    {"text": 'Advance token to the nearest Utility. \nIf unowned, you may buy it from the Bank. \nIf owned, throw dice and pay owner a total 10 times the amount thrown.', "type": "utility"},
    {"text": 'Advance token to the nearest Railroad and pay the owner Twice the Rental to which they are entitled. \nIf Railroad is UNOWNED you may buy it from the Bank.', "type": "railroad"},
    {"text": 'Advance token to the nearest Railroad and pay the owner Twice the Rental to which they are entitled. \nIf Railroad is UNOWNED you may buy it from the Bank.', "type": "railroad"},
    {"text": 'Go Back 3 Spaces.', "type": "x_spaces", "target": -3},
    {"text": 'Take a trip to Reading Railroad. \nIf you pass Go, collect $200.', "type": "movement", "target": reading_rr},
    {"text": 'Take a walk on the Boardwalk. \nAdvance token to Boardwalk.', "type": "movement", "target": boardwalk},
    {"text": 'Go to Jail. Go directly to Jail. \nDo not pass GO, do not collect $200.', "type": "jail"},
    {"text": 'Get out of Jail Free. This card may be kept until needed or traded/sold.', "type": "jailbreak", "owner": "None"},
    {"text": 'Bank pays you a dividend of $50.', "type": "payment", "amount": 50},
    {"text": 'Your building loan matures. \nCollect $150.', "type": "payment", "amount": 150},
    {"text": 'Pay school tax of $150.', "type": "payment", "amount": -150},
    {"text": 'Make general repairs on all your property: \nFor each house pay $25, \nFor each Hotel $100.', "type": "house", "amount": [25, 100]},
    {"text": 'You have been elected Chairman of the Board. Pay each player $50.', "type": "collection", "amount": -50}
    ])

community_chest = Chance("Community Chest", [
    {"text": 'Advance to "Go". \n(Collect $200)', "type": "movement", "target": go_space},
    {"text": 'Bank error in your favor, collect $200.', "type": "payment", "amount": 200},
    {"text": 'Doctor\'s fees, pay $50.', "type": "payment", "amount": -50},
    {"text": 'From sale of stock you get $50.', "type": "payment", "amount": 50},
    {"text": 'Grand Opera Opening. Collect $50 from every player for opening night seats.', "type": "collection", "amount": 50},
    {"text": 'Holiday fund matures. Receive $100.', "type": "payment", "amount": 100},
    {"text": 'Income tax refund. Collect $20.', "type": "payment", "amount": 20},
    {"text": 'It\'s your birthday. Collect $10 from every player.', "type": "collection", "amount": 10},
    {"text": 'Life insurance matures. Collect $100.', "type": "payment", "amount": 100},
    {"text": 'Hospital fees. Pay $100.', "type": "payment", "amount": -100},
    {"text": 'Receive $25 consultancy fee.', "type": "payment", "amount": 25},
    {"text": 'You have won second prize in a beauty contest, collect $10.', "type": "payment", "amount": 10},
    {"text": 'You inherit $100.', "type": "payment", "amount": 100},
    {"text": 'Go to Jail. Go directly to Jail. \nDo not pass GO, do not collect $200.', "type": "jail"},
    {"text": 'Get out of Jail Free. This card may be kept until needed or traded/sold.', "type": "jailbreak", "owner": "None"},
    {"text": 'You are assessed for street repairs: \nPay $40 per house and $115 per hotel you own.', "type": "house", "amount": [40, 115]}
])

brown_group = [mediterranean_ave, baltic_ave]
light_blue_group = [oriental_ave, vermont_ave, connecticut_ave]
pink_group = [st_charles_place, states_ave, virginia_ave]
orange_group = [st_james_place, tennessee_ave, new_york_ave]
red_group = [kentucky_ave, indiana_ave, illinois_ave]
yellow_group = [atlantic_ave, ventnor_ave, marvin_gardens]
green_group = [pacific_ave, north_carolina_ave, pennsylvania_ave]
dark_blue_group = [park_place, boardwalk]

monopoly_board = Board([go_space, mediterranean_ave, community_chest, baltic_ave, income_tax, reading_rr, oriental_ave, chance, vermont_ave, connecticut_ave, 
        jail, st_charles_place, electric_company, states_ave, virginia_ave, pennsylvania_rr, st_james_place, community_chest, tennessee_ave, new_york_ave, 
        free_parking, kentucky_ave, chance, indiana_ave, illinois_ave, b_and_o_rr, atlantic_ave, ventnor_ave, water_works, marvin_gardens, 
        go_to_jail, pacific_ave, north_carolina_ave, community_chest, pennsylvania_ave, short_line_rr, chance, park_place, luxury_tax, boardwalk])





# This space intentionally left blank for testing before running the game









player_count = 0
while player_count < 2 or player_count > 8:
    print("How many players will be playing?")
    try:
        player_count = int(input())
    except:
        print("That wasn't a number!")
    if player_count < 2:
        print("Player count is too low, please select between 2 and 8 players.")
    if player_count > 8:
        print("Player count is too high, please select between 2 and 8 players.")
token_list = ["Dog", "Battleship", "Racecar", "Top Hat", "Thimble", "Wheelbarrow", "Boot", "Iron"]

for i in range(player_count):
    player_choices = []
    print(f"What is Player {i+1}'s name?")
    player_choices.append(input().title())

    while len(player_choices) <= 1:
        print(f"{player_choices[0]}, which piece would you like?")
        print(token_list)
        token_choice = str(input()).title()
        if token_list.count(token_choice) > 0:
            token_list.remove(token_choice)
            player_choices.append(token_choice)
        else:
            print("That token is not available!")
    
    monopoly_board.player_list.append(Player(player_choices[0], player_choices[1]))
    monopoly_board.player_positions.append(0)

first_roll = 0
first_turn = 0

for player in monopoly_board.player_list:
    player.roll_dice()
    if player.last_roll > first_roll:
        first_turn = player
        first_roll = player.last_roll
while first_turn != monopoly_board.player_list[0]:
    monopoly_board.player_list.append(monopoly_board.player_list.pop(0))
print(f'{monopoly_board.player_list[0].name} goes first.')
monopoly_board.player_list[0].is_turn = True

game_active = True

while game_active:
    for player in monopoly_board.player_list:
        turn_count = 0
        player.die1 = 0
        player.die2 = 0


# Jail interactions
        if player.in_jail:
            if player.jail_time < 2:
                print(f"{player.name} is in Jail. Would you like to pay $50 to leave?")
                response = str(input()).title()
                while response != 'Yes' and response != 'No':
                    print("Please enter Yes or No.")
                    response = str(input()).title()
                if response == "Yes":
                    player.money -= 50
                    player.in_jail = False
                    player.jail_time = 0
                    print("Press enter to roll dice.")
                elif response == "No":
                    print(f"Press enter to roll dice.")
                    input()
                    roll1, roll2, movement = player.roll_dice()
                    if roll1 == roll2:
                        print(f"{player.name} rolled doubles and is free from Jail!")
                        player.in_jail = False
                        player.jail_time = 0
                        monopoly_board.update_position(player, roll1, roll2, movement)
                        current_position = monopoly_board.player_positions[monopoly_board.player_list.index(player)]
                        print(f"{player.name} landed on space {current_position}, {monopoly_board.layout[current_position].name}.")
                        monopoly_board.layout[current_position].interact(player = player, board = monopoly_board)
                        player.die1 += 1
                    else:
                        print(f"{player.name} did not roll doubles.")
                        if chance.jailbreak["owner"] == player or community_chest.jailbreak["owner"] == player:
                            print(f"Would you like to use your Get Out of Jail Free card to leave Jail?")
                            response = str(input()).title()
                            while response != 'Yes' and response != 'No':
                                print("Please enter Yes or No.")
                                response = str(input()).title()
                            if response == "Yes":
                                try:
                                    chance.jailbreak["owner"] = "None"
                                    chance.card_list.append(chance.jailbreak)
                                except:
                                    community_chest.jailbreak["owner"] = "None"
                                    community_chest.card_list.append(community_chest.jailbreak)
                                player.in_jail = False
                                player.jail_time = 0
                                monopoly_board.update_position(player, roll1, roll2, movement)
                                current_position = monopoly_board.player_positions[monopoly_board.player_list.index(player)]
                                print(f"{player.name} landed on space {current_position}, {monopoly_board.layout[current_position].name}.")
                                monopoly_board.layout[current_position].interact(player = player, board = monopoly_board)
                            elif response == "No":
                                player.jail_time += 1
                        else:
                            player.jail_time += 1
            else:
                print(f"{player.name} is in Jail. Press enter to roll dice.")
                input()
                roll1, roll2, movement = player.roll_dice()
                if roll1 != roll2:
                    if chance.jailbreak["owner"] == player or community_chest.jailbreak["owner"] == player:
                        print(f"Would you like to use your Get Out of Jail Free card to leave Jail?")
                        response = str(input()).title()
                        while response != 'Yes' and response != 'No':
                            print("Please enter Yes or No.")
                            response = str(input()).title()
                        if response == "Yes":
                            try:
                                chance.jailbreak["owner"] = "None"
                                chance.card_list.append(chance.jailbreak)
                            except:
                                community_chest.jailbreak["owner"] = "None"
                                community_chest.card_list.append(community_chest.jailbreak)
                    else:
                        print(f"{player.name} must pay $50 to leave Jail.")
                        player.money -= 50
                    player.in_jail = False
                    player.jail_time = 0
                    monopoly_board.update_position(player, roll1, roll2, movement)
                    current_position = monopoly_board.player_positions[monopoly_board.player_list.index(player)]
                    print(f"{player.name} landed on space {current_position}, {monopoly_board.layout[current_position].name}.")
                    monopoly_board.layout[current_position].interact(player = player, board = monopoly_board)


# Non-Jail Interactions
        else:
            print(f"{player.name}'s turn! Press enter to roll dice.")
        while (player.die1 == player.die2 and not player.in_jail):
            input()
            roll1, roll2, movement = player.roll_dice()
            turn_count += 1
            if turn_count == 3 and roll1 == roll2:
                print(f"{player.name} rolled doubles three times in a row! {player.name} goes to Jail!")
                monopoly_board.go_to_jail(player)
                break
            monopoly_board.update_position(player, roll1, roll2, movement)
            current_position = monopoly_board.player_positions[monopoly_board.player_list.index(player)]
            print(f"{player.name} landed on space {current_position}, {monopoly_board.layout[current_position].name}.")
            monopoly_board.layout[current_position].interact(player = player, board = monopoly_board)
            if player.die1 == player.die2:
                print(f"{player.name} rolled doubles! Roll again!")
        print(f"{player.name} ends their turn with ${player.money}.") 
    print(f"Would you like to end the game?")
    choice = str(input()).title()
    while choice != "No":
        if choice == "Yes":
            game_active = False
            break
        print("Please enter Yes or No.")
        choice = str(input()).title()
