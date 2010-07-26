"""Use Flag Mechanics """

import random
from subprocess import *

from tool import unique

## Useflag Combis ##
def findUseFlagCombis (package, ignoreprefix):
    """
    Generate combinations of use flags to test
    The output will be a list each containing a ready to use USE=... string
    """
    uses=Popen('equery -C uses '+package.packageString()+' | cut -f 1 | cut -c 2-40 | xargs',
               shell=True, stdout=PIPE).communicate()[0]
    uselist=uses.split()
    # The uselist could have duplicates due to slot-conditional
    # output of equery
    uselist=unique(uselist)
    for i in ignoreprefix:
        uselist=[u for u in uselist if not re.match(i,u)]

    if len(uselist) > 4:
        # More than 4 use flags, generate 16 random strings and everything -, everything +
        s = 2**(len (uselist))
        random.seed()
        swlist = [random.randint(0, s-1) for i in range (16)]
        swlist.append(0)
        swlist.append(s-1)
        swlist.sort()
        swlist = unique(swlist)
    else:
        # 4 or less use flags. Generate all combinations
        swlist = range(2**len(uselist))

    usecombis=[]
    for sw in swlist:
        mod = []
        for pos in range(len(uselist)):
            if ((2**pos) & sw):
                mod.append("")
            else:
                mod.append("-")
        usecombis.append(zip(mod, uselist))

    usecombis = [["".join(uf) for uf in combi] for combi in usecombis]

    # Merge everything to a USE="" string
    return ["USE=\""+" ".join(uc)+ "\"" for uc in usecombis]