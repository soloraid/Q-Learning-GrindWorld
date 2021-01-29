import unittest
import random
import QLearning


class QlearningTest(unittest.TestCase):

    def test_1(self, episodes=1000, alpha=0.1, gama=0.5, epsilon=0.2, initialQ=0):
        self.compute(episodes, alpha, gama, epsilon, initialQ)
    def test_2(self, episodes=1000, alpha=0.1, gama=0.5, epsilon=0.2, initialQ=20):
        self.compute(episodes, alpha, gama, epsilon, initialQ)
    def test_3(self, episodes=1000, alpha=0.1, gama=0.5, epsilon=0, initialQ=0):
        self.compute(episodes, alpha, gama, epsilon, initialQ)
    def test_4(self, episodes=1000, alpha=0.1, gama=0.1, epsilon=0.2, initialQ=0):
        self.compute(episodes, alpha, gama, epsilon, initialQ)
    def test_5(self, episodes=1000, alpha=0.9, gama=0.5, epsilon=0.2, initialQ=0):
        self.compute(episodes, alpha, gama, epsilon, initialQ)

    def compute(self, episodes, alpha, gama, epsilon, initialQ):
        def fn_display(agent):
            display(agent)

        result = QLearning.iterations(episodes, alpha, gama,
                                      epsilon, initialQ, fn_display)

        self.assertTrue(result == 0)
        print('#############END ITERATION#################')


class Board:

    def __init__(self):
        board = [['#', '# ', '# ', '# ', '# ', '# ', '#'], ['#', 'G|', 'R|', '. ', '. ', '. ', '#'],
                 ['#', '.|', '. ', 'H ', '. ', '. ', '#'], ['#', '.|', '. ', '. ', '. ', '. ', '#'],
                 ['#', '. ', '. ', '. ', '. ', '. ', '#'], ['#', '# ', '# ', '# ', '# ', '# ', '#']]
        self._board = board

    def get(self, row, column):
        return self._board[column][row]

    def setAgent(self, agent):
        self._board[agent.row][agent.col] = 'A '

    def printing(self):
        for i in (range(0, len(self._board))):
            print(' '.join(self._board[i]))
        print('#########################')


def display(agent):
    board = Board()
    board.setAgent(agent)
    board.printing()

def running_single_test(testcase):
    switcher = {
        1: 'test_1',
        2: 'test_2',
        3: 'test_3',
        4: 'test_4',
        5: 'test_5',
    }
    return switcher.get(testcase, 'Wrong choice')

if __name__ == "__main__":
    # unittest.main()
    while True:
        single_test = unittest.TestSuite()
        print('{0}:\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n'.format('Menu', 
        '1.episodes=1000, alpha=0.1, gama=0.5, epsilon=0.2, initialQ=0',
        '2.episodes=1000, alpha=0.1, gama=0.5, epsilon=0.2, initialQ=20',
        '3.episodes=1000, alpha=0.1, gama=0.5, epsilon=0  , initialQ=0',
        '4.episodes=1000, alpha=0.1, gama=0.1, epsilon=0.2, initialQ=0',
        '5.episodes=1000, alpha=0.9, gama=0.5, epsilon=0.2, initialQ=0',
        '6.exit'))
        test_case = int(input('\n\nEnter your choice: '))
        if test_case == 6:
            break
        test_name = running_single_test(test_case)
        if test_name != 'Wrong choice':
            single_test.addTest(QlearningTest(test_name))
            unittest.TextTestRunner().run(single_test)
        else:
            print(test_name)