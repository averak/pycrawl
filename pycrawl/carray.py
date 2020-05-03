class carray(list):
    def xpath(self, locator, single=True):
        if self != []:
            return self[0].xpath(locator, single)
        else:
            return carray()

    def css(self, locator, single=True):
        if self != []:
            return self[0].css(locator, single)
        else:
            return carray()

    def attr(self, name):
        if self != []:
            return self[0].attr(name)
        else:
            return ''

    def inner_text(self, shaping=True):
        if self != []:
            return self[0].inner_text(shaping)
        else:
            return ''

    def outer_text(self):
        if self != []:
            return self[0].outer_text()
        else:
            return ''
