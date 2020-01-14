"""
@author: magician
@file:   getset_demo.py
@date:   2020/1/13
"""


class OldResistor(object):
    """
    OldResistor
    """
    def __init__(self, ohms):
        self._ohms = ohms

    def get_ohms(self):
        return self._ohms

    def set_ohms(self, ohms):
        self._ohms = ohms


class Resistor(object):
    """
    Resistor
    """
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0


class VoltageResistance(Resistor):
    """
    VoltageResistance
    """
    def __init__(self, ohms):
        super().__init__(ohms)
        self._voltage = 0

    @property
    def voltage(self):
        return self._voltage

    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms


class BoundedResistance(Resistor):
    """
    BoundedResistance
    """
    def __init__(self, ohms):
        super().__init__(ohms)

    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms


class FixedResistance(Resistor):
    """
    FixedResistance
    """
    @property
    def ohms(self):
        return self._ohms

    @ohms.setter
    def ohms(self, ohms):
        if hasattr(self, '_ohms'):
            raise AttributeError("Can't set attribute")
        self._ohms = ohms


if __name__ == '__main__':
    r0 = OldResistor(50e3)
    print('Before: %5r' % r0.get_ohms())
    r0.set_ohms(10e3)
    print('After: %5r' % r0.get_ohms())
    r0.set_ohms(r0.get_ohms() + 5e3)

    r1 = Resistor(50e3)
    r1.ohms += 5e3

    r2 = VoltageResistance(1e3)
    print('Before: %5r amps' % r2.current)
    r2.voltage = 10
    print('After: %5r amps' % r2.current)

    r3 = BoundedResistance(1e3)
    try:
        r3.ohms = 0
    except Exception as e:
        print(e)
    try:
        BoundedResistance(-5)
    except Exception as e:
        print(e)

    r4 = FixedResistance(1e3)
    try:
        r4.ohms = 2e3
    except Exception as e:
        print(e)
