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


#
#  IMPLEMENTATION
#

service = FileService(
    account_name='worshiptogether',
    account_key='33TG6/7zK8TmKHmlSRthHpGxve8YJfu3M9ut77vn0lUy'
                'B2ZQqfL8ZdDiucbB8MAyg59707Mcxywhy2fFG/ISZA==')
share = 'songs'


def synchronize(local_dir, remote_dir):
    pass


#
# VERIFICATION
#

test_dir = 'test'


def delete_all_local_and_remote():
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)
    if service.exists(share, test_dir):
        service.delete_directory(share, test_dir)
    service.create_directory(share, test_dir)


def create_local_file(name, content):
    with open(test_dir + '/' + name, 'w') as file:
        file.write(content)


def verify_file_uploaded(name, content):
    file_found = False
    for file in service.list_directories_and_files(share, test_dir):
        assert not file_found
        assert file.name == name
        file_found = True
        remote_content = service.get_file_to_text(share, test_dir, name)
        assert remote_content == content
    assert file_found


def test_local_to_remote_upload():
    delete_all_local_and_remote()
    create_local_file('file a.UPLOAD', 'content a')
    create_local_file('file b', 'content b')
    synchronize(test_dir, test_dir)
    verify_file_uploaded('file a', 'content a')
    assert os.path.exists('file a')
    assert not os.path.exists('file a.UPLOAD')


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
# def synchronize_songs_with_server():
#     print('connected')
#     for file_or_dir in service.list_directories_and_files('songs'):
#         file  = service.get_file_properties('songs', '', file_or_dir.name)
#         print(f'{file.name}: {file.properties.last_modified}, '
#               f'{file.properties.content_length}')
#         #print(service.get_file_metadata('songs', '', file_or_dir.name))
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
# #metadata = service.get_file_metadata('songs', '', 'cc_008')
# # song = service.get_file_to_text('songs', '', 'cc_008')
# #print(metadata)
#
# # Performance analysis on 400 songs
# # 0.9727 seconds to print names
# # 34.20828866958618 to print metadata
