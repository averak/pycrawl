class carray(list):
    def xpath(self, locater, single=True):
        if self != []:
            return self[0].xpath(locator, single)
        else:
            return pycrawl(doc=None).xpath(locater, single)

