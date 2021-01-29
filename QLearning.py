import random
from graphics import *



window = None
windowObjects = [[[ ' 'for action in range(4)] for col in range(6)] for row in range(5)]
rewards = 0
plot = [[]]

class Agent:
    row = None
    col = None
    isDestructed = 0

    def __init__(self, row, col, isDestructed):
        self.row = row
        self.col = col
        self.isDestructed = isDestructed

    def setDestruction(self, number):
        self.isDestructed = number

    def updateAgent(self, row, col):
        self.row = row
        self.col = col


# actions
# up = 0
# right = 1
# down = 2
# left = 3
class QValue:
    action = None
    row = None
    col = None
    QValue = None

    def __init__(self, action, row, col, QValue):
        self.action = action
        self.row = row
        self.col = col
        self.QValue = QValue

    def __repr__(self):
        return str(self)

    def __str__(self):
        action = None
        if (self.action == 0):
            action = 'up'
        if (self.action == 1):
            action = 'right'
        if (self.action == 2):
            action = 'down'
        if (self.action == 3):
            action = 'left'
        return '(%s,%s): [%s,%s]' % (self.row, self.col, action, self.QValue)

    def __gt__(self, other):
        return self.QValue > other.QValue

    def updateQValue(self, QValue):
        self.QValue = QValue


def get_position():
    row = random.randrange(1, 5, 1)
    col = random.randrange(1, 6, 1)
    return Agent(row, col, 0)


def iterations(episodes, alpha, gama, epsilon, initialQ, display):
    global rewards
    allQValues = [[[QValue(action, row, col, initialQ) for action in range(4)] for col in range(7)] for row in range(6)]
    createGui(allQValues)
    while episodes > 0:
        rewards = 0
        print('Start |episode: %s' % (1000 - episodes))
        agent = get_position()
        limitSteps = 50
        while limitSteps > 0:
            print('step: %s' % (50 - limitSteps))
            prob = random.random()
            action = None
            flag = True
            if agent.row == 1 and agent.col == 1:
                updateGoalvalues(allQValues, 10, alpha, gama,agent)
                print('Agent passed goal!')
                print('$$$$$$$$$$ update values $$$$$$$')
                print(allQValues)
                limitSteps = 1
                flag = False

            else:
                if prob < epsilon:
                    action = random_action(agent, allQValues)
                    reward = allowed_actions(action, agent)
                    updateValues(allQValues, reward, agent, action, alpha, gama)
                else:
                    action = best_action(agent, allQValues)
                    reward = allowed_actions(action, agent)
                    updateValues(allQValues, reward, agent, action, alpha, gama)

            limitSteps = limitSteps - 1
            display(agent)
        # print(rewards)
        # print('rewards: {0}, episode: {1}').format(rewards/50,1000-episodes)
        if flag:
            print('Agent failed goal')
            print('$$$$$$$$$$ update values $$$$$$$')
            print(allQValues)
        print('Finish |episode: %s\n#####################################' % (1000 - episodes))

        episodes = episodes - 1
    deleteGui()
    return episodes


def repairing(agent):
    agent.isDestructed = 0
    return agent


def broken(agent):
    agent.isDestructed = 1
    return agent


def best_action(agent, allQValues):
    actions = []
    actions.append([0, agent.row - 1, agent.col])  # up
    actions.append([1, agent.row, agent.col + 1])  # right
    actions.append([2, agent.row + 1, agent.col])  # down
    actions.append([3, agent.row, agent.col - 1])  # left
    Qvalues = []
    for index in range(4):
        Qvalues.append(max(allQValues[actions[index][1]][actions[index][2]][:]))
    return max(Qvalues)


def random_action(agent, allQValues):
    actions = []
    actions.append([0, agent.row - 1, agent.col])  # up
    actions.append([1, agent.row, agent.col + 1])  # right
    actions.append([2, agent.row + 1, agent.col])  # down
    actions.append([3, agent.row, agent.col - 1])  # left
    rand = random.randrange(4)
    temp = allQValues[actions[rand][1]][actions[rand][2]][:]
    rand = random.randrange(4)
    return temp[rand]


def allowed_actions(action, agent):
    if action.row < 1 or action.row > 4 or action.col < 1 or action.col > 5:
        return -1
    else:
        if agent.col == 1 and agent.col + 1 == action.col and action.row == 2:
            return -1
        if agent.col == 1 and agent.col + 1 == action.col and  action.row == 3:
            return -1
        if agent.col == 2 and agent.col - 1 == action.col and action.row == 1:
            return -1
        if agent.col == 2 and agent.col - 1 == action.col and action.row == 2:
            return -1
        if agent.col == 2 and agent.col - 1 == action.col and action.row == 3:
            return -1
        if agent.col == 2 and agent.col + 1 == action.col and action.row == 1:
            return -1
        if agent.col == 3 and agent.col - 1 == action.col and action.row == 1:
            return -1
        if agent.col == 1 and agent.row == 1:
            return 10
        if agent.isDestructed == 1 and action.col == 3 and action.row == 2:
            return -10
        if agent.isDestructed == 0 and action.col == 3 and action.row == 2:
            agent.setDestruction(1)
        if agent.isDestructed == 1 and action.col == 2 and action.row == 1:
            agent.setDestruction(0)

    return 0


def updateValues(allQValues, reward, agent, action, alpha, gama):
    global rewards
    tempAction = checkAction(agent, action)
    if reward != -1:
        if tempAction == 'up':
            prob = random.random()
            if prob > 0.4:
                allQValues[agent.row][agent.col][0].updateQValue(
                    (1 - alpha) * allQValues[agent.row][agent.col][0].QValue + alpha * (reward + gama * action.QValue))
            else:
                action = QValue(2, agent.row + 1, agent.col, allQValues[agent.row + 1][agent.col][2].QValue)
                reward = allowed_actions(action, agent)
                tempAction = 'down'

        if tempAction == 'right':
            allQValues[agent.row][agent.col][1].updateQValue(
                (1 - alpha) * allQValues[agent.row][agent.col][1].QValue + alpha * (reward + gama * action.QValue))
        if tempAction == 'down':
            allQValues[agent.row][agent.col][2].updateQValue(
                (1 - alpha) * allQValues[agent.row][agent.col][2].QValue + alpha * (reward + gama * action.QValue))
        if tempAction == 'left':
            allQValues[agent.row][agent.col][3].updateQValue(
                (1 - alpha) * allQValues[agent.row][agent.col][3].QValue + alpha * (reward + gama * action.QValue))
    else:
        if tempAction == 'up':
            prob = random.random()
            if prob > 0.4:
                allQValues[agent.row][agent.col][0].updateQValue(
                    (1 - alpha) * allQValues[agent.row][agent.col][0].QValue + alpha * (reward))
            else:
                action = QValue(2, agent.row + 1, agent.col, allQValues[agent.row + 1][agent.col][2].QValue)
                reward = allowed_actions(action, agent)
                tempAction = 'down'

        if tempAction == 'right':
            allQValues[agent.row][agent.col][1].updateQValue(
                (1 - alpha) * allQValues[agent.row][agent.col][1].QValue + alpha * (reward))
        if tempAction == 'down':
            if reward == -1:
                allQValues[agent.row][agent.col][2].updateQValue(
                    (1 - alpha) * allQValues[agent.row][agent.col][2].QValue + alpha * (reward))
            else:
                allQValues[agent.row][agent.col][2].updateQValue(
                (1 - alpha) * allQValues[agent.row][agent.col][2].QValue + alpha * (reward + gama * action.QValue))
        if tempAction == 'left':
            allQValues[agent.row][agent.col][3].updateQValue(
                (1 - alpha) * allQValues[agent.row][agent.col][3].QValue + alpha * (reward))

    agentLast = Agent(agent.row,agent.col,agent.isDestructed)

    if reward != -1:
        agent.updateAgent(action.row, action.col)
    rewards += reward
    insertData(allQValues,agentLast,agent,action)

def checkAction(agent, action):
    if agent.row - 1 == action.row:
        return 'up'
    if agent.row + 1 == action.row:
        return 'down'
    if agent.col + 1 == action.col:
        return 'right'
    if agent.col - 1 == action.col:
        return 'left'

    return 'noAction'


def updateGoalvalues(allQValues, reward, alpha, gama,agent):
    allQValues[1][1][0].updateQValue((1 - alpha) * allQValues[1][1][0].QValue + alpha * reward)
    allQValues[1][1][1].updateQValue((1 - alpha) * allQValues[1][1][1].QValue + alpha * reward)
    allQValues[1][1][2].updateQValue((1 - alpha) * allQValues[1][1][2].QValue + alpha * reward)
    allQValues[1][1][3].updateQValue((1 - alpha) * allQValues[1][1][3].QValue + alpha * (reward + gama * allQValues[1][1][3].QValue))
    insertData(allQValues,agent,agent, QValue(5,1,1,0))


def createGui(allQValues):
    global window
    global windowObjects
    window = GraphWin("GridWorld", 700, 600)
    window.setCoords(0, 0, 7, 7)
    window.setBackground("black")
    rectangle = Rectangle(Point(1, 1), Point(6, 5))
    rectangle.setFill("white")
    rectangle.draw(window)
    Rectangle(Point(2, 5), Point(1, 4)).draw(window).setFill('green')
    Rectangle(Point(3, 5), Point(2, 4)).draw(window).setFill('yellow')
    Rectangle(Point(3, 4), Point(4, 3)).draw(window).setFill('brown')
    
    for i in range(1, 5):
        Line(Point(1, i), Point(6, i)).draw(window)
    for x in range(1, 6):
        if x == 2:
            l = Line(Point(x, 2), Point(x, 5)).draw(window)
            l.setWidth(5)
            l.setFill('red')
            Line(Point(x, 1), Point(x, 2)).draw(window)
        elif x == 3:
            l = Line(Point(x, 4), Point(x, 5)).draw(window)
            l.setWidth(5)
            l.setFill('red')
            Line(Point(x, 1), Point(x, 3)).draw(window)
        else:
            Line(Point(x, 1), Point(x, 5)).draw(window)
    
    for k in range(1, 5):
        for j in range(1, 6):
            if j != 1 or k != 1:
                windowObjects[k-1][j-1][0] = (Text(Point(j + 0.5, 6 - (k + 0.1)), u"\u2191" + ': ' + str('%.3f' % allQValues[k][j][0].QValue)).draw(window))
                windowObjects[k-1][j-1][1] = (Text(Point(j + 0.5, 6 - (k + 0.35)), u"\u2192" + ': ' + str('%.3f' % allQValues[k][j][1].QValue)).draw(window))
                windowObjects[k-1][j-1][2] = (Text(Point(j + 0.5, 6 - (k + 0.85)), u"\u2193" + ': ' + str('%.3f' % allQValues[k][j][2].QValue)).draw(window))
                windowObjects[k-1][j-1][3] =(Text(Point(j + 0.5, 6 - (k + 0.6)), u"\u2190" + ': ' + str('%.3f' % allQValues[k][j][3].QValue)).draw(window))
            else:
                windowObjects[k-1][j-1][3] =(Text(Point(j + 0.5, 6 - (k + 0.5)), str('%.3f' % allQValues[k][j][3].QValue)).draw(window))
    


def deleteGui():
    global window
    window.getMouse()
    window.close()

def insertData(allQValues, agentLast, agent, action):
    global window
    global windowObjects
    winObjects = []
    agentP = Circle(Point(agent.col + 0.084321, 5.084321 - agent.row), 0.06)
    agentP.setFill('blue')
    agentP.draw(window)
    winObjects.append(agentP)

    tempAction = checkAction(agentLast, action)
    row = agentLast.row
    col = agentLast.col

    if tempAction == 'up':
        windowObjects[row-1][col-1][0].undraw()
        windowObjects[row-1][col-1][0] = (Text(Point(col + 0.5, 6 - (row + 0.1)), u"\u2191" + ': ' + str('%.3f' % allQValues[row][col][0].QValue)).draw(window))
    if tempAction == 'right':
        windowObjects[row-1][col-1][1].undraw()
        windowObjects[row-1][col-1][1] = (Text(Point(col + 0.5, 6 - (row + 0.35)), u"\u2192" + ': ' + str('%.3f' % allQValues[row][col][1].QValue)).draw(window))
    if tempAction == 'down':
        windowObjects[row-1][col-1][2].undraw()
        windowObjects[row-1][col-1][2] = (Text(Point(col + 0.5, 6 - (row + 0.85)), u"\u2193" + ': ' + str('%.3f' % allQValues[row][col][2].QValue)).draw(window))
    if tempAction == 'left':
        windowObjects[row-1][col-1][3].undraw()
        windowObjects[row-1][col-1][3] = (Text(Point(col + 0.5, 6 - (row + 0.6)), u"\u2190" + ': ' + str('%.3f' % allQValues[row][col][3].QValue)).draw(window))
    if tempAction == 'noAction':
        windowObjects[row-1][col-1][3].undraw()
        windowObjects[row-1][col-1][3] =(Text(Point(col + 0.5, 6 - (row + 0.5)), str('%.3f' % allQValues[row][col][3].QValue)).draw(window))


    winObjects[0].undraw()