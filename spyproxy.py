# -*- coding: utf-8 -*-
class SpyProxy(object):
   def __init__(self, instance, logfile, spyname="SpyProxy"):
      object.__setattr__(self, "instance", instance)
      object.__setattr__(self, "spyname", spyname)
      object.__setattr__(self, "logfile", logfile)
   def __getattribute__(self, attrname):
      spyname = object.__getattribute__(self, "spyname")
      logfile = object.__getattribute__(self, "logfile")
      log = "in %s (%i): attribute '%s' read\n"%(spyname,id(object.__getattribute__(self, "instance")), attrname)
      logfile.write(log)
      
      return getattr(object.__getattribute__(self, "instance"), attrname)

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
  
  #print spyA