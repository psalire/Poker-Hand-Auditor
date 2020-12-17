import os
import re
import argparse
import Parse
from treys import Card, Evaluator
from itertools import combinations
# from scipy.stats import chisquare
from math import sqrt

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

# Print table of results
## title: str, title of the table
## label: str, label of the first column
## expected: dict, expected values
## sample: dict, sampled values
## std_dev: int 1,2,3, std_dev for use in confidence limit
## label_column_size: width of first column
## value_column_size: width of other columns
## columns: number of columns to read from parameters expected and sample
def print_results(title, label, expected, sample, std_dev=2, label_column_size=18, value_column_size=12, columns=5):
    full_width = label_column_size + value_column_size*columns + columns*3
    horizontal_divider = ('{:-^%d}' % full_width).format('')

    # Format string based on number and size of columns
    label_column = '{:^%d} | '%label_column_size
    sample_size_column = '{:^%d}'%value_column_size
    results_row = label_column + ''.join(['{:^%d} | '%value_column_size for _ in range(columns-1)]) + sample_size_column
    totals_row = label_column + ''.join(['{:^%df} | '%value_column_size for _ in range(columns-1)]) + sample_size_column
    column_value = '{:^%df}' % (value_column_size)

    sample_size = sum(sample.values())
    confidence_limit = ['68', '95', '99.7'][std_dev-1]
    z_value = {'68': 1, '95': 1.96, '99.7': 2.97}

    print(horizontal_divider)
    print(('{:^%d}' % full_width).format('{}, {}% Confidence Limit, n={}'.format(title, confidence_limit, sample_size)))
    print(horizontal_divider)
    print(results_row.format(label, 'Expected', 'Sample', 'Lower', 'Upper', 'Size'))
    print(horizontal_divider)
    sums = [0 for _ in range(5)]
    for key in sample:
        sample_percentage = sample[key]/sample_size
        # e.append(sample_percentage)
        # z.append(expected[key])

        # Calculate standard error
        ## can't divide by zero
        if sample[key] != 0:
            standard_error = z_value[confidence_limit]*sqrt((expected[key] * (1-expected[key])) / sample[key])
            lower_percentage = expected[key] - std_dev*standard_error
            upper_percentage = expected[key] + std_dev*standard_error
        else:
            standard_error = None
            lower_percentage = None
            upper_percentage = None

        print(results_row.format(
                key,
                column_value.format(expected[key]),
                *(
                    # If value is None, do str(None), else print the float value
                    (column_value.format(x) if x != None else str(x)
                        for x in [sample_percentage, lower_percentage, upper_percentage])
                ),
                sample[key],
            )
        )
        sums[0] += expected[key]
        if standard_error:
            sums[1] += sample_percentage
            sums[2] += lower_percentage
            sums[3] += upper_percentage
        sums[4] += sample[key]
    print(horizontal_divider)
    print(totals_row.format('Sum', *(sum for sum in sums)))
    assert sample_size == sums[4] # Sanity check for sample size

# Helper function for counting hole cards
## hole_cards: tuple, pair of hole cards
## frequency_dict: dict, dict for counting cards
def count_hole_cards_frequency(hole_cards, frequency_dict):
    k = ' '.join(hole_cards)
    # If key doesn't exist, then must be in opposite order
    if k not in frequency_dict:
        k = ' '.join(hole_cards[::-1]) # Reverse order of cards in key
    frequency_dict[k] += 1

def main():
    # Argparse
    argparser = argparse.ArgumentParser(description='Poker Hand Auditor')
    argparser.add_argument('path', type=str, help='Path to hand history directory')
    argparser.add_argument('--onlyme', action='store_true', help='Only count my hands')
    argparser.add_argument('--holecards', action='store_true', help='Show table for frequency of hole cards with suits (Long output)')
    argparser.add_argument('--holecardsnosuits', action='store_true', help='Show table for frequency of hole cards without suits')
    argparser.add_argument('--stdev', choices=[1,2,3], default=2, type=int,
                            help='Stdev for confidence limit, so 1 for 68%%, 2 for 95%%, and 3 for 99.7%%. Default=2')
    argparser.add_argument('--site', choices=['Bovada'], default='Bovada', type=str,
                            help='Which site\'s hand history is being parsed. Default=Bovada')
    args = argparser.parse_args()

    # Determine correct parser
    if args.site == 'Bovada':
        Parser = Parse.Bovada

    hand_probabilites = Parse.HAND_PROBABILITIES
    card_frequency = {x: 0 for x in CARDS}
    hand_frequency = {x: 0 for x in hand_probabilites.keys()}
    if args.holecards:
        hole_card_frequency = {' '.join(x): 0 for x in combinations(CARDS, 2)}
    if args.holecardsnosuits:
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
                # Frequency of hole cards as a pair
                if args.holecards:
                    count_hole_cards_frequency((c_1,c_2), hole_card_frequency)
                if args.holecardsnosuits:
                    count_hole_cards_frequency([x[0] for x in (c_1,c_2)], hole_card_nosuits_frequency)

            # Get board cards
            board = b.get_summary_board()
            if not board:
                continue

            # Count card frequency of board cards
            for c in board:
                card_frequency[c] += 1

            # Get all combinations of 5 card hands of hole cards with board
            # and count hand frequency
            for hc in hole_cards:
                for hand in combinations(list(hc)+board, 5):
                    # There doesn't seem to be support in Treys for
                    # evaluating 5 card hands, so split hand into 3 and 2
                    hand_treys_1 = [Card.new(c) for c in hand[:3]]
                    hand_treys_2 = [Card.new(c) for c in hand[3:5]]
                    # Evaluate hand for rank
                    hand_rank = evaluator.class_to_string(
                        evaluator.get_rank_class(
                            evaluator.evaluate(hand_treys_1, hand_treys_2)
                        )
                    ).lower()
                    hand_frequency[hand_rank] += 1

    print_results(
        'Distribution of Hands',
        'Hand',
        hand_probabilites,
        hand_frequency,
        std_dev=args.stdev
    )
    print_results(
        'Distribution of Cards',
        'Card',
        {x: 1/len(CARDS) for x in CARDS},
        card_frequency,
        std_dev=args.stdev
    )
    if args.holecards:
        print_results(
            'Distribution of Hole Cards with suits',
            'Hole Cards',
            {x: 1/len(hole_card_frequency) for x in hole_card_frequency.keys()},
            hole_card_frequency,
            std_dev=args.stdev
        )
    if args.holecardsnosuits:
        print_results(
            'Distribution of Hole Cards without suits',
            'Hole Cards',
            {x: 1/len(hole_card_nosuits_frequency) for x in hole_card_nosuits_frequency.keys()},
            hole_card_nosuits_frequency,
            std_dev=args.stdev
        )

if __name__ == '__main__':
    main()
