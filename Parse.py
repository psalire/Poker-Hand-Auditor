import re

HAND_PROBABILITIES = {
    'high card': 0.501177,
    'pair': 0.422569,
    'two pair': 0.047539,
    'three of a kind': 0.021128,
    'straight': 0.003925,
    'flush': 0.001965,
    'full house': 0.001441,
    'four of a kind': 0.00024,
    'straight flush': 0.0000139+0.00000154,
    # 'royal flush': 0.00000154,
}

class Bovada:

    # Regular expressions for parsing and extracting card values
    _re_card = '[2-9TJQKA][cdhs]'
    _re_position = '(?:UTG(?:\+[1-5])?|Dealer|(?:Small|Big) Blind|Dealer)'
    ## Line that occurs before each hand
    RE_HEADER = re.compile('^Bovada Hand #\d+: ')
    ## Line that occurs before each stage
    RE_STAGE = {
        'Hole Cards': re.compile('^\*\*\* HOLE CARDS \*\*\*$'),
        # 'Flop': re.compile('^\*\*\* FLOP \*\*\* \[(%s ){2}%s\]$' % (_re_card, _re_card)),
        # 'Turn': re.compile('^\*\*\* TURN \*\*\* \[(%s ){2}%s\] \[(%s){1}\]$' % (_re_card, _re_card, _re_card)),
        # 'River': re.compile('^\*\*\* RIVER \*\*\* \[(%s ){3}%s\] \[(%s){1}\]$' % (_re_card, _re_card, _re_card)),
        'Summary': re.compile('^\*\*\* SUMMARY \*\*\*$'),
    }
    ## Line for hole cards
    RE_HOLE_CARDS = re.compile(
        '^%s(?: \[ME\])? : Card dealt to a spot \[(%s) (%s)\] $' % (_re_position, _re_card, _re_card)
    )
    ## Line for hole cards with [ME] label i.e. my hole cards
    RE_HOLE_CARDS_ME_ONLY = re.compile(
        '^%s(?: \[ME\]) : Card dealt to a spot \[(%s) (%s)\] $' % (_re_position, _re_card, _re_card)
    )
    ## Line for board
    RE_BOARD = re.compile(
        '^Board \[((?:%s ){1,3} |(?:%s ){4}|(?:%s ){4}(?:%s))\]$' % (_re_card, _re_card, _re_card, _re_card)
    )

    ## file: str, filename including path
    def __init__(self, file):
        self.open_new_file(file)
    def __del__(self):
        if self.file:
            self.file.close()

    ## file: str, filename including path
    def open_new_file(self, file):
        if hasattr(self, 'file') and self.file:
            self.file.close()
        self.file = open(file, 'r')

    # Move cursor to first re match, returns empty string on EOF
    ## regex: regular expression to match
    def _move_cursor_to_re(self, regex):
        l = self.file.readline()
        while not regex.match(l) and l:
            l = self.file.readline()
        return l

    # Returns next hole cards as a list of tuples and moves cursor to location
    # Returns None if does not find hole cards header, e.g. EOF
    ## only_me : bool, only count my ([ME]) hole cards
    def get_hole_cards(self, only_me=False):
        # Find Hole Cards header
        if not self._move_cursor_to_re(self.RE_STAGE['Hole Cards']):
            return None
        re_hole_cards = self.RE_HOLE_CARDS if not only_me else self.RE_HOLE_CARDS_ME_ONLY

        # Return all hole cards as a list of tuples
        cards = []
        while True:
            l = self.file.readline()
            m = re_hole_cards.match(l) # RE match for hole cards
            if not m:
                break
            cards.append((m.group(1), m.group(2)))

        return cards
    # Returns next board cards as a list and moves cursor to location
    # Returns None if does not find summary header, e.g. no board cards seen or EOF
    def get_summary_board(self):
        # Find Summary header
        if not self._move_cursor_to_re(self.RE_STAGE['Summary']):
            return None

        while True:
            l = self.file.readline()
            m = self.RE_BOARD.match(l) # RE match for board
            # If found board, return board cards as a list
            if m:
                return m.group(1).split()
            # If at next hand without getting a board return None
            if self.RE_HEADER.match(l):
                return None
