""" cuteflip_data.py - A second go of my Voltorb Flip Port :P - Data dump from decompilation

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
	along with this program.  If not, see <https://www.gnu.org/licenses/>. """

CUTEFLIP_DATA_VERSION = (0, 2, 0)

class BoardConfig:

	def __init__(self, voltorbs=0, twos=0, \
			threes=0, max_free_per_row_col=0, max_free_multipliers=0):

		self.voltorbs = voltorbs
		self.twos = twos
		self.threes = threes

		self.max_free_multipliers_per_row_col = max_free_per_row_col
		self.max_free_multipliers = max_free_multipliers

S_BOARD_CONFIGS = [
	# Lv. 1
	# Voltorbs  Twos  Threes  MaxFreePerRowCol  MaxFreeTotal       Payout
	BoardConfig( 6,  3, 1, 3, 3 ), #     24
	BoardConfig( 6,  0, 3, 2, 2 ), #     27
	BoardConfig( 6,  5, 0, 3, 4 ), #     32
	BoardConfig( 6,  2, 2, 3, 3 ), #     36
	BoardConfig( 6,  4, 1, 3, 4 ), #     48

	BoardConfig( 6,  3, 1, 3, 3 ), #     24
	BoardConfig( 6,  0, 3, 2, 2 ), #     27
	BoardConfig( 6,  5, 0, 3, 4 ), #     32
	BoardConfig( 6,  2, 2, 3, 3 ), #     36
	BoardConfig( 6,  4, 1, 3, 4 ), #     48

	# Lv. 2
	BoardConfig( 7,  1, 3, 2, 3 ), #     54
	BoardConfig( 7,  6, 0, 3, 4 ), #     64
	BoardConfig( 7,  3, 2, 2, 3 ), #     72
	BoardConfig( 7,  0, 4, 2, 3 ), #     81
	BoardConfig( 7,  5, 1, 3, 4 ), #     96

	BoardConfig( 7,  1, 3, 2, 2 ), #     54
	BoardConfig( 7,  6, 0, 3, 3 ), #     64
	BoardConfig( 7,  3, 2, 2, 2 ), #     72
	BoardConfig( 7,  0, 4, 2, 2 ), #     81
	BoardConfig( 7,  5, 1, 3, 3 ), #     96

	# Lv. 3
	BoardConfig( 8,  2, 3, 2, 3 ), #    108
	BoardConfig( 8,  7, 0, 3, 4 ), #    128
	BoardConfig( 8,  4, 2, 3, 4 ), #    144
	BoardConfig( 8,  1, 4, 2, 3 ), #    162
	BoardConfig( 8,  6, 1, 4, 3 ), #    192

	BoardConfig( 8,  2, 3, 2, 2 ), #    108
	BoardConfig( 8,  7, 0, 3, 3 ), #    128
	BoardConfig( 8,  4, 2, 3, 3 ), #    144
	BoardConfig( 8,  1, 4, 2, 2 ), #    162
	BoardConfig( 8,  6, 1, 3, 3 ), #    192

	# Lv. 4
	BoardConfig( 8,  3, 3, 4, 3 ), #    216
	BoardConfig( 8,  0, 5, 2, 3 ), #    243
	BoardConfig( 10, 8, 0, 4, 5 ), #    256
	BoardConfig( 10, 5, 2, 3, 4 ), #    288
	BoardConfig( 10, 2, 4, 3, 4 ), #    324

	BoardConfig( 8,  3, 3, 3, 3 ), #    216
	BoardConfig( 8,  0, 5, 2, 2 ), #    243
	BoardConfig( 10, 8, 0, 4, 4 ), #    256
	BoardConfig( 10, 5, 2, 3, 3 ), #    288
	BoardConfig( 10, 2, 4, 3, 3 ), #    324

	# Lv. 5
	BoardConfig( 10, 7, 1, 4, 5 ), #    384
	BoardConfig( 10, 4, 3, 3, 4 ), #    432
	BoardConfig( 10, 1, 5, 3, 4 ), #    486
	BoardConfig( 10, 9, 0, 4, 5 ), #    512
	BoardConfig( 10, 6, 2, 4, 5 ), #    576

	BoardConfig( 10, 7, 1, 4, 4 ), #    384
	BoardConfig( 10, 4, 3, 3, 3 ), #    432
	BoardConfig( 10, 1, 5, 3, 3 ), #    486
	BoardConfig( 10, 9, 0, 4, 4 ), #    512
	BoardConfig( 10, 6, 2, 4, 4 ), #    576

	# Lv. 6
	BoardConfig( 10, 3, 4, 3, 4 ), #    648
	BoardConfig( 10, 0, 6, 3, 4 ), #    729
	BoardConfig( 10, 8, 1, 4, 5 ), #    768
	BoardConfig( 10, 5, 3, 4, 5 ), #    864
	BoardConfig( 10, 2, 5, 3, 4 ), #    972

	BoardConfig( 10, 3, 4, 3, 3 ), #    648
	BoardConfig( 10, 0, 6, 3, 3 ), #    729
	BoardConfig( 10, 8, 1, 4, 4 ), #    768
	BoardConfig( 10, 5, 3, 4, 4 ), #    864
	BoardConfig( 10, 2, 5, 3, 3 ), #    972

	# Lv. 7
	BoardConfig( 10, 7, 2, 4, 5 ), #   1152
	BoardConfig( 10, 4, 4, 4, 5 ), #   1296
	BoardConfig( 13, 1, 6, 3, 4 ), #   1458
	BoardConfig( 13, 9, 1, 5, 6 ), #   1536
	BoardConfig( 10, 6, 3, 4, 5 ), #   1728

	BoardConfig( 10, 7, 2, 4, 4 ), #   1152
	BoardConfig( 10, 4, 4, 4, 4 ), #   1296
	BoardConfig( 13, 1, 6, 3, 3 ), #   1458
	BoardConfig( 13, 9, 1, 5, 5 ), #   1536
	BoardConfig( 10, 6, 3, 4, 4 ), #   1728

	# Lv. 8
	BoardConfig( 10, 0, 7, 3, 4 ), #   2187
	BoardConfig( 10, 8, 2, 5, 6 ), #   2304
	BoardConfig( 10, 5, 4, 4, 5 ), #   2592
	BoardConfig( 10, 2, 6, 4, 5 ), #   2916
	BoardConfig( 10, 7, 3, 5, 6 ), #   3456

	BoardConfig( 10, 0, 7, 3, 3 ), #   2187
	BoardConfig( 10, 8, 2, 5, 5 ), #   2304
	BoardConfig( 10, 5, 4, 4, 4 ), #   2592
	BoardConfig( 10, 2, 6, 4, 4 ), #   2916
	BoardConfig( 10, 7, 3, 5, 5 ), #   3456
]

S_BOARD_ID_DISTRIBUTION = [
	# Lv. 8
	[
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
	],
	# Lv. 7
	[
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	],
	# Lv. 6
	[
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	],
	# Lv. 5
	[
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	],
	# Lv. 4
	[
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	],
	# Lv. 3
	[
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	],
	# Lv. 2
	[
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	],
	# Lv. 1
	[
		10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	],
]
