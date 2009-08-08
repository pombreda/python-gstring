import gstringc
import cStringIO, StringIO
import time
import gc
import sys

def time_cstringio(n, iterations, str_len):
   print "Timing native cStringIO %d times... " % n,
   cStringIO_time = 0.0
   text_to_add = "x" * str_len

   for i in xrange(n):   
      print i+1,
      gc.collect()
      time.sleep(2)
      begin = time.time()
      string = cStringIO.StringIO()
      for i in xrange(iterations):
         string.write(text_to_add)
      val = string.getvalue()
      end = time.time()
      string.close()
      del string, val
      cStringIO_time+=(end-begin)
   print "\nTime using native cStringIO %d times: %.2fs" % (n, cStringIO_time/float(n))
   return cStringIO_time/float(n)

def time_gstringc(n, iterations, str_len):
   print "Timing gstringc.GString %d times (no initial size)... " % n,
   GString_time = 0.0
   text_to_add = "x" * str_len

   for i in xrange(n):
      print i+1,
      gc.collect()
      time.sleep(2)
      begin = time.time()
      string = gstringc.GString()
      for i in xrange(iterations):
         string += text_to_add
      x = string.get_value()
      end = time.time()
      del x, string
      GString_time+=(end-begin)
   print "\nTime using gstringc.GString %d times (no initial size): %.2fs" % (n, GString_time/float(n))
   return GString_time/float(n)

def time_stringio(n, iterations, str_len):
   print "Timing native StringIO %d times... " % n,
   StringIO_time = 0.0
   text_to_add = "x" * str_len

   for i in xrange(n):   
      print i+1,
      gc.collect()
      time.sleep(2)
      begin = time.time()
      string = StringIO.StringIO()
      for i in xrange(iterations):
         string.write(text_to_add)
      val = string.getvalue()
      end = time.time()
      string.close()
      del string, val
      StringIO_time+=(end-begin)
   print "\nTime using native StringIO %d times: %.2fs" % (n, StringIO_time/float(n))
   return StringIO_time/float(n)

def run_tests():
   str_s = int(sys.argv[1])
   GString_time = time_gstringc(5, 500000, str_s)
   cStringIO_time = time_cstringio(5, 500000, str_s)
   StringIO_time = time_stringio(5, 500000, str_s)

if __name__ == "__main__":
   run_tests()
