l = [1332, 1898, 1687, 1539, 1198, 1617, 1809, 1128, 1528, 1251, 1344, 1490, 1964, 1936, 1283, 1395, 1735, 1834, 1312, 1641, 1526, 1518, 1331, 1512, 1231, 1554, 1117, 1425, 1361, 1020, 1479, 1680, 1676, 1783, 1608, 1506, 1352]




if __name__ == "__main__":
    print len(l)
    sl = sorted(l)
    #print sl
    st = 0
    for i in xrange(0,len(sl) ):
        if sl[i] > 1500:
            st = i
            break
    print sl[st:]