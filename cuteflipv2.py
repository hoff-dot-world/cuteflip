""" cuteflipv2.py - A second go of my Voltorb Flip Port :P - UI and game controller

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
		- Show Score/Coins
		- Flip animations

		- I don't quite think the logic for winning / losing
			upleveling / downleveling is completely correct right now...

			likely the round history interface needs work

"""

import sys
from os import path
from json import loads, dumps, JSONDecodeError

from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia

from cuteflip_port import GameState, CardType, RoundOutcome
from cuteflipui import Ui_cuteflip_window

FILE_PATH = path.dirname(path.abspath(__file__))
DATA_PATH = path.join(FILE_PATH, "data")

BGM_PATH = path.join(DATA_PATH, "gc.mp3")
FLIP_PATH = path.join(DATA_PATH, "flip.mp3")
EXPLODE_PATH = path.join(DATA_PATH, "explode.mp3")
REJECT_PATH = path.join(DATA_PATH, "reject.mp3")

PREFS_PATH = path.join(FILE_PATH, "prefs.json")

CUTEFLIP_VERSION = (0, 2, 0)

class CuteFlipUI(Ui_cuteflip_window):

	def __init__(self, flip_window):

		super().setupUi(flip_window)

		self.preferences = {

			"se_vol": 100,
			"bgm_vol": 40,
			"play_bgm": True
		}

		self.load_preferences()

		self.remaining_multipliers = 0

		self.flip_state = GameState()

		self.card_register = [

			self.t00, self.t01, self.t02, self.t03, self.t04,
			self.t10, self.t11, self.t12, self.t13, self.t14,
			self.t20, self.t21, self.t22, self.t23, self.t24,
			self.t30, self.t31, self.t32, self.t33, self.t34,
			self.t40, self.t41, self.t42, self.t43, self.t44
		]

		self.column_counters = [

			(self.l50_0, self.l50_2),
			(self.l51_0, self.l51_2),
			(self.l52_0, self.l52_2),
			(self.l53_0, self.l53_2),
			(self.l54_0, self.l54_2)
		]

		self.row_counters = [

			(self.l05_0, self.l05_2),
			(self.l15_0, self.l15_2),
			(self.l25_0, self.l25_2),
			(self.l35_0, self.l35_2),
			(self.l45_0, self.l45_2)
		]

		self.tile1_icon = QtGui.QIcon()
		self.tile1_icon.addPixmap(QtGui.QPixmap("data/tile-1.png"), \
			QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.tile2_icon = QtGui.QIcon()
		self.tile2_icon.addPixmap(QtGui.QPixmap("data/tile-2.png"), \
			QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.tile3_icon = QtGui.QIcon()
		self.tile3_icon.addPixmap(QtGui.QPixmap("data/tile-3.png"), \
			QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.tileV_icon = QtGui.QIcon()
		self.tileV_icon.addPixmap(QtGui.QPixmap("data/tile-v.png"), \
			QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.tile0_icon = QtGui.QIcon()
		self.tile0_icon.addPixmap(QtGui.QPixmap("data/tile.png"), \
			QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.icon_map = {

			CardType.NONE: self.tile0_icon,

			CardType.ONE: self.tile1_icon,
			CardType.TWO: self.tile2_icon,
			CardType.THREE: self.tile3_icon,

			CardType.VOLTORB: self.tileV_icon
		}

		self.music_playlist = QtMultimedia.QMediaPlaylist()
		self.music_playlist.addMedia(QtMultimedia.QMediaContent(\
			QtCore.QUrl.fromLocalFile(BGM_PATH)))

		self.music_playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)

		self.music_player = QtMultimedia.QMediaPlayer()
		self.music_player.setPlaylist(self.music_playlist)

		self.effect_player = QtMultimedia.QMediaPlayer()
		self.effect_player.setVolume(self.preferences["se_vol"])

		self.init_game()
		self.link_ui()

		self.update_bgm_volume()

		if self.preferences["play_bgm"]:
			self.music_player.play()

	def show_message_box(self, message, icon):

		message_box = QtWidgets.QMessageBox()

		message_box.setIcon(icon)
		message_box.setText(message)
		message_box.setWindowTitle(message)

		message_box.exec_()

	def init_game(self):

		self.hide_board()
		self.flip_state.clean_board()

		self.flip_state.select_board_id()
		self.flip_state.generate_board()

		self.flip_state.count_points_in_rows_cols()
		self.flip_state.count_board_max_payout()
		self.flip_state.count_multiplier_cards()

		self.remaining_multipliers = self.flip_state.multiplier_cards

		self.set_labels()

		self.show_message_box(f"Begin Level {7 - self.flip_state.level + 1}!", \
			QtWidgets.QMessageBox.Information)

	def update_bgm_volume(self):

		self.preferences["bgm_vol"] = self.bgm_vol_slider.value()
		self.music_player.setVolume(self.preferences["bgm_vol"])

		if self.preferences["play_bgm"]:
			self.bgm_vol_lbl.setText(f"Music (ON) Volume - {self.preferences['bgm_vol']} %")
		else:
			self.bgm_vol_lbl.setText(f"Music (OFF) Volume - {self.preferences['bgm_vol']} %")

	def toggle_bgm(self):

		if self.preferences["play_bgm"]:

			self.music_player.stop()
		else:
			self.music_player.play()

		self.preferences["play_bgm"] = not self.preferences["play_bgm"]
		self.update_bgm_volume()

		self.write_preferences()

	def link_ui(self):

		for i in range(0, len(self.card_register)):

			self.card_register[i].clicked.connect(\
				lambda state,i=i: self.turnover_card(i))

		self.bgm_vol_slider.setValue(self.preferences["bgm_vol"])
		self.bgm_vol_slider.valueChanged.connect(self.update_bgm_volume)

		self.btn_toggle_music.clicked.connect(self.toggle_bgm)

		self.pushButton.clicked.connect(sys.exit)

	def write_preferences(self):

		with open(PREFS_PATH, "w") as prefs_file:

			prefs_file.write(dumps(self.preferences))

	def load_preferences(self):

		try:

			with open(PREFS_PATH, "r") as prefs_file:
				pref_obj = loads(prefs_file.read())

		except (FileNotFoundError, JSONDecodeError):

			self.write_preferences()
			return False

		try:

			self.preferences["bgm_vol"] = pref_obj["bgm_vol"]
			self.preferences["play_bgm"] = pref_obj["play_bgm"]
			self.preferences["se_vol"] = pref_obj["se_vol"]

		except KeyError:

			self.show_message_box("Preferences file corrupted! Writing blank.", \
				QtWidgets.QMessageBox.Critical)

			self.write_preferences()
			return False

		return True

	def play_effect(self, sound_file):

		self.effect_player.setMedia(QtMultimedia.QMediaContent(\
			QtCore.QUrl.fromLocalFile(sound_file)))
		self.effect_player.play()

	def set_labels(self):

		voltorbs_c = self.flip_state.voltorbs_per_col
		points_c = self.flip_state.points_per_col

		voltorbs_r = self.flip_state.voltorbs_per_row
		points_r = self.flip_state.points_per_row

		for i in range(0, len(self.column_counters)):

			column_counter = self.column_counters[i]
			row_counter = self.row_counters[i]

			column_counter[1].setText(str(voltorbs_c[i]))
			column_counter[0].setText(str(points_c[i]))

			row_counter[1].setText(str(voltorbs_r[i]))
			row_counter[0].setText(str(points_r[i]))

	def hide_board(self):

		for i in range(0, len(self.card_register)):
			self.card_register[i].setIcon(self.icon_map[CardType.NONE])

	def reveal_board(self):

		for i in range(0, len(self.card_register)):
			self.turnover_card(i, revealing=True)

	def is_game_won(self):

		return self.remaining_multipliers == 0

	def turnover_card(self, card_id, revealing=False):

		internal_card = self.flip_state.get_card(card_id)

		if internal_card.flipped and not revealing:

			self.play_effect(REJECT_PATH)
			return

		self.card_register[card_id].setIcon(\
			self.icon_map[internal_card.c_type])

		if revealing:
			return

		self.play_effect(FLIP_PATH)

		round_summary = self.flip_state.current_round_summary()
		round_summary.cards_flipped += 1

		if internal_card.c_type == CardType.VOLTORB:

			round_summary.outcome = RoundOutcome.LOST

			self.flip_state.history_head = (\
				self.flip_state.history_head + 1) % 5

			self.play_effect(EXPLODE_PATH)

			self.reveal_board()
			self.show_message_box("You lost :(", QtWidgets.QMessageBox.Critical)

			self.init_game()
			return

		if internal_card.c_type != CardType.ONE:
			self.remaining_multipliers -= 1

		internal_card.flipped = True

		if self.is_game_won():

			round_summary.outcome = RoundOutcome.WON

			self.flip_state.history_head = (\
				self.flip_state.history_head + 1) % 5

			self.reveal_board()
			self.show_message_box("You won!", QtWidgets.QMessageBox.Information)

			self.init_game()

if __name__ == "__main__":

	cuteflip_app = QtWidgets.QApplication(sys.argv)
	cuteflip_window = QtWidgets.QMainWindow()

	cuteflip_ui = CuteFlipUI(cuteflip_window)
	cuteflip_window.show()

	sys.exit(cuteflip_app.exec())
