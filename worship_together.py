import ui
import sound
import midi
import sheet_music
import original_song_view
import storage
import objc_util
import ctypes
import os
import sound

experimental_view = True


def get_subview(name):
	for subview in satb_page.subviews:
		if subview.name == name:
			return subview
	raise RuntimeError('nutn is namd ' + name)


class StartScreen(ui.View):
	def will_close(self):
		sheet_music.exiting = True
		original_song_view.exiting = True


def sync_songs_and_tunes():
	print('start')
	storage.iPad('songs2', 'songs').synchronize()

	storage.iPad('tunes2', 'tunes').synchronize()
	print('end')


def create_sync_button():
	btn_container = ui.View(frame=(0, 0, 32, 44))
	btn = ui.Button(image=ui.Image.named('iob:loop_256'))
	btn.frame = (0, 0, 32, 44)
	btn.action = lambda sender: sync_songs_and_tunes()
	btn_container.add_subview(btn)
	btn_item = ui.ButtonItem()
	btn_item_objc = objc_util.ObjCInstance(btn_item)
	btn_item_objc.customView = objc_util.ObjCInstance(btn_container)
	return btn_item


def present_song(sender, dir):
	if type(sender) == ui.ListDataSource:
		new_dir = dir + '/' + sender.items[sender.selected_row]
	else:
		new_dir = dir + '/' + sender.title
	if os.path.isfile(new_dir):
		if experimental_view:
			sheet_music.present_song(sender, new_dir)
		else:
			original_song_view.present_song(sender)
	else:
		new_table = create_song_list(new_dir)
		new_table.present('fullscreen')


def create_song_list(dir):
	table = ui.TableView()
	song_files = [file for file in os.listdir(dir)]
	song_list = ui.ListDataSource(sorted(song_files))
	song_list.action = lambda sender: present_song(sender, dir)
	table.data_source = table.delegate = song_list
	screen_width, screen_height = ui.get_screen_size()
	table.row_height = 40
	table.frame = 0, 0, screen_width, screen_height - 64
	return table


def create_start_screen(dir):
	buttons = []
	# print(os.listdir())
	length = len(os.listdir(dir))
	for i in range(0, length):
		button = ui.Button()
		button.title = os.listdir(dir)[i]
		button.border_width = 3
		button.border_color = 'black'
		button.background_color = '#f0f0f0'
		button.font = 'Times', 32
		button.tint_color = 'black'
		button.corner_radius = 15
		button.action = lambda sender: present_song(sender, dir)
		y_border = ui.get_screen_size().h / (length * 3)
		x_border = ui.get_screen_size().w / 4
		boundary = 400 / length
		# x = (i * (ui.get_screen_size().w / length)) + border
		# y = border
		# w = (ui.get_screen_size().w / length) - (border * 2)
		# h = ui.get_screen_size().h - (border * 2) - 64
		x = x_border
		y = (i * ((ui.get_screen_size().h - 64) / length)) + y_border - (boundary * (i - ((length - 1) / 2)))
		w = ui.get_screen_size().w - (x_border * 2)
		h = ((ui.get_screen_size().h - 64) / length) - (y_border * 2)
		button.frame = x, y, w, h
		buttons.append(button)
	return buttons


if __name__ == '__main__':
	start_screen = StartScreen()
	start_screen.background_color = 'white'
	for button in create_start_screen('./directory'):
		start_screen.add_subview(button)
	start_screen.right_button_items = [create_sync_button()]
	start_screen.present('fullscreen')
