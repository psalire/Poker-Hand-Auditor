import os
import re
import argparse
import Parse
from treys import Card, Evaluator
from itertools import combinations
from scipy.stats import chisquare
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

# Helper functions for print_results
def format_if_valid(format_str, val, append=''):
    return format_str.format(val) if val != None else str(val)+append

# Print table of results
## title: str, title of the table
## label: str, label of the first column
## expected: dict, expected values
## sample: dict, sampled values
## std_dev: int 1,2,3, std_dev for use in confidence limit
## label_column_size: int, width of first column
## value_column_size: int, width of other columns
## is_normal: bool, is normally distributed, whether to calculate confidence intervals
def print_results(title, label, expected, sample, std_dev=2, label_column_size=15, value_column_size=15, is_normal=True):
    columns = 6 if is_normal else 4
    full_width = label_column_size + value_column_size*columns + columns
    horizontal_divider = ('{:-^%d}' % full_width).format('')

    def print_with_divider(string):
        print(string)
        print(horizontal_divider)

    # Format string based on number and size of columns
    float_value = '{:^%df}' % value_column_size
    float_value_span_halfwidth = '{:^%df}' % (full_width // 2)
    ## Columns
    label_column = '{:^%d}|' % label_column_size
    value_column = '{:^%d}|' % value_column_size
    float_value_column = '{:^%df}|' % value_column_size
    value_column_span_halfwidth = '{:^%d}|' % (full_width // 2)
    value_span_fullwidth = '{:^%d}|' % full_width

    # Row formatting
    results_row = label_column + value_column*columns
    totals_row = label_column + float_value_column + value_column + float_value_column*(columns-3) + value_column
    chi_square_row = value_column_span_halfwidth*2

    sample_size = sum(sample.values())

    # Print title and column headers
    print('\n'+horizontal_divider)
    if is_normal:
        confidence_limit = ['68', '95', '99.7'][std_dev-1]
        title_args = (title, confidence_limit, sample_size)
        column_name_args = (label, 'Expected', 'Expected Size','Sample', 'Lower', 'Upper', 'Sample Size')
    else:
        title_args = (title, sample_size)
        column_name_args = (label, 'Expected', 'Expected Size','Sample', 'Sample Size')
    print_with_divider(value_span_fullwidth.format('{}, n={}'.format(*title_args)))
    print_with_divider(results_row.format(*column_name_args))

    sums = [0 for _ in range(columns)]
    expected_sizes = []

    # Print column values
    for key in sample:
        sample_percentage = sample[key]/sample_size
        expected_size = round(expected[key]*sample_size)
        expected_sizes.append(expected_size)

        # Calculate standard error
        ## can't divide by zero
        if is_normal:
            if sample[key] != 0:
                standard_error = sqrt((expected[key] * (1-expected[key])) / sample[key])
                lower_percentage = expected[key] - std_dev*standard_error
                upper_percentage = expected[key] + std_dev*standard_error
            else:
                standard_error = None
                lower_percentage = None
                upper_percentage = None

            print(results_row.format(
                    key, # Label
                    format_if_valid(float_value, expected[key]), # Expected proportion
                    expected_size, # Expected size
                    format_if_valid(float_value, sample_percentage), # Sample proportion
                    format_if_valid(float_value, lower_percentage), # Upper confidence limit
                    format_if_valid(float_value, upper_percentage), # Lower confidence limit
                    sample[key], # Sample size
                )
            )
        else:
            print(results_row.format(
                    key, # Label
                    format_if_valid(float_value, expected[key]), # Expected proportion
                    expected_size, # Expected size
                    format_if_valid(float_value, sample_percentage), # Sample proportion
                    sample[key], # Sample size
                )
            )
        sums[0] += expected[key]
        if is_normal:
            sums[1] += expected_size
            if standard_error:
                sums[2] += sample_percentage
                sums[3] += lower_percentage
                sums[4] += upper_percentage
            sums[5] += sample[key]
        else:
            sums[1] += expected_size
            sums[2] += sample_percentage
            sums[3] += sample[key]
    print(horizontal_divider)
    print_with_divider(totals_row.format('Total', *(sum for sum in sums)))

    # Find and print chi-square values
    if 0 not in expected_sizes:
        chi_square, chi_square_pvalue = chisquare(list(sample.values()), f_exp=expected_sizes)
    else:
        chi_square, chi_square_pvalue = None, None
    print_with_divider(value_span_fullwidth.format('Chi-Square Goodness of Fit Test Results'))
    print(chi_square_row.format(
        'Chi-square',
        format_if_valid(float_value_span_halfwidth, chi_square, ' (An expected value == 0)'),
    ))
    print_with_divider(chi_square_row.format(
        'p-value',
        format_if_valid(float_value_span_halfwidth, chi_square_pvalue, ' (An expected value == 0)'),
    ))
    assert sample_size == sums[5 if is_normal else 3] # Sanity check for sample size

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
    argparser = argparse.ArgumentParser(description='Poker Hand Auditor')
    argparser.add_argument('path', type=str, help='Path to hand history directory')
    argparser.add_argument('--allcombinations', action='store_true', help='Show table for frequency of all combinations between hole and board cards.')
    argparser.add_argument('--onlyme', action='store_true', help='Only count my hands')
    argparser.add_argument('--holecards', action='store_true', help='Show table for frequency of hole cards without suits')
    argparser.add_argument('--holecardswithsuits', action='store_true', help='Show table for frequency of hole cards with suits (Long output)')
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
                # Frequency of hole cards as a pair
                if args.holecardswithsuits:
                    count_hole_cards_frequency((c_1,c_2), hole_card_frequency)
                if args.holecards:
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
                count_hand_frequency(hc, board, evaluator, hand_frequency)

                if args.allcombinations:
                    for hand in combinations(list(hc)+board, 5):
                        count_hand_frequency(hand[:2], hand[2:], evaluator, hand_allcombinations_frequency)

    print_results(
        'Distribution of Hands',
        'Hand',
        hand_probabilites,
        hand_frequency,
        std_dev=args.stdev,
    )
    if args.allcombinations:
        print_results(
            'Distribution of All Hand Combinations',
            'Hand',
            hand_probabilites,
            hand_allcombinations_frequency,
            std_dev=args.stdev,
        )
    print_results(
        'Distribution of Cards',
        'Card',
        {x: 1/len(CARDS) for x in CARDS},
        card_frequency,
        std_dev=args.stdev,
        is_normal=False
    )
    if args.holecardswithsuits:
        hole_card_combinations = [' '.join(x) for x in combinations(CARDS, 2)]
        hole_card_expected_frequency = {x: hole_card_combinations.count(x) / len(hole_card_combinations) for x in hole_card_combinations}

        print_results(
            'Distribution of Hole Cards with suits',
            'Hole Cards',
            hole_card_expected_frequency,
            hole_card_frequency,
            std_dev=args.stdev,
            is_normal=False,
        )
    if args.holecards:
        hole_card_nosuit_combinations = [' '.join((x[0], y[0])) for x, y in combinations(CARDS, 2)]
        hole_card_nosuits_expected_frequency = {x: hole_card_nosuit_combinations.count(x) / len(hole_card_nosuit_combinations) for x in hole_card_nosuit_combinations}

        print_results(
            'Distribution of Hole Cards without suits',
            'Hole Cards',
            hole_card_nosuits_expected_frequency,
            hole_card_nosuits_frequency,
            std_dev=args.stdev,
            is_normal=False,
        )

if __name__ == '__main__':
    main()
