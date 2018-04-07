class Vote:

    def __init__(self, count, preference_list):
        self.count = count
        self.preference_list = preference_list

    # used for borda count when ballot has indifference
    def set_weak_prefences(self, preferences):
        self.set_weak_prefence_list = preferences

    def __str__(self):
        return "Count: " + str(self.count) + " preference list: " + str(self.preference_list)