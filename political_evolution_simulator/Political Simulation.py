import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# --- Parameters ---
N_VOTERS               = 100
N_CANDIDATES           = 4
MAX_GENERATIONS        = 200
RESOURCE_POOL          = 1000
PUBLIC_GOODS_MUT_STD   = 0.05
POLICY_MUT_STD         = 2
THETA                  = 15
TAU                    = 0.6
PHI                    = 0.3
WINNING_COALITION_SIZE = 25
RATIO_OF_VOTERS        = 0.5

np.random.seed(1234)

# --- Voter Definition ---
class Voter:
    def __init__(self, ideology, risk_type='safe'):
        self.ideology  = ideology
        self.risk_type = risk_type
        self.included  = [False] * N_CANDIDATES

    def utility(self, cand_ideo, cand_alpha, cid):
        pay_ideo    = (self.ideology - cand_ideo)**2
        pay_public  = cand_alpha * (RESOURCE_POOL / N_VOTERS)
        pay_private = ((1 - cand_alpha) * (RESOURCE_POOL / WINNING_COALITION_SIZE)
                       if self.included[cid] else 0)
        return pay_ideo + pay_public + pay_private

    def inclusion(self, cid, coal_prob, cand_ideo):
        dist   = abs(self.ideology - cand_ideo)
        thresh = TAU if self.risk_type == 'risk' else PHI
        self.included[cid] = (dist <= THETA and coal_prob >= thresh)
        return self.included[cid]

# --- Candidate Definition ---
class Candidate:
    def __init__(self, ideology, alpha):
        self.ideology = ideology
        self.alpha    = alpha

    def mutate(self, mutate_ideology=True):
        new_alpha = np.clip(
            self.alpha + np.random.normal(0, PUBLIC_GOODS_MUT_STD), 0, 1
        )
        new_ideo  = (
            self.ideology + np.random.normal(0, POLICY_MUT_STD)
            if mutate_ideology else self.ideology
        )
        new_ideo  = np.clip(new_ideo, -100, 100)
        return Candidate(new_ideo, new_alpha)

# --- Detailed Simulator ---
class DetailedElectionSim:
    def __init__(self):
        # initialize voters
        n_safe = int(N_VOTERS * RATIO_OF_VOTERS)
        types  = ['safe'] * n_safe + ['risk'] * (N_VOTERS - n_safe)
        self.voters = [
            Voter(np.random.uniform(0, 100), types[i]) for i in range(N_VOTERS)
        ]
        # initialize candidates
        self.candidates = [
            Candidate(np.random.uniform(0, 100), np.random.uniform(0, 1))
            for _ in range(N_CANDIDATES)
        ]

    def run_generation_detailed(self):
        ballots   = []
        vote_info = []

        # collect utilities & inclusion per voter
        for vid, v in enumerate(self.voters):
            v.included = [False] * N_CANDIDATES  # reset
            utils = []
            for cid, c in enumerate(self.candidates):
                coal_prob = WINNING_COALITION_SIZE / N_VOTERS
                _ = v.inclusion(cid, coal_prob, c.ideology)
                utils.append(v.utility(c.ideology, c.alpha, cid))
            choice = int(np.argmax(utils))
            ballots.append(choice)
            vote_info.append({
                'voter_id': vid,
                'risk_type': v.risk_type,
                'utilities': utils,
                'included': v.included.copy(),
                'ballot': choice
            })

        # tally votes and mutate losers
        counts     = np.bincount(ballots, minlength=N_CANDIDATES).tolist()
        winner_idx = int(np.argmax(counts))
        for cid in range(N_CANDIDATES):
            if cid != winner_idx:
                self.candidates[cid] = self.candidates[winner_idx].mutate()

        return vote_info, counts, winner_idx

    def run_simulation_detailed(self):
        vote_records     = []
        election_summary = []
        candidate_records = []

        for gen in range(MAX_GENERATIONS):
            vote_info, counts, winner = self.run_generation_detailed()

            # record candidate state for plotting
            for cid, c in enumerate(self.candidates):
                candidate_records.append({
                    'generation': gen,
                    'candidate_id': cid,
                    'ideology': c.ideology,
                    'alpha': c.alpha,
                    'is_winner': (cid == winner)
                })

            # record summary
            election_summary.append({
                'generation': gen,
                'vote_counts': counts,
                'winner_idx': winner
            })

            # record per-voter data
            for info in vote_info:
                rec = {
                    'generation': gen,
                    'voter_id': info['voter_id'],
                    'risk_type': info['risk_type'],
                    'voted_for': info['ballot'],
                    'voter_ideology': self.voters[info['voter_id']].ideology,
                    'vote_counts': counts,
                    'winner_idx': winner
                }
                for cid, c in enumerate(self.candidates):
                    rec[f'cand{cid}_ideology'] = c.ideology
                    rec[f'cand{cid}_alpha']    = c.alpha
                    rec[f'cand{cid}_included'] = info['included'][cid]
                    rec[f'cand{cid}_utility']  = info['utilities'][cid]
                vote_records.append(rec)

        # build DataFrames
        df_votes      = pd.DataFrame(vote_records)
        df_summary    = pd.DataFrame(election_summary)
        df_candidates = pd.DataFrame(candidate_records)

        return df_votes, df_summary, df_candidates

# --- Run & Export ---
sim = DetailedElectionSim()
df_votes, df_summary, df_candidates = sim.run_simulation_detailed()

# Preview data
# tools.display_dataframe_to_user("Vote Data Sample", df_votes.head())
# tools.display_dataframe_to_user("Election Summary Sample", df_summary.head())
# tools.display_dataframe_to_user("Candidate Trajectory Sample", df_candidates.head())

# Export CSVs
df_votes.to_csv("vote_data.csv", index=False)
df_summary.to_csv("election_summary.csv", index=False)
df_candidates.to_csv("candidate_trajectory.csv", index=False)
print("Exported vote_data.csv, election_summary.csv, candidate_trajectory.csv")

# --- Plots ---
losers  = df_candidates[df_candidates['is_winner'] == False]
winners = df_candidates[df_candidates['is_winner'] == True]
colors = ['blue', 'yellow', 'green', 'purple']

# Ideology plot
plt.figure(figsize=(10, 6))
plt.scatter(losers['generation'], losers['ideology'],
            color='gray', alpha=0.4, s=10, label='Losers')
for idx, col in enumerate(colors):
    sub = winners[winners['candidate_id'] == idx]
    plt.scatter(sub['generation'], sub['ideology'],
                color=col, alpha=0.9, s=20, label=f'Winner Cand {idx+1}')
plt.xlabel('Generation')
plt.ylabel('Ideology')
plt.title('Candidate Ideologies Across Generations')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Alpha plot
plt.figure(figsize=(10, 6))
plt.scatter(losers['generation'], losers['alpha'],
            color='gray', alpha=0.4, s=10, label='Losers')
for idx, col in enumerate(colors):
    sub = winners[winners['candidate_id'] == idx]
    plt.scatter(sub['generation'], sub['alpha'],
                color=col, alpha=0.9, s=20, label=f'Winner Cand {idx+1}')
plt.xlabel('Generation')
plt.ylabel('Alpha (Public Goods Allocation)')
plt.title('Candidate Alpha Across Generations')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

