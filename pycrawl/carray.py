class carray(list):
    def xpath(self, locator, single=True):
        if self != []:
            return self[0].xpath(locator, single)
        else:
            return pycrawl(doc=None).xpath(locator, single)

    def css(self, locator, single=True):
        print(locator)
        if self != []:
            return self[0].css(locator, single)
        else:
            return pycrawl(doc=None).css(locator, single)
