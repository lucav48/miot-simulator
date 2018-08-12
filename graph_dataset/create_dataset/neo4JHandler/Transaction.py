class Transaction:
    def __init__(self, s, d, dt, con, mes):
        self.source = s
        self.destination = d
        self.timestamp = dt
        self.context = con
        self.message = mes
