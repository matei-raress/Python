from Observable import ChoiceObserver


class VendingMachineSTM:

    def __init__(self, take, select):
        self.take_money_stm = take
        self.select_product_stm = select

    def proceed_to_checkout(self):
            obs=ChoiceObserver()
            money = False
            while not money:
                opt = float(input("Introduce money(0.1,0.5,1,5,10):"))
                if opt == 0.1:
                    self.take_money_stm.insert_money_state.insert_10bani()
                elif opt == 0.5:
                    self.take_money_stm.insert_money_state.insert_50bani()
                elif opt == 1:
                    self.take_money_stm.insert_money_state.insert_1leu()
                elif opt == 5:
                    self.take_money_stm.insert_money_state.insert_5lei()
                elif opt == 10:
                    self.take_money_stm.insert_money_state.insert_10lei()

                self.select_product_stm.choose_another_product()
                obs.update()

                if self.select_product_stm.current_state.price == self.take_money_stm.money:
                    print("You can take your order :")

                if self.select_product_stm.current_state.price < self.take_money_stm.money:
                    pur = input("Do you want to continue the purchase ? ")

                    if pur == "no" or pur == "NO" or pur == "No":
                        rest = int(self.take_money_stm.money - self.select_product_stm.current_state.price)
                        self.take_money_stm.update_amount_of_money(rest) 
                        print("Rest: ", rest)
                        money = True

                else:
                    print("Not enough money for this command ")


