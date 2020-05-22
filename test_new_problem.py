import os
from pathlib import Path
from unittest import TestCase

from new_problem import Args, SCRIPT_PATH

class TestArgs(TestCase):

  def test_constructor_from_root(self):
    # Test valid construction.
    a = Args("TestComp", "2018", "TestRound", "TestProblem", True)
    assert(a.competition == "TestComp")
    assert(a.year == 2018)
    assert(a.round_name == "TestRound")
    assert(a.prob_name == "TestProblem")
    assert(a.interactive == True)
    a = Args("TestComp", "2017", "TestRound", "TestProblem", False)
    assert(a.competition == "TestComp")
    assert(a.year == 2017)
    assert(a.round_name == "TestRound")
    assert(a.prob_name == "TestProblem")
    assert(a.interactive == False)

    # Year not an int.
    with self.assertRaises(ValueError):
      a = Args("TestComp", "NotAnInt", "TestRound", "TestProblem", False)

    # Year not big enough for interactive.
    with self.assertRaises(ValueError):
      a = Args("TestComp", "2017", "TestRound", "TestProblem", True)

    # Missing arguments.
    with self.assertRaises(KeyError):
      a = Args(None, "2020", "TestRound", "TestProblem", False)
    with self.assertRaises(KeyError):
      a = Args("TestComp", None, "TestRound", "TestProblem", False)
    with self.assertRaises(KeyError):
      a = Args("TestComp", "2020", None, "TestProblem", False)
    with self.assertRaises(KeyError):
      a = Args("TestComp", "2020", "TestRound", None, False)

  def test_constructor_from_competition_folder(self):
    prev_cwd = Path.cwd()
    # Make a new folder in the SCRIPT_PATH directory.
    # Change CWD to that folder.
    # Do the tests.
    # Change CWD back.
    return "blah"
