"""Use Flag Mechanics """

import random
import re
import math
from subprocess import *

from .tool import unique
import portage

def flag_is_active(flag):
    if flag.startswith('-'):
        return False
    return True

## Useflag Combis ##
def findUseFlagCombis (package, config):
    """
    Generate combinations of use flags to test
    The output will be a list each containing a ready to use USE=... string
    """
    atom = portage.versions.best(portage.portdb.match(package.packageString()))
    uselist, required_use = portage.portdb.aux_get(atom, ['IUSE', 'REQUIRED_USE'])
    uselist = uselist.split()

    for i in config['ignoreprefix']:
        uselist=[u for u in uselist if not re.match(i,u)]

    swlist = list(range(2**len(uselist)))

    usecombis=[]
    for sw in swlist:
        mod = []
        for pos in range(len(uselist)):
            if ((2**pos) & sw):
                mod.append("")
            else:
                mod.append("-")
        usecombis.append(list(zip(mod, uselist)))

    allcombis = []
    for c in usecombis:
        c = ["".join(uf) for uf in c]
        if portage.dep.check_required_use(required_use, c, uselist.__contains__).__bool__() is True:
            allcombis.append(c)

    usecombis = []

    random.seed()
    n = config['usecombis']
    c = 0
    while c < n and len(allcombis) > 0:
        usecombis.append(allcombis.pop(random.randint(0, len(allcombis)-1)))
        c += 1

    # include all-on and all-off if not already included
    if len(allcombis) > 0:
        usecombis.append(allcombis.pop(0))
    if len(allcombis) > 0:
        usecombis.append(allcombis.pop())

    # Merge everything to a USE="" string
    return ["USE=\'"+" ".join(uc)+ "\'" for uc in usecombis]
