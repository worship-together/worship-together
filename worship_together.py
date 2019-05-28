import ui
import midi
import sheet_music
import original_song_view
import storage
import objc_util
import os

experimental_view = False


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
	storage.iPad('songs', 'songs').synchronize()
	storage.iPad('tunes', 'tunes').synchronize()


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


def present_song(sender):
	if experimental_view:
		sheet_music.present_song(sender)
	else:
		original_song_view.present_song(sender)


def create_song_list():
	table = ui.TableView()
	song_files = [file for file in os.listdir('./songs')
				  if midi.is_song(file)]
	song_list = ui.ListDataSource(sorted(song_files))
	song_list.action = present_song
	table.data_source = table.delegate = song_list
	screen_width, screen_height = ui.get_screen_size()
	table.row_height = 40
	table.frame = 0, 0, screen_width, screen_height - 64
	return table


start_screen = StartScreen()
start_screen.background_color = 'white'
start_screen.add_subview(create_song_list())
start_screen.right_button_items = [create_sync_button()]
start_screen.present('fullscreen')
