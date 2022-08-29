class Observable:
    observers: list

    def __init__(self):
        self.observers = list()

    def attach(self, obs):
        self.observers.append(obs)

    def detach(self, obs):
        self.observers.remove(obs)

    def notify_all(self):
        for obs in self.observers:
            obs.update()


class DisplayObserver:

    def update(self,money):
        print("Introduced money", money)
        pass


class ChoiceObserver:

    def update(self):
        print("Choice made")
        pass
