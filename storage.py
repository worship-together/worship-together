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

import sys
from azure.storage.file import FileService
import datetime
import os
import shutil
import time
import abc


#
#  IMPLEMENTATION
#

service = FileService(
    account_name='worshiptogether',
    account_key='33TG6/7zK8TmKHmlSRthHpGxve8YJfu3M9ut77vn0lUy'
                'B2ZQqfL8ZdDiucbB8MAyg59707Mcxywhy2fFG/ISZA==')
share = 'songs'

last_upload_filename = 'last_upload'


class Device(abc.ABC):

	def __init__(self, local_dir, remote_dir):
		self.local_dir = local_dir
		self.remote_dir = remote_dir

	@abc.abstractmethod
	def synchronize(self):
		pass

	def upload_file_to_remote(self, remote_file, local_file_path):
		service.create_file_from_path(share, self.remote_dir,
									  remote_file, local_file_path)

	def delete_remote_file(self, remote_file):
		service.delete_file(share, self.remote_dir, remote_file)

	def get_local_modified_time(self, file):
		mtime = os.path.getmtime(self.local_dir + '/' + file)
		dtime = datetime.datetime.fromtimestamp(mtime, datetime.timezone.utc)
		return dtime.replace(microsecond=0)

	def get_remote_modified_time(self, file):
		dtime = service.get_file_properties(share, self.remote_dir, file).properties.last_modified
		return dtime.replace(microsecond=0)

	def local_file_exists(self, name):
		return os.path.isfile(self.local_dir + '/' + name)

	def remote_file_exists(self, name):
		for file in service.list_directories_and_files(share, self.remote_dir):
			if file.name == name:
				return True
		return False

	def create_remote_file(self, name, content):
		service.create_file_from_text(share, self.remote_dir, name, content)

	def create_local_file(self, name, content):
		with open(test_dir + '/' + name, 'w') as file:
			file.write(content)

	def list_all_remote_files(self):
		for file in service.list_directories_and_files(share, self.remote_dir):
			print(file.name)

	def remote_file_deleted(self, name):
		file_found = False
		for file in service.list_directories_and_files(share, self.remote_dir):
			if file.name == name:
				file_found = True
		return not file_found

	def test_if_remote_file_exists(self, name):
		for file in service.list_directories_and_files(share, self.remote_dir):
			if file.name == name:
				return True
		return False

	def delete_all_local_and_remote(self, create_dir=True):
		if os.path.exists(self.local_dir):
			shutil.rmtree(self.local_dir)
		if create_dir:
			os.mkdir(self.local_dir)
		if service.exists(share, self.remote_dir):
			for file in service.list_directories_and_files(share, self.remote_dir):
				service.delete_file(share, self.remote_dir, file.name)
			service.delete_directory(share, self.remote_dir)
		if create_dir:
			service.create_directory(share, self.remote_dir)


class iPad(Device):
	def synchronize(self):
		self.sync_delete_files()
		self.sync_download_files()

	def sync_delete_files(self):
		for file in os.listdir(self.local_dir):
			if not service.exists(share, directory_name=self.remote_dir, file_name=file):
				os.remove(self.local_dir + '/' + file)

	def sync_download_files(self):
		for file in service.list_directories_and_files(share, self.remote_dir):
			if os.path.exists(self.local_dir + '/' + file.name):
				local_time = self.get_local_modified_time(file.name)
				remote_time = self.get_remote_modified_time(file.name)
				if remote_time > local_time:
					service.get_file_to_path(share, self.remote_dir, file.name, self.local_dir + '/' + file.name)
					time.sleep(1)
					os.utime(self.local_dir + '/' + file.name, (datetime.datetime.timestamp(datetime.datetime.now()),
														   datetime.datetime.timestamp(datetime.datetime.now())))
			else:
				service.get_file_to_path(share, self.remote_dir, file.name, self.local_dir + '/' + file.name)
				time.sleep(1)
				os.utime(self.local_dir + '/' + file.name, (datetime.datetime.timestamp(datetime.datetime.now()),
													   datetime.datetime.timestamp(datetime.datetime.now())))

	def verify_file_uploaded(self, name, content):
		file_found = False
		for file in service.list_directories_and_files(share, self.remote_dir):
			assert not file_found
			assert file.name == name
			file_found = True
			remote = service.get_file_to_text(share, self.remote_dir, name)
			if remote.content != content:
				print('remote content different from local content for ' + name + ':')
				print('remote content: ' + remote.content)
				print('local content: ' + content)
				assert remote.content == content
		assert file_found

	def test_if_local_file_exists(self, name):
		return os.path.exists(self.local_dir + '/' + name)

	@staticmethod
	def local_to_remote_upload():
		ipad = iPad(test_dir, test_dir)
		ipad.delete_all_local_and_remote()
		ipad.create_local_file('file a.UPLOAD', 'content a')
		ipad.create_local_file('file b', 'content b')
		ipad.synchronize()
		ipad.verify_file_uploaded('file a', 'content a')
		assert ipad.test_if_local_file_exists('file a')
		assert not ipad.test_if_local_file_exists('file a.UPLOAD')
		assert not ipad.test_if_remote_file_exists('file b')

	@staticmethod
	def local_to_remote_delete():
		ipad = iPad(test_dir, test_dir)
		ipad.delete_all_local_and_remote()
		ipad.create_local_file('file a.DELETE', 'content a')
		ipad.create_local_file('file b', 'content b')
		ipad.create_local_file('file d.DELETE', 'content d')
		ipad.create_remote_file('file a', 'content a')
		ipad.create_remote_file('file b', 'content b')
		ipad.create_remote_file('file c', 'content c')
		ipad.synchronize()
		assert ipad.remote_file_deleted('file a')
		assert not ipad.remote_file_deleted('file b')
		assert not ipad.remote_file_deleted('file c')
		assert not ipad.test_if_local_file_exists('file d')
		assert not ipad.test_if_local_file_exists('file d.DELETE')
		assert ipad.remote_file_deleted('file d')
		assert not ipad.test_if_local_file_exists('file a')
		assert not ipad.test_if_local_file_exists('file a.DELETE')

	@staticmethod
	def remote_to_local_download():
		ipad = iPad(test_dir, test_dir)
		ipad.delete_all_local_and_remote()
		ipad.create_local_file('file a', 'content a outdated')
		ipad.create_local_file('file b', 'content b')
		time.sleep(1)
		ipad.create_remote_file('file a', 'content a updated')
		ipad.create_remote_file('file c', 'content c')
		ipad.synchronize()
		local_time_a = ipad.get_local_modified_time('file a')
		remote_time_a = ipad.get_remote_modified_time('file a')
		assert local_time_a > remote_time_a
		assert not ipad.test_if_local_file_exists('file b')
		assert ipad.test_if_local_file_exists('file c')
		assert not ipad.test_if_remote_file_exists('file b')

	@staticmethod
	def test():
		iPad.local_to_remote_upload()
		iPad.local_to_remote_delete()
		iPad.remote_to_local_download()

class Laptop(Device):
	def synchronize(self):
		for song in os.listdir(self.local_dir):
			if self.local_file_exists(song):
				if not self.remote_file_exists(song):
					self.upload_file_to_remote(song, self.local_dir + '/' + song)
				else:
					local_time = self.get_local_modified_time(song)
					remote_time = self.get_remote_modified_time(song)
					if local_time > remote_time:
						self.upload_file_to_remote(song, self.local_dir + '/' + song)
		for song in service.list_directories_and_files(share, self.remote_dir):
			if not self.local_file_exists(song.name):
				self.delete_remote_file(song.name)
		time.sleep(1)
		os.utime('songs/last_upload', (datetime.datetime.timestamp(datetime.datetime.now()),
									   datetime.datetime.timestamp(datetime.datetime.now())))

	def get_local_file_content(self, filename):
		with open(self.local_dir + '/' + filename, 'r') as file:
			return file.read()

	def get_remote_file_content(self, remote_file):
		return service.get_file_to_text(share, self.remote_dir, remote_file.name).content

	@staticmethod
	def test_create_song():
		laptop = Laptop(test_dir, test_dir)
		laptop.delete_all_local_and_remote()
		laptop.create_local_file('new_file', 'new file content')
		laptop.synchronize()
		assert laptop.test_if_remote_file_exists('new_file')

	@staticmethod
	def test_delete_song():
		laptop = Laptop(test_dir, test_dir)
		laptop.delete_all_local_and_remote()
		laptop.create_remote_file('new_file', 'new file content')
		laptop.synchronize()
		assert laptop.remote_file_deleted('new_file')
		assert not laptop.test_if_remote_file_exists('new_file')

	@staticmethod
	def test_newer_local_song():
		laptop = Laptop(test_dir, test_dir)
		laptop.delete_all_local_and_remote()
		laptop.create_remote_file('new_file', 'new file content')
		print('waiting for local clock to exceed remote clock')
		time.sleep(5)
		laptop.create_local_file('new_file', 'new file with newer content')
		remote_time = laptop.get_remote_modified_time('new_file')
		local_time = laptop.get_local_modified_time('new_file')
		assert remote_time < local_time
		laptop.synchronize()
		for local_file in os.listdir(test_dir):
			local_content = laptop.get_local_file_content(local_file)
			for remote_file in service.list_directories_and_files(share, test_dir):
				if remote_file.name != last_upload_filename:
					assert local_file == remote_file.name
					remote_content = laptop.get_remote_file_content(remote_file)
					assert remote_content == local_content

	@staticmethod
	def test_older_local_song():
		laptop = Laptop(test_dir, test_dir)
		laptop.delete_all_local_and_remote()
		laptop.create_local_file('new_file', 'new file with older content')
		print('waiting for remote clock to exceed local clock')
		time.sleep(15)
		laptop.create_remote_file('new_file', 'new file content')
		local_time = laptop.get_local_modified_time('new_file')
		remote_time = laptop.get_remote_modified_time('new_file')
		assert local_time < remote_time
		Laptop(test_dir, test_dir).synchronize()
		for local_file in os.listdir(test_dir):
			local_content = laptop.get_local_file_content(local_file)
			for remote_file in service.list_directories_and_files(share, test_dir):
				if remote_file.name != last_upload_filename:
					assert local_file == remote_file.name
					remote_content = laptop.get_remote_file_content(remote_file)
					assert remote_content != local_content

	@staticmethod
	def test():
		Laptop.test_create_song()
		Laptop.test_newer_local_song()
		Laptop.test_older_local_song()
		Laptop.test_delete_song()



#
# VERIFICATION
#

test_dir = 'test'

if __name__ == '__main__':
	Laptop.test()
	iPad.test()
	laptop = Laptop(test_dir, test_dir)
	laptop.delete_all_local_and_remote(create_dir=False)
	print('all tests succeeded')
