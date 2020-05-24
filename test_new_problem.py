import os
import shutil
from pathlib import Path
from unittest import TestCase

from new_problem import Args, SCRIPT_PATH

TEST_PATH = Path(__file__).parent.resolve()

#
# Context managers

class Cwd(): 
  def __init__(self, new_cwd): 
    self.new_cwd = new_cwd
    self.old_cwd = None
        
  def __enter__(self): 
    self.old_cwd = Path.cwd()
    os.chdir(self.new_cwd)       
    return self
    
  def __exit__(self, exc_type, exc_value, exc_traceback): 
    os.chdir(self.old_cwd)

class TestFolders():
  def __init__(self, tree):
    '''
    The constructor takes a tree representing the desired test folder structure,
    with the root representing TEST_PATH.
    '''
    self.tree = tree 
    self.tree.path = SCRIPT_PATH

  def __enter__(self):
    # Create test folder structure.
    for c in self.tree.children:
      self.recursive_make_tree(c, self.tree)
    # Return tree where nodes contain paths.
    return self.tree 

  def __exit__(self, exc_type, exc_value, exc_traceback):
    # Remove all test directories.
    for c in self.tree.children:
      shutil.rmtree(c.path)

  def recursive_make_tree(self, node, parent):
    assert(parent.path != None)
    node.path = self.new_folder(node.prefix, parent.path)
    for c in node.children:
      self.recursive_make_tree(c, node)
    return node

  def new_folder(self, prefix, path):
    '''
    Makes a new folder in the given directory, and then returns its path.
    '''
    if not path.is_dir():
      raise Exception("path isn't a directory")
    folder = prefix
    suffix = 0
    new_folder = path / (folder + str(suffix))
    while new_folder.is_dir():
      suffix += 1
      new_folder = path / (folder + str(suffix))
    new_folder.mkdir()
    return new_folder

class Node():
  def __init__(self, prefix, children):
    self.children = children
    self.prefix   = prefix
    self.path     = None

  def set_path(self, path):
    self.path = path

#
# Test cases.

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

  def test_folders_context(self):
    comp1_year1 = Node("Year", [])
    comp1_year2 = Node("Year", [])
    comp1 = Node("Comp", [comp1_year1, comp1_year2])
    comp2_year1 = Node("Year", [])
    comp2 = Node("Comp", [comp2_year1])
    root = Node("root", [comp1, comp2])
    with TestFolders(root) as test_folders:
      assert(len(test_folders.children) == 2) # There are two competition folders.
      for c in test_folders.children:
        c.path.is_dir()
      assert(comp1 == test_folders.children[0])
      assert(comp2 == test_folders.children[1])
      assert(len(comp1.children) == 2) # Comp1 has two year folders.
      assert(len(comp2.children) == 1) # Comp2 has one year folder.

  def test_constructor_from_competition_folder(self):
    comp = Node("Comp", [])
    root = Node("root", [comp])
    with TestFolders(root) as test_folders:
      comp_name = comp.path.parts[-1]
      # Move to competition folder
      with Cwd(comp.path) as cwd:
        # Missing competition name.
        a = Args(None, "2017", "TestRound", "TestProblem", False)
        assert(a.competition == comp_name)
        assert(a.year == 2017)
        assert(a.round_name == "TestRound")
        assert(a.prob_name == "TestProblem")
        assert(a.interactive == False)
        # Specified competition name.
        a = Args("OtherComp", "2017", "TestRound", "TestProblem", False)
        assert(a.competition == "OtherComp")
        assert(a.year == 2017)
        assert(a.round_name == "TestRound")
        assert(a.prob_name == "TestProblem")
        assert(a.interactive == False)