from VendingMachineSTM import VendingMachineSTM
from TakeMoneySTM import TakeMoneySTM
from SelectProductSTM import SelectProductSTM

if __name__ == '__main__':
    take = TakeMoneySTM()
    select = SelectProductSTM()
    machine = VendingMachineSTM(take, select)
    machine.proceed_to_checkout()
