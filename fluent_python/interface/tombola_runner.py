"""
@author: magician
@file:   tombola_runner.py
@date:   2020/11/15
"""
import doctest

from fluent_python.interface.tombola import Tombola
from fluent_python.interface import bingo, lotto, tombolist

TEST_FILE = 'tombola_tests.rst'
TEST_MSG = '{0:16} {1.attempted:2} tests, {1.failed:2} failed - {2}'


def main(argv):
    """
    main
    @param argv:
    @return:
    """
    verbose = '-v' in argv
    real_subclass = Tombola.__subclasses__()
    virtual_classes = list(Tombola._abc_registry)

    for cls in real_subclass + virtual_classes:
        test(cls, verbose)


def test(cls, verbose=False):
    """
    test
    @param cls:
    @param verbose:
    @return:
    """
    res = doctest.testfile(
        TEST_FILE,
        globs={'ConcreteTombola': cls},
        verbose=verbose,
        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
    )
    tag = 'FAIL' if res.failed else 'OK'
    print(TEST_MSG.format(cls.__name__, res, tag))


if __name__ == '__main__':
    import sys
    main(sys.argv)
