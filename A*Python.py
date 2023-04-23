class Node:

    def __init__(self,tilePos,level,fValue): ## Constructor for the Node class : Initialise the values for each instance
        self.tilePos = tilePos ## This will hold the positions of the tiles in a 2x2 matrix
        self.fValue = fValue ## The value of this solution (heuristic + level)
        self.level = level  ##The level of the graph

    ##This will get all the valid moves we can currently make
    def MoveNCheck(self,currentPuzzle,x1,y1,x2,y2):
        length = len(self.tilePos)
        if x2 >= 0 and x2 < length and y2 >= 0 and y2 < length: ##this checks if the move is valid
            ##this then moves the puzzle
            temp_puz = []
            temp_puz = self.copy(currentPuzzle)
            temp = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp
            return temp_puz ##Our new puzzle solution
        else: ##In the event it is invalid
            return None

    def gen_children(self, tempListOfAllNodes): ## need to change this algorithm so that it doesn't create nodes that it has already traversed
        children = []
        x,y = self.locate(self.tilePos,'.')
        val_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        for i in val_list:
            child = self.MoveNCheck(self.tilePos,x,y,i[0],i[1]) ##checks not out of value and moves if so
            if child is not None:
                child_node = Node(child,self.level+1,0)
                if (child_node.notinthere( tempListOfAllNodes)):
                    children.append(child_node)
        return children
##This function will check if we have encoutered a solution before to prevent us from looping
    def notinthere(self, list):
        for i in list:
            if(i.tilePos == self.tilePos):
                return False
        return True
##Creates a copy of the node data that we can change without effecting current node
    def copy(self,currentPuzzle):
        temp = []
        for i in currentPuzzle:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp

    def locate(self,currentPuzzle,x): ##Iterates through the current solutions tiles until locate a particular tile
        length = len(self.tilePos)
        for i in range(0,length): ##Becuase its a square
            for j in range(0,length):
                if x == currentPuzzle[i][j]:
                    return i,j ##Gives back index of that tile
class Puzzle:
    def __init__(self): ## Constructor for Puzzle
        self.waiting = []
        self.traversed = []

    def h1(self,current,goal): ##Hamming Method

        temp = 0
        for i in range(0,3): #iterates through the tilePos
            for j in range(0,3):
                if current[i][j] != goal[i][j] and current[i][j] != '.':
                    temp += 1 # adds a tally to the h everytime the current tile isn't the correct one
        return temp
    def h2(self, current, goal): ## Manhattan Method
        temp = 0
        for i in range(0,3): #iterates through the tilePos
            for j in range(0,3):
                if current[i][j] != goal[i][j] and current[i][j] != '.':
                    x,y = current.locate(current.tile_pos,current[i][j])
                    temp = temp + abs(i-x)+abs(j-y) ##Calculates the vertical and horizontal difference of the tiles position
        return temp
    def h(self,heuristic,current,goal): ## handles which heuristic to use
        if heuristic == "h1":
            h1(self,current,goal)
        elif heuristic == "h2":
            h2(self,current,goal)
        else:
            print("Something has gone wrong")
            exit(1)

    def f(self,current,goal):
        return self.h1(current.tilePos,goal)+current.level


    def AStar(self):
        print("Would you like to use Manhattan(M) or Hamming(H) distance") ##User selects heuristic
        disChoice = input("")
        start = [['4', '7', '2'], ['1', '6', '5'], ['3', '8', '.']]
        goal = [['.', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]
        if disChoice.lower() == "m":
            heuristic = "h2"
        else: ##defaults to hamming
            heuristic = "h1"
        start = Node(start,0,0) ##Sets the start data as new node and begins the search
        start.fvalue = self.f(start,goal)
        self.waiting.append(start)
        while True: ##Repeats until at goal
            if len(self.waiting) == 0:
                print("No solutions")
                break
            currentNode = self.waiting[0] ##Takes the highest valued node from waiting
            print("\n")
            print("Current Node:") ##Displays node
            for i in currentNode.tilePos:
                for j in i:
                    print(j,end=" ")
                print("")

            if(self.h1(currentNode.tilePos,goal) == 0): ## when it has been solved
                break

            else: ##If not solved keep trying to solve
                tempListOfAllNodes = self.waiting + self.traversed
                temp = currentNode.gen_children(tempListOfAllNodes) ##Gets the possible moves that we can make from here and adds them to waiting
                for i in temp:
                    i.fvalue = self.f(i,goal)
                    self.waiting.append(i)
                self.traversed.append(currentNode) ##We have now done everything we can to this node so we add it to traversed
                del self.waiting[0] ##remove from waiting
                self.waiting.sort(key = lambda x:x.fvalue,reverse=False) ##Sorts the new waiting list so we can get the most optimal next path

##Main that sets of the AStar
currentPuzzle = Puzzle()
currentPuzzle.AStar()
print("The program has now completed")
