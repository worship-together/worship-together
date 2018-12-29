"""
Storage

REQUIREMENTS
- Store song files locally for playback without Internet
- Automatically upload/download songs in background when Internet available
- Support the following song modifications offline:
    - Create, edit, delete, rename
- Modifying songs requires a password built into the app
- Last song update wins (no merging)
- Songs deleted locally will be deleted from remote when Internet available
- Songs deleted from remote will be deleted locally

DESIGN
- Whenever a song is created/edited locally, append ".UPLOAD" to filename
- Whenever a song is deleted locally, append ".DELETE" to filename
- Whenever a song is renamed locally, append ".DELETE" to the old filename
    - and ".UPLOAD" to the new filename
- Remote contains file named 'last_upload', modified after each upload
- Local file named 'last_download', modified after each download
- Periodically synchronize
    - Cache remote 'last_upload' file modified time
    - Local to Remote
        - Enumerate all local files with .UPLOAD suffix
            - Copy file up to remote without .UPLOAD suffix
            - If successful, remote .UPLOAD suffix from file
        - Enumerate all local files with .DELETE suffix
            - Delete corresponding file from remote
            - If successful, delete local file
        - If any files were uploaded or deleted
            - Modify last_upload file on remote
    - Remote to Local
        - If cached 'last_upload' modified time newer than 'last_download'
            - Enumerate all local and remote files together in order with tuple
                - Leave gaps for missing local or remote files (tuple diagram)
                    +---------------+--------------+
                    |     Local     |    Remote    |
                    +---------------+--------------+
                    |               |    File A    |  (Create)
                    +---------------+--------------+
                    |    File B     |    File B    |  (Update)
                    +---------------+--------------+
                    |    File C     |              |  (Delete)
                    +---------------+--------------+
                - If file only on remote, download to local
                - If file on local & remote _and_ remote is newer
                    - Download to remote
                - If file only on local, delete local
        - Modify local 'last_download' file (regardless)

VERIFICATION
- Use a specific test directory on the local & remote
- All local & remote files are deleted before each test
- Local To Remote
    - Upload
        - Create two uniquely named local files, one an .UPLOAD suffix
        - Synchronize
        - Verify that the file with the .UPLOAD suffix was uploaded
        - Verify no .UPLOAD suffix on either the local or remote filenames
    - Delete
        - Create two uniquely named remote files
        - Create one local rile with the same name as a remote file
        - Append the .DELETE suffix to the local file
        - Synchronize
        - Verify the local and corresponding remote files were both deleted
    - Verify after each test that the remote 'last_upload' date was updated
- Remote To Local
    - Create two uniquely named remote files
    - Create two uniquely named local files
    - One of the local filenames must match a remote & have different content
    - (same as above diagram)
    - Make local 'last_download' date newer than remote 'last_upload'
    - Synchronize
    - Verify no files have changed, been created, or deleted
    - Make remote 'last_upload' date newer than local 'last_download'
    - Synchronize
    - Verify local file with no corresponding remote is deleted
    - Verify remote file with no corresponding local is downloaded locally
    - Verify content of remote file with same name as local has been downloaded
- Verify after each test that the local 'last_download' newer than 'last_upload'

OPEN QUESTIONS
- How to access Azure from iPad? (limited set of azure Python libs?)
- How are file times represented on iPad?
- How to update in background?
- How to detect that an Internet connection is available?
"""

from azure.storage.file import FileService
import datetime
import os
import shutil
import time


#
#  IMPLEMENTATION
#

service = FileService(
    account_name='worshiptogether',
    account_key='33TG6/7zK8TmKHmlSRthHpGxve8YJfu3M9ut77vn0lUy'
                'B2ZQqfL8ZdDiucbB8MAyg59707Mcxywhy2fFG/ISZA==')
share = 'songs'
upload_suffix = ".UPLOAD"
delete_suffix = ".DELETE"


def upload_files(local_dir, remote_dir):
	for file in os.listdir(local_dir):
		if file.endswith(upload_suffix):
			new_name = file[:-(len(upload_suffix))]
			old_path = local_dir+'/'+file
			new_path = local_dir+'/'+new_name
			os.rename(old_path, new_path)
			service.create_file_from_path(share, remote_dir, new_name, new_path)
			
			
def download_files(local_dir, remote_dir):
	for file in service.list_directories_and_files(share, remote_dir):
		if os.path.exists(local_dir+'/'+file.name):
			local_time = get_local_modified_time(local_dir, file.name)
			remote_time = get_remote_modified_time(remote_dir, file.name)
			if remote_time > local_time:
				service.get_file_to_path(share, remote_dir, file.name, local_dir+'/'+file.name)
				time.sleep(1)
				os.utime(local_dir+'/'+file.name, (datetime.datetime.timestamp(datetime.datetime.now()), datetime.datetime.timestamp(datetime.datetime.now())))
		else:
			service.get_file_to_path(share, remote_dir, file.name, local_dir + '/' + file.name)
			time.sleep(1)
			os.utime(local_dir + '/' + file.name, (datetime.datetime.timestamp(datetime.datetime.now()), datetime.datetime.timestamp(datetime.datetime.now())))
#    for file in os.listdir(local_dir):
#        if not service.exists(share, directory_name=remote_dir, file_name=file):
#            os.remove(local_dir+'/'+file)

def delete_files(local_dir, remote_dir):
	for file in os.listdir(local_dir):
		if file.endswith(delete_suffix) or not service.exists(share, directory_name=remote_dir, file_name=file):
			os.remove(local_dir+'/'+file)
			if service.exists(share, directory_name=remote_dir, file_name=file[:-(len(delete_suffix))]):
				service.delete_file(share, remote_dir, file[:-(len(delete_suffix))])
				
				
def synchronize(local_dir, remote_dir):
	upload_files(local_dir, remote_dir)
	delete_files(local_dir, remote_dir)
	download_files(local_dir, remote_dir)
	
#
# VERIFICATION
#

test_dir = 'test'


def delete_all_local_and_remote(create_dir=True):
	if os.path.exists(test_dir):
		shutil.rmtree(test_dir)
	if create_dir:
		os.mkdir(test_dir)
	if service.exists(share, test_dir):
		for file in service.list_directories_and_files(share, test_dir):
			service.delete_file(share, test_dir, file.name)
		service.delete_directory(share, test_dir)
	if create_dir:
		service.create_directory(share, test_dir)
	
	
def create_local_file(name, content):
	with open(test_dir + '/' + name, 'w') as file:
		file.write(content)
		
		
def create_remote_file(name, content):
	service.create_file_from_text(share, test_dir, name, content)
	
	
def verify_file_uploaded(name, content):
	file_found = False
	for file in service.list_directories_and_files(share, test_dir):
		assert not file_found
		assert file.name == name
		file_found = True
		remote = service.get_file_to_text(share, test_dir, name)
		if remote.content != content:
			print(f'remote content different from local content for {name}:')
			print(f'remote content: {remote.content}')
			print(f'local content: {content}')
			assert remote.content == content
	assert file_found
	
	
def remote_file_deleted(name):
	file_found = False
	for file in service.list_directories_and_files(share, test_dir):
		if file.name == name:
			file_found = True
	return not file_found
	
	
	
def remote_file_exists(name):
	for file in service.list_directories_and_files(share, test_dir):
		if file.name == name:
			return True
	return False
	
	
def local_file_exists(name):
	return os.path.exists(test_dir + '/' + name)
	
	
def test_local_to_remote_upload():
	delete_all_local_and_remote()
	create_local_file('file a.UPLOAD', 'content a')
	create_local_file('file b', 'content b')
	synchronize(test_dir, test_dir)
	verify_file_uploaded('file a', 'content a')
	assert local_file_exists('file a')
	assert not local_file_exists('file a.UPLOAD')
	assert not remote_file_exists('file b')
	
	
def test_local_to_remote_delete():
	delete_all_local_and_remote()
	create_local_file('file a.DELETE', 'content a')
	create_local_file('file b', 'content b')
	create_local_file('file d.DELETE', 'content d')
	create_remote_file('file a', 'content a')
	create_remote_file('file b', 'content b')
	create_remote_file('file c', 'content c')
	synchronize(test_dir, test_dir)
	assert remote_file_deleted('file a')
	assert not remote_file_deleted('file b')
	assert not remote_file_deleted('file c')
	assert not local_file_exists('file d')
	assert not local_file_exists('file d.DELETE')
	assert remote_file_deleted('file d')
	assert not local_file_exists('file a')
	assert not local_file_exists('file a.DELETE')
	
#        print(f'{file.name}: {file.properties.last_modified}, '
#              f'{file.properties.content_length}')


def calculate_month_days(month):
	if month == 0:
		return 0
	elif month == 9 or month == 4 or month == 6 or month == 11:
		return calculate_month_days(month - 1) + 30
	elif month == 2:
		return calculate_month_days(month - 1) + 28
	else:
		return calculate_month_days(month - 1) + 30
		
		
def get_local_modified_time(dir, file):
	mtime = os.path.getmtime(dir + '/' + file)
	dtime = datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc)
	return dtime.replace(microsecond=0)
	
	
def get_remote_modified_time(dir, file):
	dtime = service.get_file_properties(share, dir, file).properties.last_modified
	return dtime.replace(microsecond=0)
	
	
def test_remote_to_local_download():
	delete_all_local_and_remote()
	create_local_file('file a', 'content a outdated')
	create_local_file('file b', 'content b')
	time.sleep(1)
	create_remote_file('file a', 'content a updated')
	create_remote_file('file c', 'content c')
	synchronize(test_dir, test_dir)
	local_time_a = get_local_modified_time(test_dir, 'file a')
	remote_time_a = get_remote_modified_time(test_dir, 'file a')
	assert local_time_a > remote_time_a
	assert not local_file_exists('file b')
	assert local_file_exists('file c')
	assert not remote_file_exists('file b')
	
	
	
	# create_remote_file('file a', 'content a')
	# create_remote_file('file b', 'content b')
	# create_local_file('file c', 'content c')
	# create_local_file('file a', 'content a')
	
	#synchronize(test_dir, test_dir)
	#remote_time = service.get_file_properties(share, test_dir, 'file a').properties.last_modified
	# # remote_year = int(str(remote_time)[:4])
	# # remote_month = int(str(remote_time)[5:7])
	# # remote_day = int(str(remote_time)[8:10])
	# # remote_hour = int(str(remote_time)[11:13])
	# # remote_minute = int(str(remote_time)[14:16])
	# # remote_second = int(str(remote_time)[17:19])
	# print(time.struct_time(tm_year=remote_year, tm_mon=remote_month, tm_mday=remote_day, tm_hour=remote_hour, tm_min=remote_minute,
	#              tm_sec=remote_second, tm_wday=remote_second, tm_yday=255, tm_isdst=0))
	# unix = ((remote_year - 1970) * 365 * 24 * 60 * 60) + \
	#        (calculate_month_days(remote_month) * 24 * 60 * 60) + \
	#        (remote_day * 24 * 60 * 60) + \
	#        (remote_hour * 60 * 60) + \
	#        (remote_minute * 60) + \
	#        remote_second
	# print(unix)
	# print(os.path.getmtime(test_dir + '/' + 'file a'))
	# assert not os.path.exists('file c')
	# assert os.path.exists('file b')
	
	
	
	
#     - Delete
#         - Create two uniquely named remote files
#         - Create one local rile with the same name as a remote file
#         - Append the .DELETE suffix to the local file
#         - Synchronize
#         - Verify the local and corresponding remote files were both deleted
#     - Verify after each test that the remote 'last_upload' date was updated
# - Remote To Local
#     - Create two uniquely named remote files
#     - Create two uniquely named local files
#     - One of the local filenames must match a remote & have different content
#     - (same as above diagram)
#     - Make local 'last_download' date newer than remote 'last_upload'
#     - Synchronize
#     - Verify no files have changed, been created, or deleted
#     - Make remote 'last_upload' date newer than local 'last_download'
#     - Synchronize
#     - Verify local file with no corresponding remote is deleted
#     - Verify remote file with no corresponding local is downloaded locally
#     - Verify content of remote file with same name as local has been downloaded
# - Verify after each test that the local 'last_download' newer than 'last_upload'

if __name__ == '__main__':
	test_local_to_remote_upload()
	test_local_to_remote_delete()
	test_remote_to_local_download()
	delete_all_local_and_remote(create_dir=False)
	print('all tests succeeded')
	#service.create_file_from_text('songs', '', f'a,\'blah', 'Verse: Hello')
	#verify_file_uploaded(f'a,\'blah', 'Verse: Hello')
	#service.copy_file()
	#service.delete_file()
	#service.copy_file(self, share_name, directory_name, file_name, copy_source, metadata, timeout)
	#service.delete_file(self, share_name, directory_name, file_name, timeout)
	#service.create_file(self, share_name, directory_name, file_name, content_length, content_settings, metadata, timeout)
	
	
#
#  Experimental Code
#

# def upload_song(filename):
#     with open(f'songs/{filename}') as file:
#         song_text = file.read()
#     song = midi.Song(filename)
#     azure_filename = f'{filename} - {song.name}'
#     print(song.psalm)
#     if song.psalm:
#         azure_filename += f' - Psalm {song.psalm}'
#     service.create_file_from_text('songs', '', azure_filename, song_text)
#
# # for i in range(0, 400):
# #     service.delete_file('songs', '', f'cc {i}')
# #service.delete_file('songs', '', 'cc_008')
# #service.create_file_from_text('songs', '', f'a,\'blah', 'Verse: Hello')
# #service.delete_file('songs', '', 'CC 8 - Chide Me, O LORD, No Longer - 6')
#
#def synchronize_songs_with_server():
#    print('connected')
#    for file_or_dir in service.list_directories_and_files('songs'):
#        file  = service.get_file_properties('songs', '', file_or_dir.name)
#        print(f'{file.name}: {file.properties.last_modified}, '
#              f'{file.properties.content_length}')
#        #print(service.get_file_metadata('songs', '', file_or_dir.name))
#synchronize_songs_with_server()
#
# def enumerate_local_songs():
#     for song_filename in os.listdir('./songs'):
#         print(song_filename)
#         local_mtime = os.path.getmtime('./songs/' + song_filename)
#         print(datetime.datetime.fromtimestamp(local_mtime))
#
# # service.set_file_metadata('songs', '', 'cc_008',
# #                                {'name': 'Chide Me, O LORD, No Longer',
# #                                 'psalm': '6',
# #                                 'number': 'CC 8'})
#  #metadata = service.get_file_metadata('songs', '', 'cc_008')
# # song = service.get_file_to_text('songs', '', 'cc_008')
# #print(metadata)
#
# # Performance analysis on 400 songs
# # 0.9727 seconds to print names
# # 34.20828866958618 to print metadata

