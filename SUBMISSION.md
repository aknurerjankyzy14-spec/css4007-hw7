# HW7 submission — Blackjack

## AI-use declaration

I used ChatGPT to understand the assignment and the PyCharm and Git steps. It helped me work through the calculations in Parts A and B, prepare the tables, and write the explanations in English. It also helped me write the Python scripts for Parts C and D and explain the results from my runs.

## Setup and reproduction
I used Windows PowerShell and Python 3.13.2. Part C uses the Python standard library. Part D uses Gymnasium 1.4.0 and Matplotlib 3.11.2.

Run these commands from the project folder.

```powershell
python -m pip install gymnasium==1.4.0 matplotlib==3.11.2

# Part C: replay the four supplied games
python paper_replay.py

# Part D: collect games and evaluate the fixed policy
11, 22, 33 | ForEach-Object { python collect_games.py --seed $_ }
python evaluate_fixed.py
python compare_states.py

# Part D: train six Q-tables and evaluate the frozen policies
11, 22, 33 | ForEach-Object { python train_q.py --seed $_ --epsilon 0.2 }
11, 22, 33 | ForEach-Object { python train_q.py --seed $_ --epsilon 0 }
python evaluate_policies.py
```

## Part A — Count states and actions

- [Part A — page 1](paper/part-a-01.jpg)
- [Part A — page 2](paper/part-a-02.jpg)
- [Part A — page 3](paper/part-a-03.jpeg)
- [Part A — page 4](paper/part-a-04.jpeg)

### Comparison of states and actions

| Game | Representation | State-count formula | Type of count | Action | Legal actions in the example | Hidden information |
|---|---|---|---|---|---|---|
| Blackjack | Player sum, dealer's visible card, usable ace | 10 × 10 × 2 = 200 | Exact count of observations for sums 12–21 | Hit or stick | 2 | Dealer's hidden card |
| Durak | One player's six-card hand | C(36, 6) = 1,947,792 possible starting hands. C(29, 6) = 475,020 possible opponent hands after 7 cards are known | Each count covers one hand, which is part of the full state | Play one card, pick up, or end the attack | 6 opening moves. Against 10♣ with hearts as trumps: A♣, 7♥, Q♥, or pick up (4 moves) | Opponent's hand and stock order |
| Tic-tac-toe | Nine cells, each empty, X, or O | 3⁹ = 19,683 | Upper bound on legal positions | Place a mark in an empty cell | 5 empty cells. X moves next | None |
| Nim | Three labeled piles, initially (2, 3, 4) | 3 × 4 × 5 = 60 pile configurations. With a player label: 60 × 2 = 120 | Exact count of pile configurations. The 120 encodings include unreachable states | Choose a pile and how many stones to remove | 9 at (2,3,4), 3 at (0,1,2), and 0 at (0,0,0) | None |

Durak would need a very large Q-table. One player alone can have 1,947,792 different starting hands. The cards on the table and the phase of the game also affect the choice of action.

The number of legal actions depends on the position. For example, tic-tac-toe has 9 action labels, one for each cell. Only 5 cells are free on the given board.

## Part B — Paper calculations
I used the four games from `data/paper-games.csv`. I did two model-based sweeps, one Monte Carlo pass, and two passes each for TD(0) and Q-learning. I kept the values from the first pass when I started the second pass.

For state A, model-based learning and Monte Carlo both gave V(A) = −1/3. After two passes, TD(0) gave V(A) = −0.14003, and Q-learning gave Q(A, hit) = −0.13922. The photos below show my calculations step by step.

- [Part B — page 1](paper/part-b-01.jpeg)
- [Part B — page 2](paper/part-b-02.jpeg)
- [Part B — page 3](paper/part-b-03.jpeg)
- [Part B — page 4](paper/part-b-04.jpeg)
- [Part B — page 5](paper/part-b-05.jpeg)
- [Part B — page 6](paper/part-b-06.jpeg)
- [Part B — page 7](paper/part-b-07.jpeg)

## Part C — Reproduce the calculations

I ran `python paper_replay.py` on the four games from `data/paper-games.csv`.
All 47 checks matched the Part B reference values used in the script.

- [Full output for all four methods](outputs/paper-replay/replay.txt)
- [Full comparison table with all 47 checks](outputs/paper-replay/comparison.csv)

| Method | State / action | Sweep / pass / update | Paper result | Program result | Difference | Explanation |
|---|---|---|---:|---:|---:|---|
| Model-based | A | Sweep 2 | -1/3 | -1/3 | 0 | One of the three hits from A ended in a loss. The other two led to B, where the mean reward was 0. |
| Monte Carlo | A | Pass 1 | -1/3 | -1/3 | 0 | The returns were +1, -1 and -1. Their mean was -1/3. |
| TD(0) | A | Pass 2, game 4, step 1 | -0.14003 | -14003/100000 | 0 | The update used V(B) = 0.091. |
| Q-learning | A / hit | Pass 2, game 4, step 1 | -0.13922 | -6961/50000 | 0 | The update used the higher Q-value in B, which was 0.091. |

## Part D — Simulated games

### Fixed-policy value estimates

I used three training seeds: 11, 22 and 33. For each seed, Model-based, Monte Carlo and TD(0) used the same saved games in the same order. I checked the values after 100, 1,000 and 10,000 games. All nine model evaluations converged. All 30,000 games finished with no cut-offs.

- [Game logs for seeds 11, 22 and 33](outputs/fixed-policy/)
- [Value tables and visit counts, with and without a usable ace](outputs/fixed-policy/estimates/)
- [Checkpoint summary](outputs/fixed-policy/estimates/summary.csv)
- [Frequent and rare states at all three checkpoints](outputs/fixed-policy/estimates/frequent_rare_comparison.csv)

The table shows examples from seed 11. Values are rounded to three decimal places.

| Player sum | Dealer card | Usable ace | Games | Visits | Model-based | Monte Carlo | TD(0) |
|---:|---:|---|---:|---:|---:|---:|---:|
| 20 | 10 | No | 100 | 6 | 0.333 | 0.333 | 0.173 |
| 20 | 10 | No | 1,000 | 60 | 0.467 | 0.467 | 0.511 |
| 20 | 10 | No | 10,000 | 606 | 0.416 | 0.416 | 0.439 |
| 4 | 6 | No | 1,000 | 1 | -0.620 | -1.000 | 0.000 |
| 4 | 6 | No | 10,000 | 1 | -0.693 | -1.000 | 0.000 |
| 21 | 10 | Yes | 10,000 | 190 | 0.921 | 0.921 | 0.980 |
| 12 | 4 | Yes | 10,000 | 1 | -0.666 | -1.000 | -0.074 |

**Frequent states.** With 20 points, a dealer 10 and no usable ace, the player always sticks. The game ends on that step. Model-based and Monte Carlo therefore use the same final rewards and give the same mean. After 10,000 games, this mean was 0.416 for seed 11, 0.417 for seed 22 and 0.455 for seed 33. TD(0) gives more weight to recent results because its learning rate stays at 0.1. For seed 22, its final estimate was 0.094 even after 633 visits.

**Rare states.** With seed 11, the player visited (4, 6, no usable ace) only once and later lost that game. Monte Carlo recorded -1. TD(0) stayed at 0 because its update used the next state's value at the time of that visit. The model-based estimate changed from -0.620 to -0.693 as the model learned more about later states.

**Missing values.** When a state had zero visits, I left its estimates blank. For seed 11, the state (12, 4, usable ace) had zero visits after 1,000 games and one visit after 10,000 games. Every game finished, so each nonterminal next state appeared in the next step of the same game. No observed state needed a missing next-state value. All three seeds reached all 280 states after 10,000 games, but some states had only one or two visits.

### Q-learning and baseline evaluation

I tested each policy on 10,000 new games per evaluation seed. The baseline used the rule “hit below 20, stick at 20 or 21.” The two learned policies used frozen Q-tables. During evaluation, they chose the action with the higher Q-value and broke ties randomly. Epsilon in the table is the value used during training.

| Training seed | Policy / training epsilon | Evaluation seed | Wins | Losses | Draws | Cut-offs | Mean reward |
|---:|---|---:|---:|---:|---:|---:|---:|
| 11 | Baseline | 1011 | 2962 | 6462 | 576 | 0 | -0.3500 |
| 11 | Q-learning, 0.2 | 1011 | 4228 | 4882 | 890 | 0 | -0.0654 |
| 11 | Q-learning, 0 | 1011 | 4100 | 4929 | 971 | 0 | -0.0829 |
| 22 | Baseline | 1022 | 2935 | 6481 | 584 | 0 | -0.3546 |
| 22 | Q-learning, 0.2 | 1022 | 4220 | 4919 | 861 | 0 | -0.0699 |
| 22 | Q-learning, 0 | 1022 | 4100 | 4975 | 925 | 0 | -0.0875 |
| 33 | Baseline | 1033 | 2950 | 6496 | 554 | 0 | -0.3546 |
| 33 | Q-learning, 0.2 | 1033 | 4124 | 5025 | 851 | 0 | -0.0901 |
| 33 | Q-learning, 0 | 1033 | 4098 | 4943 | 959 | 0 | -0.0845 |

[Full evaluation results](outputs/evaluation/policy_evaluation.csv)

### Plots and learned policies

Each training run lasted 50,000 games. Each point on a training curve shows the mean reward over 1,000 games. The evaluation table above uses new games played after training.

| Training seed | Epsilon 0.2 | Epsilon 0 |
|---:|---|---|
| 11 | [Training curve](outputs/q-learning/seed_11_eps_0.2/training_curve.png) | [Training curve](outputs/q-learning/seed_11_eps_0/training_curve.png) |
| 22 | [Training curve](outputs/q-learning/seed_22_eps_0.2/training_curve.png) | [Training curve](outputs/q-learning/seed_22_eps_0/training_curve.png) |
| 33 | [Training curve](outputs/q-learning/seed_33_eps_0.2/training_curve.png) | [Training curve](outputs/q-learning/seed_33_eps_0/training_curve.png) |

Each Q-table includes the values for hit and stick, the number of times each action was tried, and the greedy action. A visit count of zero means the action was never tried in that state.

- [Example Q-table without a usable ace](outputs/q-learning/seed_11_eps_0.2/q_table_ace_0.csv)
- [Example Q-table with a usable ace](outputs/q-learning/seed_11_eps_0.2/q_table_ace_1.csv)
- [Tables, visit counts and curves for all six runs](outputs/q-learning/)

### Explain your results

**Did Q-learning improve the result?** Yes. Across the three evaluation seeds, the baseline had a mean reward of -0.3531. Q-learning reached -0.0751 with epsilon 0.2 and -0.0850 with epsilon 0. Both learned policies improved on the baseline for every seed. All three policies still lost more games than they won.

**Did exploration help?** Training with epsilon 0.2 gave the higher evaluation reward for seeds 11 and 22. For seed 33, epsilon 0 gave the higher reward: -0.0845 compared with -0.0901. Trying random actions during training gave the learner more chances to compare hit and stick. The results varied across seeds.

**What did the methods learn?** Model-based learning estimated transition probabilities and rewards. Monte Carlo averaged the returns from completed games. TD(0) updated a state's value after each step. These three methods evaluated the same fixed policy. Q-learning estimated a separate value for each action and used those values to choose a policy.

**Why do terminal states and usable aces matter?** When a game ends, the update uses only the final reward because there are no more moves. A usable ace changes what can happen after a hit. For example, drawing a ten at 17 with a usable ace leaves the player at 17. Drawing a ten at 17 without a usable ace ends the game with a loss. The agent keeps separate values for these two situations.

All 300,000 Q-learning training games and all 90,000 evaluation games finished without a cut-off. No games were excluded.


