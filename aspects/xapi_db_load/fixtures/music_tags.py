"""
This is a pythonized version the testing CSV we use for tags in edx-platform.
"""
import csv
from io import StringIO

MUSIC_TAGS_CSV = StringIO("""id,value,parent_id,comments
WINDS,Wind instruments,,"This is an example Tag Import file, in CSV format."
PERCUSS,Percussion instruments,,"Only the 'id' and 'value' fields are required. They can be anything you like, but they must must be unique within the taxonomy. Existing tags matching 'id' will be updated on import."
ELECTRIC,Electronic instruments,,"Top-level tags have no 'parent_id', and you can have as many top-level tags as you wish."
STRINGS,String instruments,,"All other fields (like these 'comments') are ignored on import, and will not be included in subsequent tag exports."
BELLS,Idiophone,PERCUSS,"Providing a 'parent_id' creates a tag hierarchy."
DRUMS,Membranophone,PERCUSS,"The 'parent_id' must match an 'id' found earlier in the import file."
CAJÓN,Cajón,DRUMS,"Tag values may contain unicode characters."
PYLE,Pyle Stringed Jam Cajón,CAJÓN,"A tag hierarchy may contain as many as 3 levels. This tag is at level 4, and so it will not be shown to users."
THERAMIN,Theramin,ELECTRIC,"A tag hierarchy may contain uneven levels. Here, the Electronic branch has only 2 levels, while Percussion has 3."
CHORD,Chordophone,PERCUSS,
BRASS,Brass,WINDS,
WOODS,Woodwinds,WINDS,
FLUTE,Flute,WOODS,
PLUCK,Plucked strings,STRINGS,
MANDOLIN,Mandolin,PLUCK,
HARP,Harp,PLUCK,
BANJO,Banjo,PLUCK,
BOW,Bowed strings,STRINGS,
VIOLIN,Violin,BOW,
CELLO,Cello,BOW,
CLARINET,Clarinet,WOODS,
OBOE,Oboe,WOODS,
TRUMPET,Trumpet,BRASS,
TUBA,Tuba,BRASS,
SYNTH,Synthesizer,ELECTRIC,
CELESTA,Celesta,BELLS,
HI-HAT,Hi-hat,BELLS,
TABLA,Tabla,DRUMS,
PIANO,Piano,CHORD,
""")

MUSIC_TAGS = csv.DictReader(MUSIC_TAGS_CSV)
