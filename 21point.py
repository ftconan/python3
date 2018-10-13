# coding=utf-8
"""
@author: magician
@date: 2018/10/13
"""
import time
import sys
import time
import random


class Card:
    """
    card class
    """
    def __init__(self, card_type, card_text, card_value):
        """
        @params: card_type  str   card type 
                 card_text  str   card text
                 card_value int    card number(A: 1 or 11, 10-K: 10)              
        """
        self.card_type = card_type  
        self.card_text = card_text  
        self.card_value = card_value 


class Role:
    """
    Role class
    computer and player (two role)
    """
    def __init__(self):
        # card in role
        self.cards = []

    def show_card(self):
        """
        print role cards
        """
        for card in self.cards:
            # print(card.card_type, card.card_text, sep='', end='')
            print(card.card_type, card.card_text)

    def get_value(self, min_or_max):
        """
        get card number(min or max)
        @params: min_or_max str      min:   A(1)
                                     max:   A(11 or 1)
        @return: value int           card number
        """
        # total points, A number
        sum2, A = 0, 0
        
        for card in self.cards:
            # calc total points
            sum2 += card.card_value
            # calc A number
            if card.card_text == 'A':
                A += 1
        
        if min_or_max == 'max':
            # decrease A number, make value <= 21
            for i in range(A):
               # A(1) number
                value = sum2 - i * 10
                if value <= 21:
                    return value

        # min A(1)
        return sum2 - A * 10

    def burst(self):
        """
        judge number > 21 True: False
        """
        return self.get_value('min') > 21


class CardManager:
    """
    card manager
    52 card
    """
    def __init__(self):
        self.cards = []
        all_card_type = ['heart', 'spade', 'diamond', 'club']
        all_card_text = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        all_card_value = [11, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        # make cards
        for card_type in all_card_type:
            for index, card_text in enumerate(all_card_text):
                card = Card(card_type, card_text, all_card_value[index])
                self.cards.append(card)

        # shuffle card
        random.shuffle(self.cards)

    def send_card(self, role, num=1):
        """
        send card to computer or player
        @params: role Role     computer or player
                 num  int      send card number(1)
        """
        for i in range(num):
            card = self.cards.pop()
            role.cards.append(card)


if __name__ == '__main__':
    # create card
    cards = CardManager()
    # create role
    computer = Role()
    player = Role()
    # send one card to computer, send two card to player
    computer.show_card()
    player.show_card()

    # ask player: do you want a card more?
    while True:
        # choice = input('do you want a card more? [y|n]')
        choice = str(input('do you want a card more?'))
        # want card
        if choice == 'y':
            cards.send_card(player)
            # show card
            computer.show_card()
            player.show_card()
            # burst, else ask player
            if player.burst():
                print('burst, you lose!')
                sys.exit()
        else:
            break

    # player stop card, send card to computer
    while True:
        print('sending card ...')
        time.sleep(1)
        cards.send_card(computer)
        # show card
        computer.show_card()
        player.show_card()
        # burst
        if computer.burst():
            print('computer burst, you win!')
            sys.exit()
        elif computer.get_value('max') >= 17:
            break
        
    # compare card point
    player_value = player.get_value('max')
    computer_value = computer.get_value('max')
    if player_value > computer_value:
        print('you win!')
    elif player_value == computer_value:
        print('draw!')
    else:
        print('you lose!')
