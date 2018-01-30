# tool to automate various AWS commands

import boto3
import sys
import os
import time

from operator import itemgetter

import util as u

def list_instances():
  ec2 = u.create_ec2_resource()
  instances = [(u.seconds_from_datetime(i.launch_time), i) for i in ec2.instances.all()]
  sorted_instances = sorted(instances, key=itemgetter(0))

  for (seconds, instance) in sorted_instances:
    hours_ago = (time.time()-seconds)/3600
    hours_ago+=8 # adjust for time being in UTC
    print(u.get_name(instance.tags), instance.id, hours_ago)

def get_instance(fragment):
  ec2 = u.create_ec2_resource()
  instances = [(u.seconds_from_datetime(i.launch_time), i) for i in ec2.instances.all()]
  # latest instance first
  sorted_instances = reversed(sorted(instances, key=itemgetter(0)))
  for (seconds, instance) in sorted_instances:
    name = u.get_name(instance.tags)
    if fragment in u.get_name(instance.tags):
      hours_ago = (time.time()-seconds)/3600
      hours_ago+=8 # adjust for time being in UTC
      print("Found instance %s launched %.1f hours ago" %(name, hours_ago,))
      return instance
  print("Found nothing matching", fragment)
  
def main():
  if len(sys.argv) < 2:
    mode = 'list'
  else:
    mode = sys.argv[1]

  if mode == 'list':
    list_instances()
  elif mode == 'reboot':
    task_fragment = sys.argv[2]
    instance = get_instance(task_fragment)
    print("Rebooting "+u.get_name(instance.tags))
    instance.reboot()
  else:
    assert False, "Unknown mode "+mode
      
if __name__=='__main__':
  main()