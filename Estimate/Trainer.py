import numpy as np
from nn import TFProcess

BSIZE=15

class GmkData:
    def __init__(self,filename):
        self.nowindex=0
        td=np.loadtxt(filename,dtype=np.float32)
        np.random.shuffle(td)
        tcol=td[:,0:BSIZE*BSIZE*2]
        tp=td[:,BSIZE*BSIZE*2:BSIZE*BSIZE*3]
        tval=td[:,BSIZE*BSIZE*3:BSIZE*BSIZE*3+1]
        tcol=tp.reshape([-1,2, BSIZE*BSIZE])
        #tp=td[:,1:50]
        #tval=td[:,50:51]
        #tp=tp.reshape([-1,49,1])
        self.ecnt=td.shape[0]
        print("%d data loaded"%(self.ecnt))
        self.data=[tcol,tp,tval]
    def next_batch(self, batchsize):
        s1=[x[self.nowindex:self.nowindex+batchsize] for x in self.data]
        self.nowindex+=batchsize
        if self.nowindex>self.ecnt:
            self.nowindex%=self.ecnt
            return [np.vstack((s1[i],self.data[i][:self.nowindex])) for i in range(3)]
        else:
            return s1

def main():
    trainer=TFProcess()
    data=GmkData("gmkdata.txt")
    while True:
        trainer.process(data.next_batch(128))
    
main()
