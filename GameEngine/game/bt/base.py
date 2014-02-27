'''
Created on Feb 1, 2014

@author: Otrebor45
'''
class State:
    Error = -2
    Failed = -1
    Ready = 0
    Running = 1
    Success = 2
    
class Group:
    def __init__(self):
        self.actions = []
    
    def __call__(self,delta):
        return self.update(delta)
            
    def update(self,delta):
        return State.Error
    
    def addAction(self, action):
        self.actions.append(action)
        return self
    def reset(self):
        for action in self.actions:
            if(hasattr(action,"reset")):
                action.reset()
'''
# base structure of a behavior continue executing until one return running or failed
'''
class BehaviorTree(Group):
    def __init__(self):
        Group.__init__(self)
        self.data = {}
        
    def __call__(self,delta):
        return self.update(delta)
    
    def update(self, delta):
        size = len(self.actions)
        for i in range(0, size):
            state = self.actions[i](delta)
            if state != State.Failed:
                return state
        self.reset()
        return state
'''
# If one or multiple fail the whole sequence fails
'''
class Sequence(Group):
    def __init__(self):
        Group.__init__(self)
        self.current = -1
        
    def __call__(self,delta):
        return self.update(delta)
    
    def update(self, delta):
        size = len(self.actions)
        if self.current == -1:
            self.current = 0
            
        for i in range(self.current, size):
            state = self.actions[i](delta)
            if state != State.Success:
                return state
        
        return state
    
    def reset(self):
        Group.reset(self)
        self.current = 0
    
class Concurrent(Group):
    def __init__(self, minfails=-1):
        Group.__init__(self)
        self.minFail = minfails
        
    def __call__(self,delta):
        return self.update(delta)
    
    def update(self, delta):
        fails = 0
        state = State.Ready
        for action in self.actions:
            node = action(delta)
            if node == State.Failed:
                fails += 1
                if fails == self.minFail:
                    return State.Failed
            if node == State.Error:
                return State.Error
            if node == State.Running:
                state = node
        return state
    
    
class PrioritySelector(Group):
    def __init__(self):
        Group.__init__(self)
        
    def __call__(self,delta):
        return self.update(delta)
        
    def update(self, delta):
        size = len(self.actions)
        for i in range(0, size):
            state = self.actions[i](delta)
            if state == State.Failed:
                if hasattr(self.actions[i],'reset'):
                    self.actions[i].reset()
            if state != State.Failed:
                break
        return state
        
class SwitchSelector:
    
    def __init__(self, condition, true, false):
        self.condition = condition
        self.doTrue = true
        self.doFalse = false
        self.exe = None
    
    def __call__(self,delta):
        return self.update(delta)
          
    def update(self, delta):
        if self.exe == None:
            if self.condition():
                self.exe = self.doTrue
            else:
                self.exe = self.doFalse
        state = State.Ready
        if self.exe != None:
            state = self.exe(delta)
            self.exe = None
        return state 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
