import os
from pprint import pprint

import numpy as np
import requests

SESSION = os.environ.get("AOC_SESSION")


def main():
    """score the board"""
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--score", type=str, default="weighted")
    parser.add_argument("--names", type=str, default="all")
    args = parser.parse_args()

    url = "http://www.adventofcode.com/2022/leaderboard/private/view/191458.json"
    page = requests.get(url, cookies={"session": SESSION})
    print(page)
    print(page.text)
    scores = page.json()
    members = list(scores["members"])
    names = {scores["members"][m]["name"]: m for m in members}

    def get_day_for_name(day, name):
        return scores["members"][names[name]]["completion_day_level"].get(str(day))

    def get_star_time(day, part, name):
        try:
            return get_day_for_name(day, name)[str(part)]["get_star_ts"]
        except (KeyError, TypeError):
            return None

    name_list = list(names)
    if args.names == "finished":
        not_finished = set()
        for name in name_list:
            for day in range(1, 26):
                for part in range(1, 3):
                    if not get_star_time(day, part, name):
                        not_finished.add(name)
        for name in not_finished:
            name_list.remove(name)

    points = {name: 0 for name in name_list}
    for day in range(1, 26):
        for part in range(1, 3):
            times = []
            for name in name_list:
                times.append(get_star_time(day, part, name))
            order = list(reversed(sorted(range(len(times)), key=lambda k: times[k] if times[k] else 1e20)))
            for score, idx in enumerate(order, start=1):
                if times[idx]:
                    if args.score == "weighted":
                        # Scaled by ~ Day 25 = 1.5x and Part 2 = 1.7x
                        points[name_list[idx]] += score * day ** 0.25 * part ** 0.5
                    elif args.score == "local":
                        points[name_list[idx]] += score
                    # points[name_list[idx]] += score * np.sqrt(day)
                    # points[name_list[idx]] += score * np.sqrt(day) * part
                    # points[name_list[idx]] += score * day ** 0.25
                    # points[name_list[idx]] += score * part

    for name in points:
        points[name] = int(points[name])

    order = list(reversed(sorted(range(len(name_list)), key=lambda k: points[name_list[k]])))
    for rank, idx in enumerate(order, start=1):
        print("%02d: %16s\t%04d" % (rank, name_list[idx], points[name_list[idx]]))


if __name__ == "__main__":
    main()
