from Observable import DisplayObserver, Observable
from State import WaitingForClient, InsertMoney, State


class TakeMoneySTM(Observable):
    wait_state: WaitingForClient
    insert_money_state: InsertMoney
    current_state: State
    money: float

    def __init__(self):
        self.obs=DisplayObserver()
        self.money = 0
        self.wait_state = WaitingForClient()
        self.insert_money_state = InsertMoney(self)
        self.current_state = self.wait_state
        obs = DisplayObserver()
        super().__init__()
        self.attach(obs)


    def notify_all(self, money):
        for obs in self.observers:
            obs.update(money)

    def add_money(self, value):
        if self.wait_state:
            self.money += value
            self.notify_all(self.money)


    def update_amount_of_money(self, value):
        self.money = value



