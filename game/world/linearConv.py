def linearConv(oR, nR, val): #oR and nR should be tuples, low to high
    oldRange = oR[1] - oR[0]
    newRange = nR[1] - nR[0]
    ret = (((val - oR[0])*newRange) / oldRange) + nR[0]
    return round(ret)