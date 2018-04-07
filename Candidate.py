class Candidate:

    def __init__(self, candidate_number, candidate_name):
        self.candidate_number = candidate_number
        self.candidate_name = candidate_name

    def __str__(self):
        return self.candidate_name + " (" + str(self.candidate_number) + ")"