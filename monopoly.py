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
    
    def __repr__(self):
        """Return description of player"""
        return f'''\
            This player, {self.name}, is playing as the {self.token}. 
            {self.name} has ${self.money}, is currently on {board.player_positions[board.player_list.index(self)]}, and owns these properties: 
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
    
    def buy_property(self, player):
        """Append property to player property list"""
        if player.money < self.cost:
            print(f"You don't have enough money to afford this property.")
            return
        else:
            player.properties.append(self)
            self.is_owned = True

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
        
    def charge_rent(self, owner, renter):
        """Take money from player who lands on owned property"""
        owner.money += self.rent[self.houses]
        renter.money -= self.rent[self.houses]
        print(f"You landed on {self.name}. Rent with {self.houses} houses costs ${self.rent[self.houses]}.")
        print(f"{renter.name} paid {owner.name} ${self.rent[self.houses]}.")

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
    
    def buy_property(self, player):
        """Append railroad to player property list"""
        if player.money < self.cost:
            print(f"You don't have enough money to afford this railroad.")
            return
        else:
            player.properties.append(self)
            player.railroads_owned += 1
            self.is_owned = True

    def charge_rent(self, owner, renter):
        """Take money from player who lands on owned railroad"""
        owner.money += self.rent[owner.railroads_owned-1]
        renter.money -= self.rent[owner.railroads_owned-1]
        print(f"You landed on {self.name}. Rent with {owner.railroads_owned} railroads owned costs ${self.rent[owner.railroads_owned-1]}.")
        print(f"{renter.name} paid {owner.name} ${self.rent[owner.railroads_owned-1]}.")

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
    
    def buy_property(self, player):
        """Append utility to player property list"""
        if player.money < self.cost:
            print(f"You don't have enough money to afford this railroad.")
            return
        else:
            player.properties.append(self)
            player.utilities_owned += 1
            self.is_owned = True
    
    def charge_rent(self, owner, renter):
        """Take money from player who lands on owned utility"""
        if owner.utilities_owned == 1:
            self.rent = renter.last_roll * 4
            print(f"You landed on {self.name}. Rent with {owner.utilities_owned} utilities owned costs 4 * the last roll, {renter.last_roll}, ${self.rent}.")
        elif owner.utilities_owned == 2:
            self.rent = renter.last_roll * 10
            print(f"You landed on {self.name}. Rent with {owner.utilities_owned} utilities owned costs 10 * the last roll, {renter.last_roll}, ${self.rent}.")
        owner.money += self.rent
        renter.money -= self.rent
        print(f"{renter.name} paid {owner.name} ${self.rent}.")

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
        self.player_positions[self.player_list.index(player)] = self.layout.index("Jail")
        print(f"{player.name} is on space {self.player_positions[self.player_list.index(player)]} and is in Jail.")
        player.in_jail = True

class Chance:
    def __init__(self, name, card_list):
        self.name = name
        self.card_list = card_list
        self.active_card = {}
        shuffle(self.card_list)
        self.jailbreak = 0
    
    def draw_card(self, player, board):
        self.active_card = self.card_list.pop(0)
        print(f"{player} draws a card!")
        print(f'{self.active_card["text"]}')
        if self.active_card["type"] == "movement":
            self.movement_coard(player, board)
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

    def movement_card(self, player, board):
        current_space = board.player_positions[board.player_list.index(player)]
        target_space = board.layout.index(self.active_card["target"])
        spaces_to_move = 0
        if target_space > current_space:
            spaces_to_move = target_space - current_space
        else:
            spaces_to_move = board.length - (current_space - target_space)
        board.update_position(player = player, spaces_to_move = spaces_to_move)
        self.card_list.append(self.active_card)
        self.active_card = {}
    
    def payment_card(self, player):
        player.money += self.active_card["amount"]
        self.card_list.append(self.active_card)
        self.active_card = {}
    
    def collection_card(self, active_player, board):
        for player in board.player_list:
            player.money -= self.active_card["amount"]
            active_player += self.active_card["amount"]
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
        if board.layout[board.player_positions[board.player_list.index(player)]].is_owned:
            die1, die2, total = player.roll_dice()



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

chance = Chance("Chance", [
    {"text": 'Advance to "Go". \n(Collect $200)', "type": "movement", "target": "Go"},
    {"text": 'Advance to Illinois Ave.', "type": "movement", "target": illinois_ave},
    {"text": 'Advance to St. Charles Place.', "type": "movement", "target": st_charles_place},
    {"text": 'Advance token to the nearest Utility. \nIf unowned, you may buy it from the Bank. \nIf owned, throw dice and pay owner a total 10 times the amount thrown.', "type": "utility"},
    {"text": 'Advance token to the nearest Railroad and pay the owner Twice the Rental to which they are entitled. \nIf Railroad is UNOWNED you may buy it from the Bank.', "type": "railroad"},
    {"text": 'Advance token to the nearest Railroad and pay the owner Twice the Rental to which they are entitled. \nIf Railroad is UNOWNED you may buy it from the Bank.', "type": "railroad"},
    {"text": 'Go Back 3 Spaces.', "type": "movement", "target": "position - 3"},
    {"text": 'Take a trip to Reading Railroad. \nIf you pass Go, collect $200.', "type": "movement", "target": reading_rr},
    {"text": 'Take a walk on the Boardwalk. \nAdvance token to Boardwalk.', "type": "movement", "target": boardwalk},
    {"text": 'Go to Jail. Go directly to Jail. \nDo not pass GO, do not collect $200.', "type": "jail"},
    {"text": 'Get out of Jail Free. This card may be kept until needed or traded/sold.', "type": "jailbreak", "owner": 0},
    {"text": 'Bank pays you a dividend of $50.', "type": "payment", "amount": 50},
    {"text": 'Your building loan matures. \nCollect $150.', "type": "payment", "amount": 150},
    {"text": 'Pay school tax of $150.', "type": "payment", "amount": -150},
    {"text": 'Make general repairs on all your property: \nFor each house pay $25, \nFor each Hotel $100.', "type": "house", "amount": [25, 100]},
    {"text": 'You have been elected Chairman of the Board. Pay each player $50.', "type": "collection", "amount": -50}
    ])

community_chest = Chance("Community Chest", [
    {"text": 'Advance to "Go". \n(Collect $200)', "type": "movement", "target": "Go"},
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
    {"text": 'Get out of Jail Free. This card may be kept until needed or traded/sold.', "type": "jailbreak"},
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

board = Board(["Go", mediterranean_ave, community_chest, baltic_ave, "Income Tax", reading_rr, oriental_ave, chance, vermont_ave, connecticut_ave, 
        "Jail", st_charles_place, electric_company, states_ave, virginia_ave, pennsylvania_rr, st_james_place, community_chest, tennessee_ave, new_york_ave, 
        "Free Parking", kentucky_ave, chance, indiana_ave, illinois_ave, b_and_o_rr, atlantic_ave, ventnor_ave, water_works, marvin_gardens, 
        "Go To Jail", pacific_ave, north_carolina_ave, community_chest, pennsylvania_ave, short_line_rr, chance, park_place, "Luxury Tax", boardwalk])

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
    
    board.player_list.append(Player(player_choices[0], player_choices[1]))
    board.player_positions.append(0)

first_roll = 0
first_turn = 0

for player in board.player_list:
    player.roll_dice()
    if player.last_roll > first_roll:
        first_turn = player
        first_roll = player.last_roll
while first_turn != board.player_list[0]:
    board.player_list.append(board.player_list.pop(0))
print(f'{board.player_list[0].name} goes first.')
board.player_list[0].is_turn = True

game_active = True

while game_active:
    for player in board.player_list:
        chance.utility_card(player, board)
        turn_count = 0
        player.die1 = 0
        player.die2 = 0
        print(f"{player.name}'s turn! Press enter to roll dice.")
        while (player.die1 == player.die2):
            input()
            roll1, roll2, movement = player.roll_dice()
            turn_count += 1
            if turn_count == 3 and roll1 == roll2:
                print(f"{player.name} rolled doubles three times in a row! {player.name} goes to Jail!")
                board.go_to_jail(player)
                break
            board.update_position(player, roll1, roll2, movement)
            print(f"{player.name} is on space {board.player_positions[board.player_list.index(player)]}")
            if player.die1 == player.die2:
                print(f"{player.name} rolled doubles! Roll again!")
    print(f"Would you like to end the game?")
    choice = str(input()).title()
    while choice != "No":
        if choice == "Yes":
            game_active = False
            break
        print("Please enter Yes or No.")
        choice = str(input()).title()

