import Election, Vote, Candidate
import re, sys
import copy

class ElectionSimulator:

    def __init__(self):
        self.data_file = 'voting-rules/ED-00016-00000001.toi'
        # self.data_file = 'test.toi'
        self.file = open(self.data_file, 'r')
        self.election = Election.Election()
        self.parse_file()

    def parse_file(self):
        for idx, line in enumerate(self.file):
            if (idx == 0):
                num_candidates = int(line)
                self.election.set_num_candidates(num_candidates)
            elif (idx > 0 and idx <= num_candidates):
                candidate_data = line.split(',')
                candidate_number = int(candidate_data[0])
                candidate_name = candidate_data[1].strip()
                candidate = Candidate.Candidate(candidate_number, candidate_name)
                self.election.add_candidate(candidate)
            elif (idx == num_candidates + 1):
                meta_election_info = line.split(',')
                number_of_voters = int(meta_election_info[0])
                sum_of_vote_count = int(meta_election_info[1])
                number_of_unique_orders = int(meta_election_info[2])
                self.election.init_meta_info(number_of_voters, sum_of_vote_count, number_of_unique_orders)
            else:
                vote_info = line.split(',', 1)
                count = int(vote_info[0])

                # clean the preferences
                raw_pref_string = vote_info[1].strip()

                if ('{' in raw_pref_string and '}' in raw_pref_string):
                    raw_pref_string = self.remove_indifferent_votes(raw_pref_string)

                preference_list = raw_pref_string.split(',')
                # convert preference string into ints
                preference_list = list(map(int, preference_list))
                vote = Vote.Vote(count, preference_list)
                self.election.add_vote(vote)

    def remove_indifferent_votes(self, raw_pref_string):
        """ remove all voters who expressed any indifferences among ranked candidates (in curly braces) from
         the data
        :param raw_pref_string: the raw preference list string
        :return: the prefernce list string without any indifferent votes
        """
        clean_pref_string = raw_pref_string
        result = re.findall(r".*?(,\{.*?\})", raw_pref_string)
        for group in result:
            clean_pref_string = clean_pref_string.replace(group, "")

        return clean_pref_string

    def run_plurality_vote(self):
        """ A plurality vote describes the circumstance when a candidate or proposition polls
        more votes than any other
        :return;
        """
        print("running plurality vote simulation")
        candidates = copy.copy(self.election.candidates)
        # sum of votes for a candidate (index - 1 =  candidate number
        election_results = [0] * self.election.num_candidates
        for vote in self.election.votes:
            count = vote.count
            preferences = vote.preference_list
            index = preferences[0] - 1
            candidate = candidates[index]
            election_results[index] += count
            # for preference in preferences:
            #     index = preference - 1
            #     candidate = candidates[index]
            #     election_results[index] += count

        max_votes = 0
        winning_candidate = None
        for (idx, candidate_votes) in enumerate(election_results):
            candidate = candidates[idx]
            if (max_votes < candidate_votes):
                max_votes = candidate_votes
                winning_candidate = candidate

            print(candidate, "had", candidate_votes, "votes")

        print(winning_candidate, "won the election with " + str(max_votes) + " votes")

    def run_instant_runoff_voting(self):
        """ Repeatedly eliminating the candidate with the fewest first place votes until one
         has a majority of first place votes
        :return: 
        """
        print("running instant runoff voting simulation")
        candidates = copy.copy(self.election.candidates)
        # sum of votes for a candidate (index - 1 =  candidate number

        for runoff_vote_iteration in range(self.election.num_candidates, 1, -1):

            election_results = [0] * runoff_vote_iteration
            for vote in self.election.votes:
                count = vote.count
                preferences = vote.preference_list

                for preference in preferences:
                    index = preference - 1
                    if 0 <= index < len(candidates):
                        candidate = candidates[index]
                        election_results[index] += count
                        break

            # remove candidate with least 1st place votes
            min_votes = sys.maxsize
            eliminated_candidate = None
            for (idx, candidate_votes) in enumerate(election_results):
                candidate = candidates[idx]
                if (min_votes > candidate_votes):
                    min_votes = candidate_votes
                    eliminated_candidate = candidate

            candidates.remove(eliminated_candidate)
            election_results.remove(min_votes)
            # print(eliminated_candidate, "was eliminated from the election with " + str(min_votes) + " votes")

        print(candidates[0], "won the election with", election_results[0], "votes")
    def run_borda_count(self):
        """ The Borda count is a single-winner election method in which voters rank options or
         candidates in order of preference. The Borda count determines the outcome of a debate
          or the winner of an election by giving each candidate, for each ballot, a number of 
          points corresponding to the number of candidates ranked lower.
          since we have incomplete preference ballots, this implementation gives every unranked 
          candidate 1 point, the points they would normally get for last place.
        :return: 
        """
        print("running borda count simulation")

        candidates = copy.copy(self.election.candidates)
        # borda count for a candidate (index - 1 =  candidate number
        election_results = [0] * self.election.num_candidates
        for vote in self.election.votes:
            count = vote.count
            preferences = vote.preference_list

            all_preferences = set(range(self.election.num_candidates))
            unranked_preferences = all_preferences - set(preferences)
            n = self.election.num_candidates
            for (idx, preference) in enumerate(preferences):
                index = preference - 1
                increment = count * (n - idx)
                election_results[index] += increment
            for unranked_preference in unranked_preferences:
                index = unranked_preference - 1
                election_results[index] += count

        max_votes = 0
        winning_candidate = None
        for (idx, candidate_votes) in enumerate(election_results):
            candidate = candidates[idx]
            if (max_votes < candidate_votes):
                max_votes = candidate_votes
                winning_candidate = candidate

            # print(candidate, "had a borda count of", candidate_votes)

        print(winning_candidate, "won the election with a borda count of", max_votes)

    def run_approval_voting(self):
        """ Where every candidate that shows up on a voter’s preference list gets 1 point and the
         candidate with the maximum number of points wins
        :return: 
        """
        print("running approval rating simulation")

        candidates = copy.copy(self.election.candidates)
        # borda count for a candidate (index - 1 =  candidate number
        election_results = [0] * self.election.num_candidates
        for vote in self.election.votes:
            count = vote.count
            preferences = vote.preference_list

            for (idx, preference) in enumerate(preferences):
                index = preference - 1
                election_results[index] += count

        max_votes = 0
        winning_candidate = None
        for (idx, candidate_votes) in enumerate(election_results):
            candidate = candidates[idx]
            if (max_votes < candidate_votes):
                max_votes = candidate_votes
                winning_candidate = candidate

            # print(candidate, "had",candidate_votes,"votes")

        print(winning_candidate, "won the election by appearing on", max_votes, "ballots")

simulator = ElectionSimulator()
simulator.run_plurality_vote()
simulator.run_instant_runoff_voting()
simulator.run_borda_count()
simulator.run_approval_voting()