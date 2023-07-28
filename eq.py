from pyo import *

s = Server()
s.setAmp(.1)
s.boot()
s.start()

class Eq(PyoObject):

    def __init__(self,src= Noise(),port = 9997,type = 0):
        
        self._port = port
        self._oscmsg = OscReceive(port=self._port, address=["/freq","/q","/boost", "/mul","/bypass"])
        self._src = src
        self._type = type
        self._q = self._oscmsg["/q"]
        self._oscmsg.setValue("/q", 1)
        self._boost = self._oscmsg["/boost"]
        self._freq = self._oscmsg["/freq"]
        self._mul = self._oscmsg["/mul"]
        self._oscmsg.setValue("/mul", 1)
        self._eq = EQ(self._src, freq = self._freq, q = self._q, boost = self._boost, mul = self._mul, type=self._type)
        self._p = Pan(self._eq, outs=2, pan=0.5)
        self._base_objs = self._p.getBaseObjects()
        

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, x):
        self._src = x
        self._eq.setInput(self._src)

    @property
    def freq(self):
        return self._freq
        
    @freq.setter
    def freq(self, x):
        self._freq = x
        self._eq.setFreq(self._freq) 

    @property
    def q(self):
        return self._q

    @q.setter
    def q(self, x):
        self._q = x
        self._eq.setQ(self._q) 
    
    @property
    def boost(self):
        return self._boost

    @boost.setter
    def boost(self, x):
        self._boost = x
        self._eq.setBoost(self._boost)

    @property
    def mul(self):
        return self._mul

    @mul.setter
    def mul(self, x):
        self._mul = x
        self._eq.setMul(self._mul)
    
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, x):
        self._type = x
        self._eq.setType(self._type)
    
    def ctrl(self):
        self._eq.ctrl()

    def out(self): 
        self._bypass = self._oscmsg["/bypass"]
        eq_out = Interp(self._src, self._p, interp=self._bypass) # 1=ON, 0=bypass
        self._out = eq_out.out()

if __name__ == '__main__':
    eq = Eq()
    eq.ctrl()
    eq.out()
    Spectrum(eq)
    s.gui(locals())