class CheckerBox:
    def __init__(self,size):
        self.size = size
        self.noGrids = self.size**2
        self.initBoard()
        self.count = 0

        self.user1 = ""
        self.user2 = ""

        self.user1symbol = "X"
        self.user2symbol = "O"

    def initBoard(self):
        self.board = []
        for i in range(self.noGrids):
            self.board.append("")

    def inputPlayersName(self):
        self.user1 = input("Enter name for player 1: \n")
        self.user2 = input("Enter name for player 2: \n")

    #Check whether there is a match arising from the player's last grid
    def isThereAMatch(self,gridNo):
        if self.count < 5:
            return False
        else:
            if self.size == 3:
                result = self.checkThree(gridNo)
            else:
                result = self.checkN(gridNo)
            return result

    #Returns whether there is a next round 
    def playRound(self):
        gridNo = self.getUserGrid()

        if gridNo == -1:
            return False
        else:
            isSymbolPlaced = self.placeGrid(gridNo)

            if (isSymbolPlaced):
                self.count += 1
                match = self.isThereAMatch(gridNo)

                if (match):
                    self.printWinner()
                    return False
                else:
                    if self.count >= self.noGrids:
                        self.printTie()
                        return False
                    else:
                        return True
            else:
                return True

    #Asks for user to provide the grid where the symbol will be added to
    def getUserGrid(self):
        playerNo = self.count % 2
        playerName = self.getPlayerName(playerNo)

        if playerNo == 0:
            symbol = self.user1symbol
        else:
            symbol = self.user2symbol

        boxNo = input("Player {}, choose a box to place an '{}' into: \n".format(playerName,symbol))
        if boxNo.isdigit() and (int(boxNo)>0 and int(boxNo)<=self.noGrids):
            return int(boxNo)
        else:
            print("You have entered an invalid input. Please try again.")
            return -1

    # Places the symbol in the board
    def placeGrid(self,grid):
        playerNo = self.getPlayerNo()

        if (self.isGridValid(grid)):
            if self.board[int(grid)-1] == "":
                if playerNo == 0:
                    token = self.user1symbol
                else:
                    token = self.user2symbol
                    
                self.board[grid-1] = token
                return True
            else:
                print("You have selected a box that is filled. Please try again.")
                return False
        else:
            return False

    #Prints out the board
    def printBoard(self):
        toPrint = ""
        formattedRow = []
        for i in range(self.noGrids):
            colNo = i%self.size
            if self.board[i] == "":
                formattedRow.append(str(i+1))
            else:
                formattedRow.append(self.board[i])
            if colNo == self.size-1:
                rowOfGrids = " | ".join(formattedRow)
                toPrint = toPrint + rowOfGrids + "\n"
                formattedRow = []
                rowNo = i/self.size
                if rowNo < self.size-1:
                    toPrint = toPrint + "-"*len(rowOfGrids) + "\n"
                
        print(toPrint)

    #Logic to consider the cases for each grid in a 3x3 to reduce the number of search cases
    def checkThree(self,gridNo):
        if gridNo == 1:
            return self.checkRightRight(gridNo) or self.checkDownDown(gridNo) or self.checkDiagRightDownRightDown(gridNo)
        elif gridNo == 2:
            return self.checkDownDown(gridNo) or self.checkLeftRight(gridNo)
        elif gridNo == 3:
            return self.checkLeftLeft(gridNo) or self.checkDownDown(gridNo) or self.checkDiagLeftDownLeftDown(gridNo)
        elif gridNo == 4:
            return self.checkUpDown(gridNo) or self.checkRightRight(gridNo)
        #This has 4 solutions
        elif gridNo == 5:
            return self.checkLeftRight(gridNo) or self.checkUpDown(gridNo) or self.checkDiagLeftUpRightDown(gridNo) or self.checkDiagRightUpLeftDown(gridNo)
        elif gridNo == 6:
            return self.checkLeftLeft(gridNo) or self.checkUpDown(gridNo)
        elif gridNo == 7:
            return self.checkRightRight(gridNo) or self.checkUpUp(gridNo) or self.checkDiagRightUpRightUp(gridNo)
        elif gridNo == 8:
            return self.checkLeftRight(gridNo) or self.checkUpUp(gridNo)
        else :
            return self.checkLeftLeft(gridNo) or self.checkUpUp(gridNo) or self.checkDiagLeftUpLeftUp(gridNo)

    def checkN(self,gridNo):
        return self.checkLeftLeft(gridNo) or self.checkLeftRight(gridNo) or self.checkRightRight(gridNo) or self.checkUpUp(gridNo) or self.checkUpDown(gridNo) or self.checkDownDown(gridNo) or self.checkDiagLeftUpLeftUp(gridNo) or self.checkDiagLeftUpRightDown(gridNo) or self.checkDiagRightDownRightDown(gridNo) or self.checkDiagRightUpRightUp(gridNo) or self.checkDiagRightUpLeftDown(gridNo) or self.checkDiagLeftDownLeftDown(gridNo)

    #Check for vertical match starting from the grid to 2 grids below it
    def checkUpUp(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if rowNo<2:
            return False
        else:
            upGrid = (rowNo-1)*self.size+colNo
            upupGrid = (rowNo-2)*self.size+colNo
            return self.board[boardIndex] == self.board[upGrid] and self.board[boardIndex] == self.board[upupGrid]

    #Check for vertical match checking the grid above and the grid below
    def checkUpDown(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if rowNo<1 or rowNo+1 >= self.size:
            return False
        else:
            upGrid = (rowNo-1)*self.size+colNo
            downGrid = (rowNo+1)*self.size+colNo
            return self.board[boardIndex] == self.board[upGrid] and self.board[boardIndex] == self.board[downGrid]

    #Check for vertical match checking 2 grids above
    def checkDownDown(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if rowNo+2 >= self.size:
            return False
        else:
            downGrid = (rowNo+1)*self.size+colNo
            downDownGrid = (rowNo+2)*self.size+colNo
            return self.board[boardIndex] == self.board[downGrid] and self.board[boardIndex] == self.board[downDownGrid]

    #Check for horizontal match match checking 2 grids to the left
    def checkLeftLeft(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if colNo < 2:
            return False
        else:
            leftGrid = boardIndex-1
            leftLeftGrid = boardIndex-2
            return self.board[boardIndex] == self.board[leftGrid] and self.board[boardIndex] == self.board[leftLeftGrid]

    #Check for horizontal match match checking grid to the left and grid to the right
    def checkLeftRight(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if colNo < 1 or colNo+1 >= self.size:
            return False
        else:
            leftGrid = boardIndex-1
            rightGrid = boardIndex+1
            return self.board[boardIndex] == self.board[leftGrid] and self.board[boardIndex] == self.board[rightGrid]

    #Check for horizontal match match checking 2 grids to the right
    def checkRightRight(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if colNo+2 >= self.size:
            return False
        else:
            rightGrid = boardIndex+1
            rightRightGrid = boardIndex+2
            return self.board[boardIndex] == self.board[rightGrid] and self.board[boardIndex] == self.board[rightRightGrid]
        
    #Check for diagonal match by checking 2 grids in the northwest direction
    def checkDiagLeftUpLeftUp(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if rowNo < 2 or colNo < 2:
            return False
        else:
            leftUpGrid = (rowNo-1)*self.size+colNo-1
            leftUpleftUpGrid = (rowNo-2)*self.size+colNo-2
            return self.board[boardIndex] == self.board[leftUpGrid] and self.board[boardIndex] == self.board[leftUpleftUpGrid]

    #Check for diagonal match by checking grid in the northwest direction and the southeast direction
    def checkDiagLeftUpRightDown(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if (rowNo < 1 or colNo < 1) or (rowNo+1 >= self.size or colNo+1 >= self.size) :
            return False
        else:
            leftUpGrid = (rowNo-1)*self.size+colNo-1
            rightDownGrid = (rowNo+1)*self.size+colNo+1
            return self.board[boardIndex] == self.board[leftUpGrid] and self.board[boardIndex] == self.board[rightDownGrid]

    #Check for diagonal match by checking 2 grids in the southeast direction
    def checkDiagRightDownRightDown(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if (rowNo+2 >= self.size or colNo+2 >= self.size) :
            return False
        else:
            rightDownGrid = (rowNo+1)*self.size+colNo+1
            rightDownRightDownGrid = (rowNo+2)*self.size+colNo+2
            return self.board[boardIndex] == self.board[rightDownGrid] and self.board[boardIndex] == self.board[rightDownRightDownGrid]

    #Check for diagonal match by checking 2 grids in the northeast direction
    def checkDiagRightUpRightUp(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if (rowNo < 2 or colNo+2 >= self.size) :
            return False
        else:
            rightUpGrid = (rowNo-1)*self.size+colNo+1
            rightUprightUpGrid = (rowNo-2)*self.size+colNo+2
            return self.board[boardIndex] == self.board[rightUpGrid] and self.board[boardIndex] == self.board[rightUprightUpGrid]

    #Check for diagonal match by checking grid in northeast and grid in southwest direction
    def checkDiagRightUpLeftDown(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if (rowNo+1 >= self.size or colNo < 1) or (rowNo-1 > 0 or colNo+1 >= self.size) :
            return False
        else:
            leftDownGrid = (rowNo+1)*self.size+colNo-1
            rightUpGrid = (rowNo-1)*self.size+colNo+1
            return self.board[boardIndex] == self.board[leftDownGrid] and self.board[boardIndex] == self.board[rightUpGrid]

    #Check for diagonal match by checking 2 grids in the southwest direction
    def checkDiagLeftDownLeftDown(self,gridNo):
        boardIndex = gridNo-1
        rowNo,colNo = self.getRowNoColNo(boardIndex)

        if (rowNo+2 >= self.size or colNo < 2) :
            return False
        else:
            leftDownGrid = (rowNo+1)*self.size+colNo-1
            leftDownLeftDownGrid = (rowNo+2)*self.size+colNo-2
            return self.board[boardIndex] == self.board[leftDownGrid] and self.board[boardIndex] == self.board[leftDownLeftDownGrid]

    def getRowNoColNo(self,gridNo):
        rowNo = int(gridNo/self.size)
        colNo = gridNo%self.size
        return rowNo,colNo

    def printWinner(self):
        player = (self.count-1)%2
        playerName = self.getPlayerName(player)
        print("Congratulations {}! You have won.\n".format(playerName))

    #Odd counts are player 2, even counts are player 1
    def getPlayerNo(self):
        return self.count % 2

    def printTie(self):
        print("There is no winner in this round.\n")

    # Check the grid the user is trying to add to is valid
    def isGridValid(self,gridNo):
        if gridNo<1 or gridNo > self.noGrids:
            return False
        else:
            return True

    def getPlayerName(self,playerNo):
        if playerNo == 0:
            playerName = self.user1
        else:
            playerName = self.user2

        return playerName

def getGridSize():
    isValid = False
    toReturn = 3
    
    while(not isValid):
        sizeOfN = input("What is the size of the grid you want to play with? Size should be at least 3. ")
        if sizeOfN.isdigit():
            toReturn = int(sizeOfN)
            if toReturn < 3:
                print("You have input an invalid size. Please try again")
            else:
                isValid = True
        else:
            print("You have input an invalid value. Please try again.")

    return toReturn
            

if __name__ == "__main__":
    boardSize = getGridSize()
    board = CheckerBox(boardSize)
    board.inputPlayersName()

    isGameStillOn = True
    board.printBoard()
    while (isGameStillOn == True):
        isGameStillOn = board.playRound()
        board.printBoard()