"""Replay the supplied Blackjack histories. Run: python paper_replay.py"""
import csv
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "outputs" / "paper-replay"
ACTIONS = ("stick", "hit")
ALPHA = Fraction(1, 10)

# Reference results from Part B. Check them against the handwritten pages.
PAPER_VALUES = dict(A="-1/3", B="0", C="0", D="0", E="0")
PAPER_UPDATES = {
    "TD(0)": "0 .1 -.1 0 0 0 -.08 -.01 -.073 .091 -.1657 0 0 0 -.14003 -.0181",
    "Q-learning": "0 .1 -.1 0 0 0 -.08 -.01 -.072 .091 -.1648 0 0 0 -.13922 -.0181",
}


def read_csv(name):
    with (ROOT / "data" / name).open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def main():
    states = read_csv("states.csv")
    labels = [row["label"] for row in states]
    policy = {row["label"]: int(int(row["player_sum"]) < 20) for row in states}

    games = defaultdict(list)
    for row in read_csv("paper-games.csv"):
        successor = "END" if row["terminated"].lower() == "true" else row["next_state"]
        games[int(row["game"])].append(
            (row["state"], int(row["action"]), successor, int(row["reward"]))
        )

    steps = [step for game in games.values() for step in game]
    log = []
    comparison = []

    def compare(method, entry, stage, paper, value):
        reference = Fraction(paper)
        difference = value - reference
        comparison.append(
            (
                method,
                entry,
                stage,
                reference,
                value,
                difference,
                "Match" if difference == 0 else "Check original calculation",
            )
        )

    # 1. Model-based learning
    counts = Counter()
    reward_sums = Counter()
    visits = Counter()

    for state, action, successor, reward in steps:
        key = (state, action, successor)
        counts[key] += 1
        reward_sums[key] += reward
        visits[state, action] += 1

    model = defaultdict(list)
    log.append("Model: state action next | count/visits | probability | mean reward")

    for (state, action, successor), count in counts.items():
        total = visits[state, action]
        probability = Fraction(count, total)
        mean_reward = Fraction(reward_sums[state, action, successor], count)
        model[state, action].append((successor, probability, mean_reward))
        log.append(
            f"{state} {ACTIONS[action]} {successor} | {count}/{total} | "
            f"{probability} | {mean_reward}"
        )

    for state in labels:
        for action in range(2):
            if not visits[state, action]:
                log.append(f"{state} {ACTIONS[action]}: unobserved")

    values = dict.fromkeys(labels + ["END"], 0)

    for sweep in (1, 2):
        previous = values.copy()
        for state in labels:
            values[state] = sum(
                probability * (reward + previous[successor])
                for successor, probability, reward in model[state, policy[state]]
            )
            compare("Model-based", state, f"sweep {sweep}", PAPER_VALUES[state], values[state])
            log.append(f"Sweep {sweep}: V({state}) = {values[state]}")

    # 2. Every-visit Monte Carlo
    returns = defaultdict(list)

    for game_id, game in games.items():
        total = 0
        for state, action, successor, reward in reversed(game):
            total += reward
            returns[state].append(total)
            log.append(f"MC game {game_id}: return from {state} = {total}")

    for state in labels:
        samples = returns[state]
        average = Fraction(sum(samples), len(samples))
        log.append(f"MC {state}: returns={samples}, visits={len(samples)}, mean={average}")
        compare("Monte Carlo", state, "pass 1", PAPER_VALUES[state], average)

    # 3. TD(0) and 4. Q-learning. Each method starts with a fresh table.
    for method, reference_line in PAPER_UPDATES.items():
        estimates = defaultdict(Fraction)
        references = iter(reference_line.split())
        log.append(f"{method}: pass game.step pair next | old reward continuation target new")

        for replay in (1, 2):
            for game_id, game in games.items():
                for number, (state, action, successor, reward) in enumerate(game, 1):
                    key = state if method == "TD(0)" else (state, action)
                    continuation = 0

                    if successor != "END":
                        if method == "TD(0)":
                            continuation = estimates[successor]
                        else:
                            continuation = max(estimates[successor, a] for a in range(2))

                    old = estimates[key]
                    target = reward + continuation
                    estimates[key] = old + ALPHA * (target - old)

                    stage = f"pass {replay}, game {game_id}, step {number}"
                    pair = state if method == "TD(0)" else f"{state}/{ACTIONS[action]}"
                    log.append(
                        f"{stage} {pair} -> {successor} | "
                        f"{old} {reward} {continuation} {target} {estimates[key]}"
                    )
                    compare(method, pair, stage, next(references), estimates[key])

            for state in labels:
                if method == "TD(0)":
                    log.append(f"Pass {replay}: V({state}) = {estimates[state]}")
                else:
                    stick, hit = (estimates[state, a] for a in range(2))
                    greedy = "tie" if stick == hit else ACTIONS[int(hit > stick)]
                    log.append(
                        f"Pass {replay}: {state} stick={stick}, hit={hit}, greedy={greedy}"
                    )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = "\n".join(log) + "\n"
    print(report, end="")
    (OUTPUT / "replay.txt").write_text(report, encoding="utf-8")

    with (OUTPUT / "comparison.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Method",
                "State/action",
                "Sweep/pass/update",
                "Paper result",
                "Program result",
                "Difference",
                "Explanation",
            ]
        )
        writer.writerows(comparison)

    matches = sum(row[5] == 0 for row in comparison)
    print(f"Matches: {matches}/{len(comparison)}")


if __name__ == "__main__":
    main()