
class Election:

    def __init__(self):
        self.votes = []
        self.candidates = []

    def init_meta_info(self, number_of_voters, sum_of_vote_count, number_of_unique_orders):
        self.number_of_voters = number_of_voters
        self.sum_of_vote_count = sum_of_vote_count
        self.number_of_unique_orders = number_of_unique_orders

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def add_vote(self, vote):
        self.votes.append(vote)

    def set_num_candidates(self, num_candidates):
        self.num_candidates = num_candidates