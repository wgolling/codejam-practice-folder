import os
import shutil
from pathlib import Path
from unittest import TestCase

from new_problem import Args, FolderMaker, process_input

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
    self.tree.path = TEST_PATH

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
      # Move to competition folder.
      with Cwd(comp.path) as cwd:
        # Missing competition name.
        a = Args(None, "2017", "TestRound", "TestProblem", False)
        assert(a.competition == comp_name)
        assert(a.year == 2017)
        assert(a.round_name == "TestRound")
        assert(a.prob_name == "TestProblem")
        assert(a.interactive == False)
        # Specified different input.
        a = Args("OtherComp", "2017", "TestRound", "TestProblem", False)
        assert(a.competition == "OtherComp")
        assert(a.year == 2017)
        assert(a.round_name == "TestRound")
        assert(a.prob_name == "TestProblem")
        assert(a.interactive == False)

  def test_constructor_from_year_folder(self):
    year = Node("2020", [])
    comp = Node("Comp", [year])
    root = Node("root", [comp])
    with TestFolders(root) as test_folders:
      year_name = year.path.parts[-1]
      comp_name = comp.path.parts[-1]
      # Move to year folder.
      with Cwd(year.path) as cwd:
        # Missing competition and year.
        a = Args(None, None, "TestRound", "TestProblem", False)
        assert(a.competition == comp_name)
        assert(a.year == int(year_name))
        assert(a.round_name == "TestRound")
        assert(a.prob_name == "TestProblem")
        assert(a.interactive == False)
        # Specified different input.
        a = Args("OtherComp", "2017", "TestRound", "TestProblem", False)
        assert(a.competition == "OtherComp")
        assert(a.year == 2017)
        assert(a.round_name == "TestRound")
        assert(a.prob_name == "TestProblem")
        assert(a.interactive == False)

  def test_constructor_from_round_folder(self):
    rnd = Node("Round", [])
    year = Node("2020", [rnd])
    comp = Node("Comp", [year])
    root = Node("root", [comp])
    with TestFolders(root) as test_folders:
      round_name = rnd.path.parts[-1]
      year_name = year.path.parts[-1]
      comp_name = comp.path.parts[-1]
      # Move to round folder
      with Cwd(rnd.path) as cwd:
        # Missing competition, year and round.
        a = Args(None, None, None, "TestProblem", False)
        assert(a.competition == comp_name)
        assert(a.year == int(year_name))
        assert(a.round_name == round_name)
        assert(a.prob_name == "TestProblem")
        assert(a.interactive == False)
        # Specified different input.
        a = Args("OtherComp", "2017", "TestRound", "TestProblem", False)
        assert(a.competition == "OtherComp")
        assert(a.year == 2017)
        assert(a.round_name == "TestRound")
        assert(a.prob_name == "TestProblem")
        assert(a.interactive == False)

  def test_constructor_from_problem_folder(self):
    prob = Node("Problem", [])
    rnd = Node("Round", [prob])
    year = Node("2020", [rnd])
    comp = Node("Comp", [year])
    root = Node("root", [comp])
    with TestFolders(root) as test_folders:
      # Move to problem folder.
      with Cwd(prob.path) as cwd:
        # Missing all names.
        with self.assertRaises(KeyError):
          a = Args(None, None, None, None, False)
        # Specified different input.
        a = Args("OtherComp", "2017", "TestRound", "TestProblem", False)
        assert(a.competition == "OtherComp")
        assert(a.year == 2017)
        assert(a.round_name == "TestRound")
        assert(a.prob_name == "TestProblem")
        assert(a.interactive == False)


class TestFolderMaker(TestCase):

  def test_folder_making(self):
    comp = Node("Comp", [])
    root = Node("root", [comp])
    with TestFolders(root) as test_tree:
      comp_name = comp.path.parts[-1]
      # Test non-interactive.
      args = Args(comp_name, "2017", "TestRound", "TestProblem", False)
      fm = FolderMaker(args, test_mode=True)
      new_folder = fm.make_folder()
      parts = new_folder.parts
      assert(parts[-1] == args.prob_name)
      assert(parts[-2] == args.round_name)
      assert(parts[-3] == str(args.year))
      assert(parts[-4] == args.competition)
      assert(new_folder / "tests.in").exists()
      assert(new_folder / "main.py").exists()
      with open(new_folder / "main.py", 'r') as f:
        head = f.readline().strip()
        assert(head == "'''Standard template.")
      with self.assertRaises(FileExistsError):
        fm.make_folder()
      # Test interactive.
      i_args = Args(comp_name, "2018", "TestRound", "TestProblem", True)
      fm = FolderMaker(i_args, test_mode=True)
      new_folder = fm.make_folder()
      parts = new_folder.parts
      assert(parts[-1] == i_args.prob_name)
      assert(parts[-2] == i_args.round_name)
      assert(parts[-3] == str(i_args.year))
      assert(parts[-4] == i_args.competition)
      assert(new_folder / "tests.in").exists()
      assert(new_folder / "main.py").exists()
      with open(new_folder / "main.py", 'r') as f:
        head = f.readline().strip()
        assert(head == "'''Interactive template.")
      with self.assertRaises(FileExistsError):
        fm.make_folder()

class TestProcessInput(TestCase):

  def test_process_input(self):
    comp = Node("Comp", [])
    root = Node("root", [comp])
    with TestFolders(root) as test_folders:
      comp_name = comp.path.parts[-1]
      args = ['-c', comp_name, '-y', '2017', '-r', 'TestRound', '-p', 'TestProblem']
      process_input(args)
      args = ['-c', comp_name, '-y', '2018', '-r', 'TestRound', '-p', 'TestProblem2', '-i']
      process_input(args)
      args = ['-c', comp_name, '-y', 'blah', '-r', 'TestRound', '-p', 'TestProblem']
      with self.assertRaises(ValueError):
        process_input(args)
      args = ['-c', comp_name, '-y', '2017', '-r', 'TestRound', '-p', 'TestProblem', '-h']
      assert(process_input(args) == "help")
