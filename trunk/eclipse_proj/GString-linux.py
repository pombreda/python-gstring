def run_tests(iterations, str_append_size):
   import time
   import gc
   import sys
   import StringIO
   import cStringIO
   import gstringc

   str_size    = str_append_size
   text_to_add = "x" * str_size
   
   print "Timing native StringIO..."
   gc.collect()
   time.sleep(1)
   begin = time.time()
   string = StringIO.StringIO()
   for i in xrange(iterations):
      string.write(text_to_add)
   val = string.getvalue()
   end = time.time()
   string.close()
   del string, val
   print "Time using native StringIO: %.2fs" %(end-begin)

   print "Timing native cStringIO..."
   gc.collect()
   time.sleep(1)
   begin = time.time()
   string = cStringIO.StringIO()
   for i in xrange(iterations):
      string.write(text_to_add)
   val = string.getvalue()
   end = time.time()
   string.close()
   del string, val
   cStringIO_time = end-begin
   print "Time using native cStringIO: %.2fs" %(end-begin)

   print "Timing gstringc.GString..."
   gc.collect()
   time.sleep(1)
   begin = time.time()
   string = gstringc.GString("",iterations*len(text_to_add))
   for i in xrange(iterations):
      string += text_to_add
   x = string.get_value()
   end = time.time()
   del x, string
   GString_time = end-begin
   print "Time using gstringc.GString: %.2fs" %(end-begin)

   print "Timing gstringc.GString (no initial size)..."
   gc.collect()
   time.sleep(1)
   begin = time.time()
   string = gstringc.GString()
   for i in xrange(iterations):
      string += text_to_add
   x = string.get_value()
   end = time.time()
   del x, string
   GString_time = end-begin
   gc.collect()
   time.sleep(1)
   print "Time using gstringc.GString (no initial size): %.2fs" %(end-begin)

   print "\n# Performance of gstringc.GString concat (+=) over cStringIO.write: %.2f%%" % (GString_time*100.0/cStringIO_time)
   print "# In %d iterations using an string with size %d to append\n" % (iterations, len(text_to_add))

if __name__ == "__main__":
   
   for i in range(10, 41, 10):
      run_tests(100000*2, i)
