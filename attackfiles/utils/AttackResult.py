# A class to store the result of an attack


class AttackResult:
    def __init__(self, attack, context, result, details):
        self.attack = attack
        self.context = context
        self.result = result
        self.details = details

    def __str__(self):
        return '{} {} {} {}'.format(str(self.attack), str(self.context), str(self.result), str(self.details))


