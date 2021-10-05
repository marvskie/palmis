# Organizations
ADMIN = 'admin'
CAMB = 'camb'
EB = 'eb'
EXECUTIVE = 'exe'
FPB = 'pb'
LSDB = 'lsdb'
LOB = 'lob'
MB = 'mb'
PPB = 'ppb'
SAMB = 'samb'
TOSB = 'tosb'

ASCOM = 'ascom'
PAMU = 'pamu'
FSSU = 'fssu'

PPB_CHIEF = 'ppb_c'


OG4 = [ADMIN, CAMB, EB, EXECUTIVE, FPB, LSDB, LOB, MB, PPB, SAMB, TOSB]
HPA = OG4 + [ASCOM]


def is_og4(code):
    return code in OG4


def is_hpa(code):
    return code in HPA
