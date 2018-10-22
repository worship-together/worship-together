from notes import *
import keys

name = "With All My Heart My Thanks I'll Bring"
number = "CC 150"
psalm = 110
beats_per_measure = 4
tempo = 120
key = keys.B_Flat

# jython representation
# beats_in_first_measure = 1
# soprano1p = [F4,  D4, E4, F4, B4,  B4, A4, A4, B4, C5, D5, E5, D5, C5]
# soprano1d = [QN, DQN, EN, QN, QN, DQN, EN, QN, QN, QN, QN, QN, QN, DHN]
# alto1p    = [D4,  B3, C4, D4, D4,  E4, E4, E4, F4, G4, F4, E4, F4, F4, EN4, F4]
# alto1d    = [QN, DQN, EN, QN, QN, DQN, EN, QN, QN, QN, QN, QN, QN, QN,  QN, QN]
# tenor1p   = [B3,  F3, B3, B3, D4,  C4, C4, C4, B3, B3, B3, B3, B3, C4,  B3, A3]
# tenor1d   = alto1d
# bass1p    = [B2,  B2, B2, B2, B2,  C3, C3, C3, D3, E3, F3, G3, B3, A3,  G3, F3]
# bass1d    = alto1d
# line1 = [zip(soprano1p, soprano1d), zip(alto1p, alto1d),
#          zip(tenor1p, tenor1d), zip(bass1p, bass1d)]

notes = [
    [
        [F4],
        [D4],
        [B3],
        [B2]
    ],
    [
        [D4(1.5), E4(0.5), F4, B4],
        [B3(1.5), C4(0.5), D4, D4],
        [F3(1.5), B3(0.5), B3, D4],
        [B2(1.5), B2(0.5), B2, B2]
    ],
    [
        [B4(1.5), A4(0.5), A4, B4],
        [E4(1.5), E4(0.5), E4, F4],
        [C4(1.5), C4(0.5), C4, B3],
        [C3(1.5), C3(0.5), C3, D3]
    ],
    [
        [C5, D5, E5, D5],
        [G4, F4, E4, F4],
        [B3, B3, B3, B3],
        [E3, F3, G3, B3]
    ],
    [
        [C5(3), R],
        [F4, E4n, F4, R],
        [C4, B3, A3, R],
        [A3, G3, F3, R]
    ]
]



