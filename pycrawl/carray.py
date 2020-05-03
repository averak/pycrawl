class carray(list):
    def xpath(self, locator, single=True):
        if self != []:
            return self[0].xpath(locator, single)
        else:
            return pycrawl(doc=None).xpath(locator, single)

    def css(self, locator, single=True):
        if self != []:
            return self[0].css(locator, single)
        else:
            return pycrawl(doc=None).css(locator, single)

    def attr(self, name):
        if self != []:
            return self[0].attr(name)
        else:
            return pycrawl(doc=None).attr(name)

    def inner_text(self, shaping=True):
        if self != []:
            return self[0].inner_text(shaping)
        else:
            return pycrawl(doc=None).inner_text(shaping)

    def outer_text(self):
        if self != []:
            return self[0].outer_text()
        else:
            return pycrawl(doc=None).outer_text()
