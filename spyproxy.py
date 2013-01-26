# -*- coding: utf-8 -*-
class SpyProxy(object):
   """
   This simple class acts like the object it replaces but logs some operations
   like function calls, and get/set operations on attributes.
   It can be used to intrusively quickly study some moderately complicated object to help 
   understand how it is called without actually reading the code that uses it. 
   """
    
   def __init__(self, instance, logfile, spyname="SpyProxy"):
      """
      @param instance: the object to be replaced by the spying proxy
      @param logfile: a file-like object implementing a 'write' method
      
      """
      object.__setattr__(self, "instance", instance)
      object.__setattr__(self, "spyname", spyname)
      object.__setattr__(self, "logfile", logfile)
      
      
   def _logmethod(self,method, methodname):
      """
      decorator for loging method calls
      """
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
      if callable(attribute):
          decorator = object.__getattribute__(self, "_logmethod")
          attribute = decorator(attribute, attrname)
      log = "in %s (%i): reading attribute '%s' of type %s with value %s\n"%(spyname,id(attribute), attrname,str(attributetype), str(attribute))
      logfile.write(log)
      return attribute

   def __setattr__(self, attrname, value):
      spyname = object.__getattribute__(self, "spyname")
      logfile = object.__getattribute__(self, "logfile")
      log = "in %s (%i): attribute '%s' written with value:%s\n"%(spyname,id(object.__getattribute__(self, "instance")), attrname, str(value))
      logfile.write(log)
      
      return setattr(object.__getattribute__(self, "instance"), attrname, value)

   def __getitem__(self, key):
       spyname = object.__getattribute__(self, "spyname")
       instance = object.__getattribute__(self,"instance")
       logfile = object.__getattribute__(self, "logfile")
       
       item = instance[key]
       logfile.write("in %s (%i): reading item[%s] of type %s of value %s\n"%(spyname, id(instance), str(key), type(item), str(item) ) )
       
       return item
       
   def __repr__(self):
       instance = object.__getattribute__(self,"instance")
       return repr(instance)

  