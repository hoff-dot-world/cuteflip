""" cuteflip_port.py - A second go of my Voltorb Flip Port :P - Logic port from decompilation

	MASSIVE THANKS TO THE TEAM AT https://github.com/pret/pokeheartgold
	this port wouldn't be possible without their hard work

	Copyright (C) 2021-2024 hoff.industries

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <https://www.gnu.org/licenses/>.

	TODO:
		- Mersenne Twister RNG implementation

"""

from random import randint

from cuteflip_data import S_BOARD_ID_DISTRIBUTION, S_BOARD_CONFIGS

CUTEFLIP_PORT_VERSION = (0, 2, 0)

def mt_random():

	return randint(0, 100)

class RoundOutcome:

	NONE = 0
	QUIT = 1
	WON = 2
	LOST = 3

class Axis:

	COL = 0
	ROW = 1

class CardType:

	NONE = 0
	ONE = 1
	TWO = 2
	THREE = 3
	VOLTORB = 4

class Card:

	def __init__(self, c_type=CardType.NONE, \
			memo=0, flipped=False):

		self.c_type = c_type
		self.memo = memo
		self.flipped = flipped

class RoundSummary:

	def __init__(self, outcome=RoundOutcome.NONE, \
			flipped=0, board_id=0, level=0):

		self.outcome = outcome
		self.cards_flipped = flipped
		self.board_id = board_id
		self.level = level


def level_at_least(board_id, level):
	return board_id >= 10 * (level - 1)

def is_multiplier_card(c_type):

	return c_type == CardType.TWO or c_type == CardType.THREE

def card_value(c_type):

	if c_type == CardType.ONE:
		return 1

	if c_type == CardType.TWO:
		return 2

	if c_type == CardType.THREE:
		return 3

	return 0

class GameState:

	def __init__(self):

		self.cards = [[Card() for _ in range(0, 5)] for _ in range(0, 5)]

		self.points_per_col = [0] * 5
		self.points_per_row = [0] * 5

		self.voltorbs_per_col = [0] * 5
		self.voltorbs_per_row = [0] * 5

		self.round_outcome = RoundOutcome.NONE

		self.payout = 0
		self.max_payout = 0

		self.multiplier_cards = 0
		self.multiplier_flipped = 0

		self.cards_flipped = 0
		self.board_id = 0

		self.level = 0
		self.history_head = 0
		self.unk150 = []

		self.board_history = [RoundSummary() for _ in range(0, 5)]

	def clean_board(self):

		self.cards = [[Card() for _ in range(0, 5)] for _ in range(0, 5)]

		self.points_per_col = [0] * 5
		self.points_per_row = [0] * 5

		self.voltorbs_per_col = [0] * 5
		self.voltorbs_per_row = [0] * 5

		self.multiplier_cards = 0
		self.multiplier_flipped = 0

		self.cards_flipped = 0

	def current_round_summary(self):

		return self.board_history[self.history_head]

	def prev_round_summary(self):

		head = self.history_head

		if head == 0:
			idx = 4
		else:
			idx = head - 1

		return self.board_history[idx]

	def calc_next_level(self):

		prev_round = self.prev_round_summary()
		round_outcome = prev_round.outcome

		if round_outcome == RoundOutcome.WON and \
				level_at_least(prev_round.board_id, 8):

			return 0

		board_id = prev_round.board_id

		if level_at_least(board_id, 5):
			for i in range(0, 5):

				round_s = self.board_history[i]

				if round_s.cards_flipped < 8 or \
						round_s.outcome == RoundOutcome.LOST:

					break

			if i == 5:
				return 0

		if (level_at_least(board_id, 7) and prev_round.cards_flipped >= 7) \
			or (level_at_least(board_id, 6) and round_outcome == RoundOutcome.WON):

			return 1

		if (level_at_least(board_id, 6) and prev_round.cards_flipped >= 6) \
			or (level_at_least(board_id, 5) and round_outcome == RoundOutcome.WON):

			return 2

		if (level_at_least(board_id, 5) and prev_round.cards_flipped >= 5) \
			or (level_at_least(board_id, 4) and round_outcome == RoundOutcome.WON):

			return 3

		if (level_at_least(board_id, 4) and prev_round.cards_flipped >= 4) \
			or (level_at_least(board_id, 3) and round_outcome == RoundOutcome.WON):

			return 4

		if (level_at_least(board_id, 3) and prev_round.cards_flipped >= 3) \
			or (level_at_least(board_id, 2) and round_outcome == RoundOutcome.WON):

			return 5

		if (level_at_least(board_id, 2) and prev_round.cards_flipped >= 2) \
			or round_outcome == RoundOutcome.WON:

			return 6

		return 7

	def select_board_id(self):

		rand = mt_random()
		level = self.calc_next_level()

		for i in range(0, 80):
			if rand < S_BOARD_ID_DISTRIBUTION[level][i]:
				break

		self.level = level
		self.board_id = i

	def get_card(self, card_id):

		row = card_id // 5
		col = card_id % 5

		return self.cards[row][col]

	def place_cards_on_board(self, c_type, n, is_not_1):

		attempts = 0
		i = 0

		while i < n:

			if is_not_1:
				card_id = mt_random() % 25
			else:
				card_id = i

			card = self.get_card(card_id)

			if card.c_type == CardType.ONE or not is_not_1:
				card.c_type = c_type

			else:
				attempts += 1

				if attempts >= 100:
					break

				i -= 1

			i += 1

	def voltorbs_along_axis(self, axis, i):

		if axis == Axis.COL:

			return self.voltorbs_per_col[i]

		elif axis == Axis.ROW:

			return self.voltorbs_per_row[i]

		return 0

	def count_multiplier_cards(self):

		for i in range(0, 25):
			card = self.get_card(i)

			if is_multiplier_card(card.c_type):
				self.multiplier_cards += 1

	def count_board_max_payout(self):

		var1 = 1

		for i in range(0, 25):

			card = self.get_card(i)

			if card.c_type != CardType.VOLTORB:
				var1 *= card_value(card.c_type)

		if var1 > 50000:
			var1 = 50000

		self.max_payout = var1

	def count_points_in_rows_cols(self):

		for r in range(0, 5):

			self.points_per_row[r] = 0
			self.points_per_col[r] = 0

			for c in range(0, 5):

				self.points_per_row[r] += card_value(self.cards[r][c].c_type)

				self.points_per_col[r] += card_value(self.cards[c][r].c_type)

	def retry_board_gen(self):

		free_multi_per_col = [0] * 5
		free_multi_per_row = [0] * 5

		free_multipliers = 0

		config = S_BOARD_CONFIGS[self.board_id]

		for i in range(0, 25):

			card = self.get_card(i)

			if is_multiplier_card(card.c_type):
				col = i % 5
				row = i // 5

				voltorbs_in_col = self.voltorbs_along_axis(Axis.COL, col)
				voltorbs_in_row = self.voltorbs_along_axis(Axis.ROW, row)

				if voltorbs_in_row == 0 or voltorbs_in_col == 0:

					free_multi_per_col[col] += 1
					free_multi_per_row[row] += 1

					free_multipliers += 1

		if config.max_free_multipliers <= free_multipliers:
			return True

		for i in range(0, 5):
			if config.max_free_multipliers_per_row_col <= free_multi_per_col[i] \
					or config.max_free_multipliers_per_row_col <= free_multi_per_row[i]:

				return True

		return False

	def count_voltorbs_in_row_cols(self):

		for r in range(0, 5):

			self.voltorbs_per_row[r] = 0
			for c in range(0, 5):
				if self.cards[r][c].c_type == CardType.VOLTORB:

					self.voltorbs_per_row[r] += 1

		for c in range(0, 5):

			self.voltorbs_per_col[c] = 0
			for r in range(0, 5):
				if self.cards[r][c].c_type == CardType.VOLTORB:

					self.voltorbs_per_col[c] += 1


	def generate_board(self):

		voltorbs = S_BOARD_CONFIGS[self.board_id].voltorbs
		twos = S_BOARD_CONFIGS[self.board_id].twos
		threes = S_BOARD_CONFIGS[self.board_id].threes

		for i in range(0, 1000):

			self.place_cards_on_board(CardType.ONE, 25, False)
			self.place_cards_on_board(CardType.VOLTORB, voltorbs, True)
			self.place_cards_on_board(CardType.TWO, twos, True)
			self.place_cards_on_board(CardType.THREE, threes, True)

			self.count_voltorbs_in_row_cols()

			if not self.retry_board_gen():
				break

	def print_cards(self):

		print(f"== VOLTORB FLIP == LEVEL {self.level} BOARD ID {self.board_id}")

		for r in range(0, 5):
			for c in range(0, 5):
				print(f"({r},{c}){self.cards[r][c].c_type} - ", end="")

			print("")

if __name__ == "__main__":

	new_game = GameState()

	new_game.select_board_id()
	new_game.generate_board()

	print(new_game.cards)
	new_game.print_cards()
