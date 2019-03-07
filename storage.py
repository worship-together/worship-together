"""
Storage

REQUIREMENTS
- Store song files locally for playback without Internet
- Automatically download updated songs from remote to iPad
  in background when Internet is available
- Delete songs from iPad that are no longer on remote
- Support manually uploading updated songs to remote from laptop
- Delete songs from remote that are no longer on laptop
- Songs are stored and versioned in git


DESIGN
- To upload from laptop to remote
  - Enumerate all local songs
    - If song does not exist on remote, copy it up to remote
    - If song on laptop is newer, copy it up to remote
  - Enumerate all remote songs
  	- If song does not exist on laptop, delete it from remote
  - Modify remote last_upload file
- To download from remote to iPad
  - If remote last_upload file newer than local last_download file
	- Enumerate all remote songs
      - If song does not exist on iPad, copy it from remote
	  - If song on remote is newer, copy it from remote
	- Enumerate all local songs
	  - If song does not exist on remote, delete it from iPad
	- Modify local last_download file


VERIFICATION
- Use a specific test directory on the local & remote
- All local & remote files are deleted before each test
- Upload Laptop To Remote
  - Create Song
    - Create a local song file
    - Invoke upload
    - Verify song file is on remote
  - Newer Local Song
    - Create a remote song file
    - Create a local song file with the same name and different content
    - Invoke upload
    - Verify remote song matches local song
  - Older Local Song
    - Create a local song file
    - Create a remote song file with the same name and different content
    - Invoke upload
    - Verify remote song does *not* match local song
  - Delete Song
    - Create a remote song file
    - Invoke upload
    - Verify remote song file is deleted
  - Verify after each test that remote last_upload file was updated
- Download Remote to iPad
  - Create Song
    - Create a remote song file
    - Invoke download
    - Verify song file is copied locally
  - Newer Remote Song
    - Create a local song file
    - Create a remote song file with the same name and different content
    - Invoke download
    - Verify local song matches remote song
  - Older Remote Song
    - Create a remote song file
    - Create a local song file with the same name and different content
    - Invoke download
    - Verify remote song does *not* match local song
  - Delete Song
    - Create a local song file
    - Invoke download
    - Verify local song file is deleted
  - Verify after each test that the local last_download file updated

OPEN QUESTIONS
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


def sync_upload_file(remote_dir, remote_file, local_file_path):
	service.create_file_from_path(share, remote_dir,
	                              remote_file, local_file_path)

def sync_upload_files(local_dir, remote_dir):
	for file in os.listdir(local_dir):
		if file.endswith(upload_suffix):
			new_name = file[:-(len(upload_suffix))]
			old_path = local_dir+'/'+file
			new_path = local_dir+'/'+new_name
			os.rename(old_path, new_path)
			sync_upload_file(remote_dir, new_name, new_path)
			
			
def sync_download_files(local_dir, remote_dir):
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


def sync_delete_remote_file(remote_dir, remote_file):
	service.delete_file(share, remote_dir, remote_file)


def sync_delete_files(local_dir, remote_dir):
	for file in os.listdir(local_dir):
		if file.endswith(delete_suffix) or not service.exists(share, directory_name=remote_dir, file_name=file):
			os.remove(local_dir+'/'+file)
			if service.exists(share, directory_name=remote_dir, file_name=file[:-(len(delete_suffix))]):
				sync_delete_remote_file(remote_dir, file[:-(len(delete_suffix))])
				
				
def synchronize(local_dir, remote_dir):
	sync_upload_files(local_dir, remote_dir)
	sync_delete_files(local_dir, remote_dir)
	sync_download_files(local_dir, remote_dir)


def local_file_exists(local_dir, name):
	return os.path.exists(local_dir + '/' + name)


def remote_file_exists(remote_dir, name):
	for file in service.list_directories_and_files(share, remote_dir):
		if file.name == name:
			return True
	return False


def upload_laptop_to_remote(local_dir, remote_dir):
	print("uploading local " + local_dir + " to remote " + remote_dir)
	for song in os.listdir(local_dir):
	# Create local song
		if local_file_exists(local_dir, song) is True:
			if remote_file_exists(remote_dir, song) is False:
				sync_upload_file(remote_dir, song, local_dir + '/' + song)
				if remote_file_exists(remote_dir, song) is True:
					print('newly uploaded ' + song)
	# Newer local song
			local_time = get_local_modified_time(local_dir, song)
			remote_time = get_remote_modified_time(remote_dir, song)
			if remote_time < local_time:
				sync_upload_file(remote_dir, song, local_dir + '/' + song)
				print('updated ' + song)
	# Delete song
	for song in service.list_directories_and_files(share, remote_dir):
		if local_file_exists(local_dir, song.name) is False and remote_file_exists(remote_dir, song.name) is True:
			sync_delete_remote_file(remote_dir, song.name)
			if remote_file_exists(remote_dir, song) is False:
				print('successfully deleted ' + song.name + ' from remote')
		else:
			print('nothing to delete')
	# Update last_upload time
	time.sleep(1)
	os.utime('songs/last_upload', (datetime.datetime.timestamp(datetime.datetime.now()),
									datetime.datetime.timestamp(datetime.datetime.now())))
	print('modified last_upload file')


#
# VERIFICATION
#

test_dir = 'test2'


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
	
	
def list_all_remote_files(remote_dir):
	for file in service.list_directories_and_files(share, remote_dir):
		print(file.name)


def verify_file_uploaded(name, content):
	file_found = False
	for file in service.list_directories_and_files(share, test_dir):
		assert not file_found
		assert file.name == name
		file_found = True
		remote = service.get_file_to_text(share, test_dir, name)
		if remote.content != content:
			print('remote content different from local content for ' + name + ':')
			print('remote content: ' + remote.content)
			print('local content: ' + content)
			assert remote.content == content
	assert file_found
	
	
def remote_file_deleted(name):
	file_found = False
	for file in service.list_directories_and_files(share, test_dir):
		if file.name == name:
			file_found = True
	return not file_found
	
	
def test_if_remote_file_exists(name):
	for file in service.list_directories_and_files(share, test_dir):
		if file.name == name:
			return True
	return False
	
	
def test_if_local_file_exists(name):
	return os.path.exists(test_dir + '/' + name)


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


def test_sync_local_to_remote_upload():
	delete_all_local_and_remote()
	create_local_file('file a.UPLOAD', 'content a')
	create_local_file('file b', 'content b')
	synchronize(test_dir, test_dir)
	verify_file_uploaded('file a', 'content a')
	assert test_if_local_file_exists('file a')
	assert not test_if_local_file_exists('file a.UPLOAD')
	assert not test_if_remote_file_exists('file b')
	
	
def test_sync_local_to_remote_delete():
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
	assert not test_if_local_file_exists('file d')
	assert not test_if_local_file_exists('file d.DELETE')
	assert remote_file_deleted('file d')
	assert not test_if_local_file_exists('file a')
	assert not test_if_local_file_exists('file a.DELETE')

	
def test_sync_remote_to_local_download():
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
	assert not test_if_local_file_exists('file b')
	assert test_if_local_file_exists('file c')
	assert not test_if_remote_file_exists('file b')
	

def test_upload_laptop_to_remote_create_song():
	delete_all_local_and_remote()
	create_local_file('new_file', 'new file content')
	upload_laptop_to_remote(test_dir, test_dir)
	assert test_if_remote_file_exists('new_file')


def test_upload_laptop_to_remote_newer_local_song():
	delete_all_local_and_remote()
	create_remote_file('new_file', 'new file content')
	create_local_file('new_file', 'new file with newer content')
	upload_laptop_to_remote(test_dir, test_dir)
	for file in os.listdir(test_dir):
		local_file = open(test_dir + '/' + file, 'r')
		for rem_file in service.list_directories_and_files(share, test_dir):
			remote_file = service.get_file_to_text(share, test_dir, rem_file.name)
			remote_content = remote_file.content
			local_content = local_file.read()
			assert remote_content == local_content
			local_file.close()


def test_upload_laptop_to_remote_older_local_song():
	delete_all_local_and_remote()
	create_remote_file('new_file', 'new file content')
	create_local_file('new_file', 'new file with older content')
	upload_laptop_to_remote(test_dir, test_dir)
	for file in os.listdir(test_dir):
		local_file = open(test_dir + '/' + file, 'r')
		for rem_file in service.list_directories_and_files(share, test_dir):
			remote_file = service.get_file_to_text(share, test_dir, rem_file.name)
			remote_content = remote_file.content
			local_content = local_file.read()
			print(remote_content)
			print(local_content)
			assert remote_content != local_content
			local_file.close()


def test_upload_laptop_to_remote_delete_song():
	delete_all_local_and_remote()
	create_remote_file('new_file', 'new file content')
	upload_laptop_to_remote(test_dir, test_dir)
	assert remote_file_deleted('new_file')
	assert not test_if_remote_file_exists('new_file')


if __name__ == '__main__':
	# service.create_directory(share, test_dir)
	# create_remote_file("my_file", "this is the day that the Lord has made")
	# list_all_remote_files(test_dir)
	#
	# upload_laptop_to_remote('songs', 'songs')
	# test_upload_laptop_to_remote_create_song()
	test_upload_laptop_to_remote_newer_local_song()
	test_upload_laptop_to_remote_older_local_song()
	# test_upload_laptop_to_remote_delete_song()
	#
	# test_sync_local_to_remote_upload()
	# test_sync_local_to_remote_delete()
	# test_sync_remote_to_local_download()
	delete_all_local_and_remote(create_dir=False)
	print('all tests succeeded')

