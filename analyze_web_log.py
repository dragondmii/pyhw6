#!/usr/bin/python

#########################################
## CS 3430: S2017: HW06
## Author: Robert Epstein
#########################################

import re
import sys
import os
import fnmatch
import math

## --------- GENERATING FILE NAMES

def generate_file_names(fnpat, rootdir):
  for path, dirlist, filelist in os.walk(rootdir):
    for file_name in fnmatch.filter(filelist, fnpat):
      yield os.path.join(path, file_name)
  pass

def unit_test_01(fnpat, rootdir):
  for fn in generate_file_names(fnpat, rootdir):
    sys.stdout.write(fn + '\n')
  sys.stdout.flush()

## uncomment the unit test to run
if __name__ == '__main__':
##  unit_test_01(sys.argv[1], sys.argv[2])
  pass

## ----------- GENERATING INPUT STREAMS & LINES
      
def generate_input_streams(gen_filenames):
  for fn in gen_filenames:
   if fn.endswith('.txt'):
    yield open(fn)

def generate_lines(gen_instreams):
  for fs in gen_instreams:
   for line in fs:
    yield line

def unit_test_02(fnpat, rootdir):
  fns = generate_file_names(fnpat, rootdir)
  instreams = generate_input_streams(fns)
  lns = generate_lines(instreams)
  for ln in lns:
    print ln,

if __name__ == '__main__':
#  unit_test_02(sys.argv[1], sys.argv[2])
  pass

## ----------- GENERATING TOOPS OF IPS and TRANSFERRED BYTES

def generate_ip_trbts_toops(pat, gen_lines, ip_group_num=1, trbytes_group_num=9):
 cpat = re.compile(pat)
 for line in gen_lines:
  m = re.match(cpat, line)
  if m != None:
   yield (m.group(ip_group_num),int(m.group(trbytes_group_num)))
 pass

ip_trbts = {} ## dictionary
def count_ip_trbts(gen_ip_trbts_toops):
  global ip_trbts
  for i in gen_ip_trbts_toops:

   if ip_trbts.has_key(i[0]):
    ip_trbts[i[0]] = ip_trbts[i[0]]+[i[1]]
   else:
    ip_trbts[i[0]] = [i[1]]
  pass

def unit_test_03(fnpat, rootdir):
  logpat =  r'^([\d\.\w-]+)\s+(- -)\s+\[(\d{2}\/\w{3}\/\d{4}):(\d{2}:\d{2}:\d{2}).+\]\s+\"(.+)\s+(.+)\s+(.+)\"\s+(\d+)\s+(\d+)$'
  fns = generate_file_names(fnpat, rootdir)
  instreams = generate_input_streams(fns)
  lns = generate_lines(instreams)
  toops = generate_ip_trbts_toops(logpat, lns, ip_group_num=1, trbytes_group_num=9)
  count_ip_trbts(toops)
  for ip, trbts in ip_trbts.items():
    print ip, '-->', trbts

if __name__ == '__main__':
# unit_test_03(sys.argv[1], sys.argv[2])
 pass

## ----------- COMPUTING LOG STATS

## call compute_log_stats or pipe_log_stats before calling generate_log_stats.
## pipe_log_stats does the same as compute_log_stats but with fewer lines of code.
def compute_log_stats(fnpat, rootdir):
  logpat = r'^([\d\.\w-]+)\s+(- -)\s+\[(\d{2}\/\w{3}\/\d{4}):(\d{2}:\d{2}:\d{2}).+\]\s+\"(.+)\s+(.+)\s+(.+)\"\s+(\d+)\s+(\d+)$'
  glogs = generate_file_names(fnpat, rootdir)
  gstreams = generate_input_streams(glogs)
  glines = generate_lines(gstreams)
  ## adjust the values of ip_group_num and trbytes_group_num according to your regexp
  gip_trbts_toops = generate_ip_trbts_toops(logpat, glines, ip_group_num=1, trbytes_group_num=9)
  count_ip_trbts(gip_trbts_toops)

def pipe_log_stats(fnpat, rootdir):
  logpat = r'^([\d\.\w-]+)\s+(- -)\s+\[(\d{2}\/\w{3}\/\d{4}):(\d{2}:\d{2}:\d{2}).+\]\s+\"(.+)\s+(.+)\s+(.+)\"\s+(\d+)\s+(\d+)$'
  glines = generate_lines(generate_input_streams(generate_file_names(fnpat, rootdir)))
  count_ip_trbts(generate_ip_trbts_toops(logpat, glines, ip_group_num=1, trbytes_group_num=9))
  
## standard deviation
def std(seq):
  t = var(seq)
  return t**.5
  pass

## variance
def var(seq):
  if len(seq) == 1:
    return 0.0
  t=0.0
  for x in xrange(len(seq)):
    t=t+float((seq[x] - (sum(seq)/len(seq)))**2)
  t = t*(1.0/len(seq))
  return t
  pass

def getKey(item):
	return int(item[1][4:])

def top_n(gen_log_stats, n):

  sort_things = sorted(list(gen_log_stats), key = getKey, reverse=True)
  for i in xrange(n+1):
    print sort_things[i]

def generate_log_stats(ip_trbts):
  for key, value in ip_trbts.items():
    yield ['IP='+str(key), 'SUM='+str(sum(value)), 'N='+str(len(value)), 'MEAN='+str(sum(value)/len(value)), 'VAR='+str(var(value)), 'STD='+str(std(value))]
  pass


def unit_test_04(fnpat, rootdir, n):
  global ip_trbts
  compute_log_stats(fnpat, rootdir)
  top_n(generate_log_stats(ip_trbts), n)

## comment and uncomment unit test
if __name__ == '__main__':
  unit_test_04(sys.argv[1], sys.argv[2], int(sys.argv[3]))
  pass













