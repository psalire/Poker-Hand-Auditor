from scipy.stats import chisquare
from math import sqrt

class Results:

    def __init__(self, label_column_size=15, value_column_size=15, columns=6):
        self.set_label_column_size(label_column_size)
        self.set_value_column_size(value_column_size)
        self._set_full_width(6)

    # Set sizes and formatting values based on size
    def set_label_column_size(self, size):
        self._label_column_size = size
        self._label_column = '{:^%d}|' % self._label_column_size
    def set_value_column_size(self, size):
        # Various column formats
        self._value_column_size = size
        self._value_column = '{:^%d}|' % self._value_column_size
        self._float_value_column = '{:^%df}|' % self._value_column_size
        self._float_value = '{:^%df}' % self._value_column_size
    def _set_full_width(self, columns):
        # Various column formats
        self._full_width = self._label_column_size + self._value_column_size*columns + columns
        self._horizontal_divider = ('{:-^%d}' % self._full_width).format('')
        self._value_span_fullwidth = '{:^%d}|' % self._full_width
        self._float_value_span_halfwidth = '{:^%df}' % (self._full_width // 2)
        self._value_column_span_halfwidth = '{:^%d}|' % (self._full_width // 2)

        # Row formats
        self._results_row = self._label_column + self._value_column*columns
        self._halfwidth_value_span_row = self._value_column_span_halfwidth*2
        self._totals_row = self._label_column + self._float_value_column + self._value_column + self._float_value_column*(columns-3) + self._value_column

    # Printing rows
    def _print_row(self, s, divider=False):
        print(s)
        if divider:
            self._print_horizontal_divider()
    def _print_results_row(self, *argv, divider=False):
        self._print_row(self._results_row.format(*argv), divider)
    def _print_halfwidth_value_span_row(self, *argv, divider=False):
        self._print_row(self._halfwidth_value_span_row.format(*argv), divider)
    def _print_fullwidth_value_span_row(self, *argv, divider=False):
        self._print_row(self._value_span_fullwidth.format(*argv), divider)
    # Totals row used in calculate_and_print_results
    def _print_totals_row(self, *argv, divider=False):
        self._print_row(self._totals_row.format(*argv), divider)

    def _format_if_valid(self, format_str, val, append=''):
        return format_str.format(val) if val != None else str(val)+append
    def _print_horizontal_divider(self):
        print(self._horizontal_divider)
    def _print_string_with_divider(self, s):
        print(s)
        self._print_horizontal_divider()

    # Print table of results
    ## title: str, title of the table
    ## label: str, label of the first column
    ## expected: dict, expected values
    ## sample: dict, sampled values
    ## std_dev: int 1,2,3, std_dev for use in confidence limit
    ## label_column_size: int, width of first column
    ## value_column_size: int, width of other columns
    ## is_normal: bool, is normally distributed, whether to calculate confidence intervals
    def calculate_and_print_results(self, title, label, expected, sample, summary, test_results, std_dev=2, is_normal=True):
        columns = 6 if is_normal else 4
        self._set_full_width(columns)

        sample_size = sum(sample.values())

        # Print title and column headers
        self._print_string_with_divider('')
        if is_normal:
            confidence_limit = ['68', '95', '99.7'][std_dev-1]
            table_title = '{}, {}% Confidence Level, n={}'.format(title, confidence_limit, sample_size)
            column_name_args = (label, 'Expected', 'Expected Size','Sample', 'Lower', 'Upper', 'Sample Size')
            # Track proportion values as list of tuples (sample,lower,upper)
            proportions = []
        else:
            table_title = '{}, n={}'.format(title, sample_size)
            column_name_args = (label, 'Expected', 'Expected Size','Sample', 'Sample Size')
        self._print_fullwidth_value_span_row(table_title, divider=True)
        self._print_results_row(*column_name_args, divider=True)

        totals = [0 for _ in range(columns)]
        expected_sizes = []

        # Print column values
        for key in sample:
            sample_percentage = sample[key]/sample_size
            expected_size = round(expected[key]*sample_size)
            expected_sizes.append(expected_size)

            # Print row of values
            if is_normal:
                # Calculate standard error
                ## can't divide by zero
                if sample[key] != 0:
                    standard_error = sqrt((expected[key] * (1-expected[key])) / sample[key])
                    lower_percentage = expected[key] - std_dev*standard_error
                    upper_percentage = expected[key] + std_dev*standard_error
                    proportions.append((sample_percentage, lower_percentage, upper_percentage))
                else:
                    standard_error = None
                    lower_percentage = None
                    upper_percentage = None

                self._print_results_row(
                    key, # Label
                    self._format_if_valid(self._float_value, expected[key]), # Expected proportion
                    expected_size, # Expected size
                    self._format_if_valid(self._float_value, sample_percentage), # Sample proportion
                    self._format_if_valid(self._float_value, lower_percentage), # Upper confidence limit
                    self._format_if_valid(self._float_value, upper_percentage), # Lower confidence limit
                    sample[key], # Sample size
                )
            else:
                self._print_results_row(
                    key, # Label
                    self._format_if_valid(self._float_value, expected[key]), # Expected proportion
                    expected_size, # Expected size
                    self._format_if_valid(self._float_value, sample_percentage), # Sample proportion
                    sample[key], # Sample size
                )


            # Count totals
            totals[0] += expected[key]
            if is_normal:
                totals[1] += expected_size
                if standard_error:
                    totals[2] += sample_percentage
                    totals[3] += lower_percentage
                    totals[4] += upper_percentage
                totals[5] += sample[key]
            else:
                totals[1] += expected_size
                totals[2] += sample_percentage
                totals[3] += sample[key]
        self._print_horizontal_divider()
        self._print_totals_row('Total', *(total for total in totals), divider=True)

        # Find and print chi-square values
        if 0 not in expected_sizes:
            chi_square, chi_square_pvalue = chisquare(list(sample.values()), f_exp=expected_sizes)
        else:
            chi_square, chi_square_pvalue = None, None
        self._print_fullwidth_value_span_row('Chi-Square Goodness of Fit Test Results', divider=True)
        self._print_halfwidth_value_span_row(
            'Chi-square',
            self._format_if_valid(self._float_value_span_halfwidth, chi_square, ' (Expected value(s) == 0)'),
            divider=False,
        )
        self._print_halfwidth_value_span_row(
            'p-value',
            self._format_if_valid(self._float_value_span_halfwidth, chi_square_pvalue, ' (Expected value(s) == 0)'),
            divider=True,
        )

        assert sample_size == totals[5 if is_normal else 3] # Sanity check for sample size

        # Write summary of results
        summary.append(('{}, n={}'.format(title, sample_size), []))
        if is_normal:
            test_results.append(all([l < s < u for s,l,u in proportions]))
            summary[-1][1].append((
                'Sample in {}% confidence interval'.format(confidence_limit),
                'PASS' if test_results[-1] else 'FAIL',
            ))
        if chi_square_pvalue != None:
            test_results.append(chi_square_pvalue > 0.05)
            summary[-1][1].append((
                'Chi-square p-value > 0.05',
                'PASS' if test_results[-1] else 'FAIL',
            ))

    # Print summary
    ## summary: list of pair of strs
    ## test_results: list of bool
    def print_summary(self, summary, test_results):
        self._set_full_width(4)

        self._print_string_with_divider('')
        self._print_fullwidth_value_span_row('SUMMARY', divider=True)
        for t,d in summary:
            self._print_fullwidth_value_span_row(t, divider=True)
            self._print_halfwidth_value_span_row('Test', 'Result', divider=True)
            for test, result in d:
                self._print_halfwidth_value_span_row(test, result)
            self._print_horizontal_divider()
        passing_test_count = test_results.count(True)
        self._print_fullwidth_value_span_row(
            'Passing Tests: {}/{} ({:.2f}%)'.format(passing_test_count, len(test_results), 100*passing_test_count/len(test_results)),
            divider=True,
        )
