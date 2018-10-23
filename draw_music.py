"""
Draw Music

REQUIREMENTS
- Draw all notes for a given song on the staff

DESIGN
- Draw five evenly spaced black horizontal lines
- Leave a gap below the same height as all five lines
- Draw five more evenly spaced black horizontal lines
- Draw one small oval for each soprano note on or between appropriate line(s)
  - Use type of note to determine where to draw oval
- Leave a reasonable amount of horizontal space between notes
"""

import midi

song = [song for song in midi.songs if '334' in str(song)][0]
print(song)

for measure in song.measures:
    soprano = measure[midi.Voice.Soprano]
    for note in soprano:
        if type(note) is type:
            note_name = note.__name__
        else:
            note_name = type(note).__name__
        print(note_name)
