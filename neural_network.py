import numpy as np

class MLP(object):
    def __init__(self,parameter,Layers=(5, 10, 3)):
        self.net = [dict() for i in range(len(Layers))]
        self.net[0]['a']=np.zeros(Layers[0]+1)
        start=0
        end=0
        for i in range(1,len(Layers)):
            self.net[i]['a'] = np.zeros(Layers[i]+1)
            self.net[i]['z'] = np.zeros((Layers[i]))
            if i==1:
                start = 0
                end+=(Layers[i - 1] + 1) * Layers[i]
                self.net[i]['W'] = parameter[start:end].reshape(Layers[i - 1] + 1, Layers[i])
            else:
                start +=(Layers[i - 2]+1)* Layers[i-1]
                end+=(Layers[i - 1]+1)* Layers[i]
                self.net[i]['W'] = parameter[start:end].reshape(Layers[i - 1] + 1, Layers[i])
        self.p = np.zeros(self.net[-1]['a'][1:].shape) # Softmax Output

    def forward(self,x):
        np.copyto(self.net[0]['a'],np.hstack((1,x)))
        for i in range(1, len(self.net)):
            np.copyto(self.net[i]['z'],self.net[i-1]['a'].dot(self.net[i]['W']))
            np.copyto(self.net[i]['a'],np.hstack((1,self.sigmoid(self.net[i]['z']))))
        np.copyto(self.p, self.softmax(self.net[-1]['a'][1:]))

    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-1.0*z))
    def softmax(self, a):
        return np.exp(a) / np.sum(np.exp(a), axis=0)




