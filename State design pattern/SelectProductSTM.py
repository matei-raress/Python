from Observable import Observable
from State import *


class SelectProductSTM(Observable):

    def __init__(self):
        self.select_product_state = SelectProduct()
        self.sprite_state = Sprite(1)
        self.pepsi_state = Pepsi(2)
        self.coca_cola_state = CocaCola(0.5)
        self.current_state = self.select_product_state

    def choose_another_product(self):
        self.select_product_state.choose(self)
        pass
