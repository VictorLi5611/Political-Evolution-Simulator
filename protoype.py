import numpy as np

# --- Parameters ---
N_VOTERS = 100        # Number of voters
N_CANDIDATES = 4      # Number of candidates
N_GENERATIONS = 2000    # Election cycles
RESOURCE_POOL = 1000  # Total resources available to each candidate
PUBLIC_GOODS_MUT_STD = 0.05  # Std dev for mutation of alpha (public/private split)
POLICY_MUT_STD = 2    # Std dev for policy mutation
THETA = 15           # Max ideological distance for coalition inclusion
TAU = 0.6             # Risk-seeking threshold
PHI = 0.3             # Safe-seeking threshold

np.random.seed(1234)

# --- Voter Definition ---
class Voter:
    def __init__(self, ideology, risk_type='safe'):
        self.ideology = ideology  # in [0, 100]
        self.risk_type = risk_type # 'safe' or 'risk'

    def utility(self, candidate, coalition_prob, included):
        # Utility: -|p_i - p_c|^2 + public + (private if included)
        policy_loss = -(self.ideology - candidate.policy) ** 2
        public_payoff = candidate.alpha * (RESOURCE_POOL / N_VOTERS)
        private_payoff = (1 - candidate.alpha) * (RESOURCE_POOL / N_VOTERS) if included else 0
        return policy_loss + public_payoff + private_payoff

    def inclusion(self, candidate, coalition_prob):
        # Decide if voter believes they'll be included in coalition
        max_dist = THETA
        threshold = TAU if self.risk_type == 'risk' else PHI
        return abs(self.ideology - candidate.policy) <= max_dist and coalition_prob >= threshold
        # return coalition_prob >= threshold

# --- Candidate Definition ---
class Candidate:
    def __init__(self, policy, alpha):
        self.policy = policy  # Ideological position in [0, 100]
        self.alpha = alpha    # Fraction to public goods [0,1]
        self.supporters = set()
        self.winning_coalition = set()

    def mutate(self, mutate_policy=True):
        # Mutate alpha and optionally policy
        new_alpha = np.clip(self.alpha + np.random.normal(0, PUBLIC_GOODS_MUT_STD), 0, 1)
        new_policy = self.policy + np.random.normal(0, POLICY_MUT_STD) if mutate_policy else self.policy
        new_policy = np.clip(new_policy, 0, 100)
        return Candidate(new_policy, new_alpha)

# --- Simulation Environment ---
class ElectionSim:
    def __init__(self):
        # Randomize voters and candidate pool
        self.voters = [Voter(np.random.uniform(0, 100), risk_type=np.random.choice(['safe', 'risk'])) for _ in range(N_VOTERS)]
        self.candidates = [Candidate(np.random.uniform(0, 100), np.random.uniform(0, 1)) for _ in range(N_CANDIDATES)]

    def run_generation(self, mutate_policy=True):
        # 1. Voters compute utility for each candidate and vote
        ballots = []
        for voter in self.voters:
            utilities = []
            for candidate in self.candidates:
                # Voters estimate probability of inclusion (simple: size of coalition / N)
                coalition_prob = len(candidate.winning_coalition) / N_VOTERS if candidate.winning_coalition else 1/N_VOTERS
                included = voter.inclusion(candidate, coalition_prob)
                utilities.append(voter.utility(candidate, coalition_prob, included))
            chosen = np.argmax(utilities)
            ballots.append(chosen)
        
        # 2. Count support and form winning coalitions
        for idx, candidate in enumerate(self.candidates):
            candidate.supporters = {i for i, b in enumerate(ballots) if b == idx}
            # Form coalition: pick up to a quota (could be majority or some rule)
            coalition_size = int(0.5 * N_VOTERS)
            supporters_list = list(candidate.supporters)
            np.random.shuffle(supporters_list)
            candidate.winning_coalition = set(supporters_list[:coalition_size])

        # 3. Elect winner (largest viable coalition)
        coalition_sizes = [len(c.winning_coalition) for c in self.candidates]
        winner_idx = np.argmax(coalition_sizes)
        winner = self.candidates[winner_idx]

        # 4. Replicate winner, mutate, replace losers
        new_candidates = [winner]
        while len(new_candidates) < N_CANDIDATES:
            new_cand = winner.mutate(mutate_policy=mutate_policy)
            new_candidates.append(new_cand)
        self.candidates = new_candidates

        # Optionally collect statistics here for analysis
        return winner, coalition_sizes

    def run_simulation(self, generations=N_GENERATIONS, mutate_policy=True):
        history = []
        for gen in range(generations):
            winner, coalition_sizes = self.run_generation(mutate_policy=mutate_policy)
            history.append({
                'generation': gen,
                'winner_policy': winner.policy,
                'winner_alpha': winner.alpha,
                'coalition_sizes': coalition_sizes,
            })
        return history

# --- Running the Simulation ---
if __name__ == '__main__':
    sim = ElectionSim()
    results = sim.run_simulation(mutate_policy=True)  # Set to False for fixed policy mode

    # Print results from last generation for quick check
    print(f"Final winner policy: {results[-1]['winner_policy']:.2f}")
    print(f"Final winner alpha (public/private split): {results[-1]['winner_alpha']:.2f}")
    print(f"Final coalition sizes: {results[-1]['coalition_sizes']}")

    # You can plot or export `results` for deeper analysis
    #FOr Winning Policy and Alpha Over Generations Plot the private and public goods allocation

    import matplotlib.pyplot as plt
    policies = [r['winner_policy'] for r in results]
    alphas = [r['winner_alpha'] for r in results]
    generations = [r['generation'] for r in results]
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(generations, policies, label='Winning Policy', color='blue')
    plt.xlabel('Generation')
    plt.ylabel('Policy Position')
    plt.title('Winning Policy Over Generations')
    plt.subplot(1, 2, 2)
    plt.plot(generations, alphas, label='Winning Alpha', color='green')
    plt.xlabel('Generation')
    plt.ylabel('Public Goods Allocation (Alpha)')
    plt.title('Winning Public Goods Allocation Over Generations')
    plt.tight_layout()
    plt.show()
