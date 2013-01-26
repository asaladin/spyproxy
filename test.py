from spyproxy import SpyProxy
import sys
import unittest

from StringIO import StringIO




class TestSpyProxy(unittest.TestCase):
        def setUp(self):
            pass
        
        def testSpyArray(self):
            def aMethod(a, b, c='hello'):
                return {'calc':a+b, 'string':c}

            
            a = [3, 4, "custom message", aMethod] # set values of list 'a'
            result1 = a[3](a[0], a[1], a[2])

            buf = StringIO()
            spya = SpyProxy(a, buf)
            result2 = spya[3](spya[0], spya[1], spya[2])
            
            self.assertEqual(result1, result2)
            log = buf.getvalue()
            
            self.assertIn("reading item[3] of type <type 'function'> of value <function aMethod at", log)
            self.assertIn("reading item[0] of type <type 'int'> of value 3", log)
            self.assertIn("reading item[1] of type <type 'int'> of value 4", log)
            
            self.assertEqual(str(a), str(spya))
            
            

            
        def testSimpleClassAttribute(self):
            class A:
                def __init__(self):
                    self.myattribute = 3
            buf = StringIO()
            a  = A()
            self.assertEqual(a.myattribute, 3)
            
            a = SpyProxy(a, buf)
            self.assertEqual(a.myattribute, 3)
            ret = buf.getvalue()
            self.assertTrue("reading attribute 'myattribute' of type <type 'int'> with value 3" in ret)
            
        def testClassMethod(self):
            class C:
                def __init__(self):
                    self.toto = "3"
      
                def foo(self, arg1, arg2):
                    return "in foo: arg1=",arg1," arg2=", arg2

            buf = StringIO()
            c = C()
            spyC = SpyProxy(c, buf, "spyC")
            
            self.assertEqual(c.foo(1,2), spyC.foo(1,2))
            
            
        def testAddAttributeDynamically(self):
            class C:
                pass
            
            buf = StringIO()
            
            spyc = SpyProxy(C(), buf )
            spyc.foo = 42
            self.assertEqual(spyc.foo, 42)
            
            log = buf.getvalue()
            self.assertIn("attribute 'foo' written with value:42", log)
            self.assertIn("reading attribute 'foo' of type <type 'int'> with value 42", log)
            

            
if __name__ == "__main__":
        unittest.main()