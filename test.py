import tictactoe
import copy
import unittest
from unittest.mock import patch

class TestTicTacToe(unittest.TestCase):

    # Create a 3x3 grid, checks whether a grid user provides as input is valid or not
    def test_GridChecker(self):
        board = tictactoe.CheckerBox(3)
        result = board.isGridValid(9)
        self.assertEqual(result,True)

    # Checks if user provides an invalid input
    @patch('builtins.input', return_value="0")
    def test_invalidInput(self,input):
        board = tictactoe.CheckerBox(3)
        result = board.playRound()
        self.assertEqual(result, False)

    @patch('builtins.input', return_value="10")
    def test_invalidInputMax(self,input):
        board = tictactoe.CheckerBox(3)
        result = board.playRound()
        self.assertEqual(result, False)

    #Check if user provides a valid input
    @patch('builtins.input', return_value="1")
    def test_validUserInput(self,input):
        board = tictactoe.CheckerBox(3)
        result = board.playRound()
        self.assertEqual(result, True)
        self.assertEqual(board.count,1)
        self.assertEqual(["X","","","","","","","",""],board.board)

    # Tries to add a symbol to an invalid grid, but fails
    def test_addSymbolPlayer1(self):
        board = tictactoe.CheckerBox(3)
        board.placeGrid(0)
        self.assertEqual(["","","","","","","","",""],board.board)

    # Add a symbol to a valid grid, and passes
    def test_addValidSymbolPlayer1(self):
        board = tictactoe.CheckerBox(3)
        board.placeGrid(1)
        self.assertEqual(["X","","","","","","","",""],board.board)

    def test_addValidSymbolPlayer2(self):
        board = tictactoe.CheckerBox(3)
        board.placeGrid(1)
        board.count = 1
        board.placeGrid(1)
        self.assertEqual(["X","","","","","","","",""],board.board)

    # Test to see whether it can identify a match
    def test_checkMatch(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["X","X","X","O","O","O","","",""]
        board.count = 6
        result = board.isThereAMatch(1)
        self.assertEqual(result,True)

    # Test to see whether it cannot identify a match.
    def test_checkTie(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["X","X","O","O","O","X","X","O","X"]
        board.count = 9
        result = board.isThereAMatch(5)
        self.assertEqual(result,False)

    #Check the individual checking functions
    '''
     1 | X | O 
    -----------
     4 | X | O 
    -----------
     8 | X | 9 
    -----------
    '''
    def test_checkUpUp(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["","X","O","","X","O","","X",""]
        board.count = 5

        #Should fail because there are no grids above grid 2
        result = board.checkUpUp(2)
        self.assertEqual(result,False)

        #Should fail because there is only 1 grid above grid 5
        result = board.checkUpUp(5)
        self.assertEqual(result,False)

        # Should pass because there are 2 grids and there is a match
        result = board.checkUpUp(8)
        self.assertEqual(result,True)

        board.board = ["","X","O","","X","O","X","",""]
        # Should fail because there is no match along grid 8
        result = board.checkUpUp(8)
        self.assertEqual(result,False)

    def test_checkUpDown(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["","X","O","","X","O","","X",""]
        board.count = 5

        #Should fail because there are no grids above grid 2
        result = board.checkUpDown(2)
        self.assertEqual(result,False)

        #Should pass because there is 1 grid above grid 5 and 1 grid below grid 5 and there is a match
        result = board.checkUpDown(5)
        self.assertEqual(result,True)

        # Should fail because there are no grids below grid 8
        result = board.checkUpDown(8)
        self.assertEqual(result,False)

        board.board = ["","X","O","","X","O","X","",""]
        # Should fail because there is no match along grid 5
        result = board.checkUpDown(5)
        self.assertEqual(result,False)
    
    def test_checkDownDown(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["","X","O","","X","O","","X",""]
        board.count = 5

        #Should pass because there are 2 grids below grid 2
        result = board.checkDownDown(2)
        self.assertEqual(result,True)

        #Should fail because there is only 1 grid below grid 5
        result = board.checkDownDown(5)
        self.assertEqual(result,False)

        # Should fail because there are no grids below grid 8
        result = board.checkDownDown(8)
        self.assertEqual(result,False)

        board.board = ["X","","O","","X","O","","X",""]
        # Should fail because there is no match along grid 2
        result = board.checkDownDown(5)
        self.assertEqual(result,False)

    '''
     1 | O | 3 
    -----------
     X | X | X 
    -----------
     7 | O | 9 
    -----------
    '''
    def test_checkLeftLeft(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["","O","","X","X","X","","O",""]
        board.count = 5

        #Should fail because there are no grids to the left on grid 4
        result = board.checkLeftLeft(4)
        self.assertEqual(result,False)

        #Should fail because there is only 1 grid to the left of grid 5
        result = board.checkLeftLeft(5)
        self.assertEqual(result,False)

        # Should pass because there are 2 grids to the left of grid 6 and there is a match
        result = board.checkLeftLeft(6)
        self.assertEqual(result,True)

        board.board = ["","O","X","O","X","X","","O",""]
        # Should fail because there is no match along grid 6 to the left
        result = board.checkLeftLeft(6)
        self.assertEqual(result,False)

    def test_checkLeftRight(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["","O","","X","X","X","","O",""]
        board.count = 5

        #Should fail because there are no grids to the left on grid 4
        result = board.checkLeftRight(4)
        self.assertEqual(result,False)

        #Should pass because there is 1 grid to the left and 1 grid to the right of grid 5
        result = board.checkLeftRight(5)
        self.assertEqual(result,True)

        # Should fail because there are no grids to the right on grid 6
        result = board.checkLeftRight(6)
        self.assertEqual(result,False)

        board.board = ["","O","X","O","X","X","","O",""]
        # Should fail because there is no match along grid 5 to the left and right
        result = board.checkLeftRight(5)
        self.assertEqual(result,False)

    def test_checkRightRight(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["","O","","X","X","X","","O",""]
        board.count = 5

        #Should pass because there are 2 grids to the right on grid 4
        result = board.checkRightRight(4)
        self.assertEqual(result,True)

        #Should fail because there is only 1 grid to the right of grid 5
        result = board.checkRightRight(5)
        self.assertEqual(result,False)

        # Should fail because there are no grids to the right on grid 6
        result = board.checkRightRight(6)
        self.assertEqual(result,False)

        board.board = ["","O","X","O","X","X","","O",""]
        # Should fail because there is no match along grid 4 to the left and right
        result = board.checkRightRight(4)
        self.assertEqual(result,False)

    '''
     X | O | 3 
    -----------
     4 | X | 6 
    -----------
     7 | O | X 
    -----------
    '''
    def test_checkDiagLeftUpLeftUp(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["X","O","","","X","","","O","X"]
        board.count = 5

        #Should fail because there are no grids up or left
        result = board.checkDiagLeftUpLeftUp(1)
        self.assertEqual(result,False)

        #Should fail because there is only 1 grid up and 1 grid to the left
        result = board.checkDiagLeftUpLeftUp(5)
        self.assertEqual(result,False)

        # Should pass because there are 2 grids up and 2 grids to the left
        result = board.checkDiagLeftUpLeftUp(9)
        self.assertEqual(result,True)

        board.board = ["","O","X","O","X","","","O","X"]
        # Should fail because there is no match along grid 9 to the left diagonal
        result = board.checkDiagLeftUpLeftUp(9)
        self.assertEqual(result,False)

    
    def test_checkDiagLeftUpRightDown(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["X","O","","","X","","","O","X"]
        board.count = 5

        #Should fail because there are no grids up or left
        result = board.checkDiagLeftUpRightDown(1)
        self.assertEqual(result,False)

        #Should pass because there is at least 1 grid up, 1 grid left, 1 grid down, 1 grid right
        result = board.checkDiagLeftUpRightDown(5)
        self.assertEqual(result,True)

        # Should fail because there are no grids to the right or down
        result = board.checkDiagLeftUpRightDown(9)
        self.assertEqual(result,False)

        board.board = ["","O","X","O","X","","","O","X"]
        # Should fail because there is no match along grid 9 to the left diagonal
        result = board.checkDiagLeftUpLeftUp(5)
        self.assertEqual(result,False)

    def test_checkDiagRightDownRightDown(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["X","O","","","X","","","O","X"]
        board.count = 5

        #Should pass because there is at least 2 grids to the right, 2 grids down
        result = board.checkDiagRightDownRightDown(1)
        self.assertEqual(result,True)

        #Should fail because there is only 1 grid down and 1 grid right
        result = board.checkDiagRightDownRightDown(5)
        self.assertEqual(result,False)

        # Should fail because there are no grids to the right or down
        result = board.checkDiagRightDownRightDown(9)
        self.assertEqual(result,False)

        board.board = ["","O","X","O","X","","","O","X"]
        # Should fail because there is no match along grid 1 to the right
        result = board.checkDiagRightDownRightDown(1)
        self.assertEqual(result,False)

    '''
     1 | O | X 
    -----------
     4 | X | 6 
    -----------
     X | O | 9 
    -----------
    '''
    def test_checkDiagRightUpRightUp(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["","O","X","","X","","X","O",""]
        board.count = 5

        #Should fail because there are no grids up or right
        result = board.checkDiagRightUpRightUp(3)
        self.assertEqual(result,False)

        #Should fail because there is only 1 grid up and 1 grid to the right
        result = board.checkDiagRightUpRightUp(5)
        self.assertEqual(result,False)

        # Should pass because there are at least 2 grids up and 2 grids to the right
        result = board.checkDiagRightUpRightUp(7)
        self.assertEqual(result,True)

        board.board = ["","O","X","O","X","","","O","X"]
        # Should fail because there is no match along grid 9 to the left diagonal
        result = board.checkDiagRightUpRightUp(5)
        self.assertEqual(result,False)

    def test_checkDiagRightUpLeftDown(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["","O","X","","X","","X","O",""]
        board.count = 5

        #Should fail because there are no grids up or right
        result = board.checkDiagRightUpLeftDown(3)
        self.assertEqual(result,False)

        #Should pass because there is at least 1 grid up and 1 grid to the right, 1 grid down and 1 grid left
        result = board.checkDiagRightUpLeftDown(5)
        self.assertEqual(result,True)

        # Should fail because there are no grids down or no grids left
        result = board.checkDiagRightUpLeftDown(7)
        self.assertEqual(result,False)

        board.board = ["","O","X","O","X","","","O","X"]
        # Should fail because there is no match along grid 5 to the right diagonal
        result = board.checkDiagRightUpLeftDown(5)
        self.assertEqual(result,False)

    def test_checkDiagLeftDownLeftDown(self):
        board = tictactoe.CheckerBox(3)
        board.board = ["","O","X","","X","","X","O",""]
        board.count = 5

        #Should pass because there are at least 2 grids left and 2 grids down
        result = board.checkDiagLeftDownLeftDown(3)
        self.assertEqual(result,True)

        #Should fail because there is only 1 grid left and 1 grid down
        result = board.checkDiagLeftDownLeftDown(5)
        self.assertEqual(result,False)

        # Should fail because there are no grids down or no grids left
        result = board.checkDiagRightUpLeftDown(7)
        self.assertEqual(result,False)

        board.board = ["","O","X","O","X","","","O","X"]
        # Should fail because there is no match along grid 5 to the right diagonal
        result = board.checkDiagRightUpLeftDown(5)
        self.assertEqual(result,False)


