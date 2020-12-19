import os
import re
import argparse
import Parse
from Results import Results
from treys import Card, Evaluator
from itertools import combinations

CARDS = [
    '2c','2d','2h','2s',
    '3c','3d','3h','3s',
    '4c','4d','4h','4s',
    '5c','5d','5h','5s',
    '6c','6d','6h','6s',
    '7c','7d','7h','7s',
    '8c','8d','8h','8s',
    '9c','9d','9h','9s',
    'Tc','Td','Th','Ts',
    'Jc','Jd','Jh','Js',
    'Qc','Qd','Qh','Qs',
    'Kc','Kd','Kh','Ks',
    'Ac','Ad','Ah','As',
]

# Helper function for counting hole cards
## hole_cards: tuple, pair of hole cards
## frequency_dict: dict, dict for counting cards
def count_hole_cards_frequency(hole_cards, frequency_dict):
    k = ' '.join(hole_cards)
    # If key doesn't exist, then must be in opposite order
    if k not in frequency_dict:
        k = ' '.join(hole_cards[::-1]) # Reverse order of cards in key
    frequency_dict[k] += 1
# Helper function for counting hands
## hole_cards: list of strs, 2 card hand
## board: list of strs, 3-5 cards
## evaluator: treys.Evaluator
## hand_frequency: dict, count hand frequency
def count_hand_frequency(hole_cards, board, evaluator, hand_frequency):
    # Evaluate hand for rank
    hand_rank = evaluator.class_to_string(
    evaluator.get_rank_class(
            evaluator.evaluate(
                [Card.new(x) for x in hole_cards],
                [Card.new(x) for x in board]
            )
        )
    ).lower()
    hand_frequency[hand_rank] += 1

def main():
    # Argparse
    argparser = argparse.ArgumentParser(description="This script takes a user's poker hand history and calculates proportions of card draws and hands compared to the expected values, their confidence intervals, and chi-square p-values to determine if the site's RNG is behaving as expected.")
    argparser.add_argument('path', type=str, help='Path to hand history directory')
    argparser.add_argument('--site', choices=['Bovada'], default='Bovada', type=str,
    help='Which site\'s hand history is being parsed. Default=Bovada')
    argparser.add_argument('--summaryonly', action='store_true', help='Show summary only, no tables.')
    argparser.add_argument('--stdev', choices=[1,2,3], default=2, type=int,
    help='Stdev for confidence limit, so 1 for 68%%, 2 for 95%%, and 3 for 99.7%%. Default=2')
    argparser.add_argument('--onlyme', action='store_true', help='Only count my hands')
    argparser.add_argument('--holecards', action='store_true', help='Show results for frequency of hole cards without suits')
    argparser.add_argument('--holecardswithsuits', action='store_true', help='Show results for frequency of hole cards with suits (Long output)')
    argparser.add_argument('--allcombinations', action='store_true', help='Show results for frequency of all combinations between hole and board cards.')
    args = argparser.parse_args()

    # Determine correct parser
    if args.site == 'Bovada':
        Parser = Parse.Bovada

    hand_probabilites = Parse.HAND_PROBABILITIES
    card_frequency = {x: 0 for x in CARDS}
    hand_frequency = {x: 0 for x in hand_probabilites.keys()}
    if args.allcombinations:
        hand_allcombinations_frequency = {x: 0 for x in hand_probabilites.keys()}
    if args.holecardswithsuits:
        hole_card_frequency = {' '.join(x): 0 for x in combinations(CARDS, 2)}
    if args.holecards:
        hole_card_nosuits_frequency = {' '.join(x): 0 for x in combinations([c[0] for c in CARDS], 2)} # Remove suit from cards

    # Treys evaluator
    evaluator = Evaluator()

    for file in os.listdir(args.path):
        # Only open .txt files
        if not file.lower().endswith('.txt'):
            continue

        # Open file with parser
        b = Parser('{}\{}'.format(args.path, file))

        while True:
            # Get hole cards
            hole_cards = b.get_hole_cards(only_me=args.onlyme)
            if not hole_cards:
                break # EOF

            # Count card frequency of hole cards
            for c_1, c_2 in hole_cards:
                # Individual card frequency
                card_frequency[c_1] += 1
                card_frequency[c_2] += 1
                # Frequency of hole cards together
                if args.holecardswithsuits:
                    count_hole_cards_frequency((c_1,c_2), hole_card_frequency)
                if args.holecards:
                    count_hole_cards_frequency([x[0] for x in (c_1,c_2)], hole_card_nosuits_frequency)

            # Get board cards
            board = b.get_board_cards()
            if not board:
                continue

            # Count frequency of individual board cards
            for c in board:
                card_frequency[c] += 1

            # Count hand frequencies
            for hc in hole_cards:
                # Hand frequency of hole cards with board
                count_hand_frequency(hc, board, evaluator, hand_frequency)

                # Hand frequency of all combinations of hole cards with board
                if args.allcombinations:
                    for hand in combinations(list(hc)+board, 5):
                        count_hand_frequency(hand[:2], hand[2:], evaluator, hand_allcombinations_frequency)

    summary = [] # List of strs of result summaries
    test_results = [] # List of bool of pass/fail test results

    results = Results(summary_only=args.summaryonly)

    # Print all results
    results.calculate_and_print_results(
        'Distribution of Hands',
        'Hand',
        hand_probabilites,
        hand_frequency,
        summary,
        test_results,
        std_dev=args.stdev,
    )
    if args.allcombinations:
        results.calculate_and_print_results(
            'Distribution of All Hand Combinations',
            'Hand',
            hand_probabilites,
            hand_allcombinations_frequency,
            summary,
            test_results,
            std_dev=args.stdev,
        )
    results.calculate_and_print_results(
        'Distribution of Cards',
        'Card',
        {x: 1/len(CARDS) for x in CARDS},
        card_frequency,
        summary,
        test_results,
        std_dev=args.stdev,
        is_normal=False
    )
    if args.holecardswithsuits:
        hole_card_combinations = [' '.join(x) for x in combinations(CARDS, 2)]
        hole_card_expected_frequency = {x: hole_card_combinations.count(x) / len(hole_card_combinations) for x in hole_card_combinations}

        results.calculate_and_print_results(
            'Distribution of Hole Cards with suits',
            'Hole Cards',
            hole_card_expected_frequency,
            hole_card_frequency,
            summary,
            test_results,
            std_dev=args.stdev,
            is_normal=False,
        )
    if args.holecards:
        hole_card_nosuit_combinations = [' '.join((x[0], y[0])) for x, y in combinations(CARDS, 2)]
        hole_card_nosuits_expected_frequency = {x: hole_card_nosuit_combinations.count(x) / len(hole_card_nosuit_combinations) for x in hole_card_nosuit_combinations}

        results.calculate_and_print_results(
            'Distribution of Hole Cards without suits',
            'Hole Cards',
            hole_card_nosuits_expected_frequency,
            hole_card_nosuits_frequency,
            summary,
            test_results,
            std_dev=args.stdev,
            is_normal=False,
        )

    results.print_summary(summary, test_results)

if __name__ == '__main__':
    main()
