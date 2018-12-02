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
- Whenever a song is renamed locally, append ".RENAME." followed by new name
- Remote contains file named 'last_upload'
    - Modified after each upload
- Local file named 'last_download'
    - Modified time is updated to match 'last_upload' modified time
- Periodically compare modified time of 'last_upload' with 'last_download'
- If times differ:
    - Generate a set of the union of all unique local and remote song filenames
        - Filenames do not include '.UPLOAD' or '.DELETE' suffixes
    - For each filename:
        - If local file exists:
            - If file has '.UPLOAD' suffix:
                - Remove suffix
                - Upload file to remote
                - Set modified time of local file to match remote
            - Else if file has '.DELETE' suffix:
                - Delete remote file
                - Delete local file as well
            - Else if file has '.RENAME' suffix:
                - Rename remote file
                - Rename local file
                - Upload file to remote, in case it has been modified
                - Set modified time of local file to match remote
            - Else if remote file does not exist
                - Delete local file
            - Else if remote file has newer modified time
                - Overwrite local file with remote
                - Set modified time of local file to match remote
        - Else:
            - Download remote file
            - Set modified time of local file to match remote

VERIFICATION
- Create several local and remote files with the same name & modified date
    - Verify after each test that these files were not updated
- Synchronization Trigger
    - Create remote file with no corresponding local file
    - Set local last_download and remote last_upload to same modified date
    - Synchronize and verify that no local file was created
    - Set remote last_upload to a newer modified date
    - Synchronize and verify that the local file was created
- Upload
    - Set local last_download and remote last_upload to same modified date
    - Create local file w/'.UPDATED' suffix, no corresponding remote file
        - Synchronize and verify remote file was created with same name
        - Also verify that local file has same modified date as remote
    - Create local file w/'.DELETED' suffix and corresponding remote file
        - Synchronize and verify both local and remote files are deleted
    - Create local file w/'.RENAME.' suffix and corresponding remote file
        - Synchronize and verify both local and remote files are renamed
        - Also verify that local file has same modified date as remote
- Download
    - Create a local file with no corresponding remote file
        - Set local last_download and remote last_upload to same modified date
        - Synchronize, verify that the local file is not deleted
        - Make remote last_upload newer
        - Synchronize, verify that the local file is deleted
    - Create corresponding older local and newer remote files, different sizes
        - Set local last_download and remote last_upload to same modified date
        - Synchronize, verify that the modified dates do not change
        - Make remote last_upload newer
        - Synchronize, veriy that the local file is overwitten & date updated

OPEN QUESTIONS
- How to access Azure from iPad? (limited set of azure Python libs?)
- How are file times represented on iPad?
- How to update in background?
- How to detect that an Internet connection is available?
"""

from azure.storage.file import FileService
import midi
import datetime
import os

file_service = FileService(
    account_name='worshiptogether',
    account_key='33TG6/7zK8TmKHmlSRthHpGxve8YJfu3M9ut77vn0lUy'
                'B2ZQqfL8ZdDiucbB8MAyg59707Mcxywhy2fFG/ISZA==')

def upload_song(filename):
    with open(f'songs/{filename}') as file:
        song_text = file.read()
    song = midi.Song(filename)
    azure_filename = f'{filename} - {song.name}'
    print(song.psalm)
    if song.psalm:
        azure_filename += f' - Psalm {song.psalm}'
    file_service.create_file_from_text('songs', '', azure_filename, song_text)

# for i in range(0, 400):
#     file_service.delete_file('songs', '', f'cc {i}')
#file_service.delete_file('songs', '', 'cc_008')
#file_service.create_file_from_text('songs', '', f'a,\'blah', 'Verse: Hello')
#file_service.delete_file('songs', '', 'CC 8 - Chide Me, O LORD, No Longer - 6')

def synchronize_songs_with_server():
    print('connected')
    for file_or_dir in file_service.list_directories_and_files('songs'):
        file  = file_service.get_file_properties('songs', '', file_or_dir.name)
        print(f'{file.name}: {file.properties.last_modified}, '
              f'{file.properties.content_length}')
        #print(file_service.get_file_metadata('songs', '', file_or_dir.name))

def enumerate_local_songs():
    for song_filename in os.listdir('./songs'):
        print(song_filename)
        local_mtime = os.path.getmtime('./songs/' + song_filename)
        print(datetime.datetime.fromtimestamp(local_mtime))

# file_service.set_file_metadata('songs', '', 'cc_008',
#                                {'name': 'Chide Me, O LORD, No Longer',
#                                 'psalm': '6',
#                                 'number': 'CC 8'})
#metadata = file_service.get_file_metadata('songs', '', 'cc_008')
# song = file_service.get_file_to_text('songs', '', 'cc_008')
#print(metadata)

if __name__ == '__main__':
    # upload_song('cc_312')
    synchronize_songs_with_server()
    enumerate_local_songs()

# Performance analysis on 400 songs
# 0.9727 seconds to print names
# 34.20828866958618 to print metadata
