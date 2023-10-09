import random


def generate_draft(players, draft_rounds):
    ordered_players = []
    draft_string = ''
    index = 1

    draft_string += "Pick Order"

    while len(players) > 0:
        choice = random.choice(players)
        ordered_players.append(players.pop(players.index(choice)))
        draft_string += "\n%d. %s" % (index, choice)
        index += 1

    draft_string += "\n\nDraft"
    round_index = 1
    for draft_round in range(1, draft_rounds + 1):
        for draftee in ordered_players:
            draft_string += "\n%2d. %10s: " % (round_index, draftee)
            round_index += 1
        ordered_players.reverse()
    return "```%s```" % draft_string


if __name__ == "__main__":
    print(generate_draft(['ryan', 'adam', 'maher t'], 4))
