'''
Created on Mar 5, 2014

@author: rfloresx
'''
import game.Game as game


class Main(game.Game):
    def __init__(self):
        game.Game.__init__(self)
        
    
if __name__ == '__main__':
    m = Main()
    m.run()