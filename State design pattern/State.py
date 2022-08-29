import TakeMoneySTM


class State:
    pass

class WaitingForClient(State):
    state_machine: TakeMoneySTM

    def client_arrived(self):
        return True


class InsertMoney(State):

    def __init__(self, stm: TakeMoneySTM):
        self.state_machine = stm


    def insert_10bani(self):
        self.state_machine.add_money(0.1)

    def insert_50bani(self):
        self.state_machine.add_money(0.5)

    def insert_1leu(self):
        self.state_machine.add_money(1)

    def insert_5lei(self):
        self.state_machine.add_money(5)

    def insert_10lei(self):
        self.state_machine.add_money(10)

class SelectProduct(State):
    price: float

    def __init__(self):
        self.price = 0

    @staticmethod
    def choose(state_machine):
        print("Menu:\n\t1. CocaCola\n\t2. Pepsi\n\t3.Sprite")
        opt = input('Option: ')
        if opt == '1':
            state_machine.current_state = state_machine.coca_cola_state
        if opt == '2':
            state_machine.current_state = state_machine.pepsi_state
        if opt == '3':
            state_machine.current_state = state_machine.sprite_state



class CocaCola(State):
    price: float

    def __init__(self, price):
        self.price = price


class Pepsi(State):
    price: float

    def __init__(self, price):
        self.price = price


class Sprite(State):
    price: float

    def __init__(self, price):
        self.price = price
