# -*- coding: utf-8 -*-
class SpyProxy(object):
   def __init__(self, instance, logfile, spyname="SpyProxy"):
      object.__setattr__(self, "instance", instance)
      object.__setattr__(self, "spyname", spyname)
      object.__setattr__(self, "logfile", logfile)
      
      
   def _logmethod(self,method, methodname):
      def newmethod(*a,**b):
	  logfile = object.__getattribute__(self, "logfile")
          log = "calling callable '%s' with positional arguments %s and named arguments %s\n"%(methodname,str(a),str(b))
          logfile.write(log)
          return method(*a,**b)
      return newmethod
      
   def __getattribute__(self, attrname):
      spyname = object.__getattribute__(self, "spyname")
      logfile = object.__getattribute__(self, "logfile")
      attribute = getattr(object.__getattribute__(self, "instance"), attrname)
      attributetype = type(attribute)
      print type(attribute)
      if callable(attribute):
          decorator = object.__getattribute__(self, "_logmethod")
          attribute = decorator(attribute, attrname)
      log = "in %s (%i): reading attribute '%s' of type %s\n"%(spyname,id(attribute), attrname,str(attributetype))
      logfile.write(log)
      return attribute

   def __setattr__(self, attrname, value):
      spyname = object.__getattribute__(self, "spyname")
      logfile = object.__getattribute__(self, "logfile")
      log = "in %s (%i): attribute '%s' written with value:%s\n"%(spyname,id(object.__getattribute__(self, "instance")), attrname, str(value))
      logfile.write(log)
      
      return setattr(object.__getattribute__(self, "instance"), attrname, value)



if __name__ == "__main__":
  
  class C:
    def __init__(self):
      self.toto = "3"
      
    def foo(self, arg1, arg2):
      print "in foo: arg1=",arg1," arg2=", arg2
  
  import sys
  a = [1,2,3,3,6,1,-5]
  print id(a)
  print a
  spyA = SpyProxy(a, sys.stdout, "listspy" )
  spyA.sort()
  spyA.append(3)
  print a
  print spyA
  
  
  c = C()
  print "c.toto is", c.toto
  print "c has id: ",id(c)
  spyC = SpyProxy(c, sys.stdout, "cspy")
  spyC.toto = 29
  
  print "now c.toto has been modified:", c.toto
  
  
  c.foo(1,3)
  spyC.foo(1,3)
  