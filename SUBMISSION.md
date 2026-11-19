# HW7 submission — Blackjack

## AI-use declaration

I used ChatGPT to understand
the assignment and the PyCharm and Git steps. It helped me calculate the answers for Part A, write the explanations and comparison table, and understand the first method in Part B. It also showed me how to add photos of my handwritten work to the report.

## Setup and reproduction

- Python version: 3.13.2
- Part C uses only the Python standard library. No extra packages are needed.
- To reproduce Part C, run `python paper_replay.py` from the project folder.
- Results are saved in `outputs/paper-replay/replay.txt` and `outputs/paper-replay/comparison.csv`.

## Part A — Count states and actions

- [Part A — page 1](paper/part-a-01.jpg)
- [Part A — page 2](paper/part-a-02.jpg)
- [Part A — page 3](paper/part-a-03.jpeg)
- [Part A — page 4](paper/part-a-04.jpeg)

- ### Comparison of states and actions

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

Link the shared logs, checkpoint value tables and visit counts. Explain
missing states and differences among model-based, Monte Carlo and TD estimates.

### Q-learning and baseline evaluation

| Training seed | Policy / epsilon | Evaluation seed | Wins | Losses | Draws | Cut-offs | Mean reward |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Plots and learned policies

Link training curves, Q-tables, hit/stick policy tables and state-action counts.
Separate usable-ace and no-usable-ace results.

### Explain your results

Address prediction versus control, terminal updates, usable aces, exploration,
coverage, variation across seeds and whether the learned policy improved.
