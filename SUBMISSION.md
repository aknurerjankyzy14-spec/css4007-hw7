# HW7 submission — Blackjack

## AI-use declaration

I used ChatGPT to understand
the assignment and the PyCharm and Git steps. It helped me calculate the answers for Part A, write the explanations and comparison table, and understand the first method in Part B. It also showed me how to add photos of my handwritten work to the report.

## Setup and reproduction

Record dependency versions, installation steps and exact commands for the
paper replay, training and frozen-policy evaluation.

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

Link scans/photos of all four methods. Commit the original paper work before
implementing learners. Keep originals alongside any corrections.

## Part C — Reproduce the calculations

Link the fixed-history replay output in outputs/paper-replay/.

| Method | State / action | Sweep / pass / update | Paper result | Program result | Difference | Explanation |
| --- | --- | --- | --- | --- | --- | --- |

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
