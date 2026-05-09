#Ibraheem Sleet 1220200 
import re
import heapq
import copy
from collections import defaultdict, deque
# Initialize an empty 2D array
######################################################################################

Time = 0 #counter for the time 
Memory = [] #Store the processes from the file sorted base on the arrival
Memory2 = []
Readyq = [] #Store the ready processes sorted base on priority
Waitq = [] #Store the processes that request a used resors
IOq = [] #Store the processes that request an IO 
CPU = [] #Store the executable process
GanttChart=[] #[[PID1,time in cpu],[PID2,time in cpu]...]
resources=[] #[[PID1,Resourse1 num],[PID2,Resourse2 num]...]
periodes=[] #[[PID1,wait1,IO1,ready1],[PID2,wait2,IO2,ready2]...]
Round_Roben_lists=[] #store the processes that enter a round roben
neededresources=[]
Round_Roben=0 #len(Round_Roben_lists)
cpu_time=0
IO_time=0
#######################################################################################

# Open the file
with open('test.txt', 'r') as file:
    for line in file:
        Lines = line.strip()
        row1 = re.split(r'[ ]+',Lines)  #['PID','Arrival','priority','cpu{20','R[1]'...comp not importent]
        row2 = re.split(r'[CPUIO]+', Lines)#['PID Arrival priority', '{20, R[2], 30, F[2], 10}', '{20}', '{30}'...]
        row =row1[0:3] + row2[1:len(row2)] #concate ['PID','Arrival','priority', with '{20, R[2], 30, F[2], 10}', '{20}', '{30}'...]
        Memory.append(row) #insert the list in the memory
Memory2 = copy.deepcopy(Memory)
#Memory.sort(key=lambda x: x[1])#sort the memory based on arraival

###########################################################################################
       
def cpu_f():
  global Readyq,Waitq,IOq,CPU,GanttChart,resources,Round_Roben,cpu_time,periodes,Round_Roben_lists
  x=0
  x1=0
  x2=0
  run = list(filter(None, re.split(r'[{}, ]+', CPU[3]))) #run store one cpu burst if cpu{20,R[1],10}-->['20','R[1]','10'] (filter for empty strings)
  while  (x1==0 and run and CPU) or ((run[0][0] == 'R' or run[0][0] == 'F')and run) : # if process enter now in the cpu (if cpu_time not get value yet) and (run not empty(process finish))   
    
    if run[0][0] == 'R': 
      result = [row for row in resources if row[1] == int(run[0][2])] #we search in the second colomn of resources list about run[0][2]-->resource_num (R[resource_num]) 
      if result: # if the resource exist in resources list mean that is currently held by another process
         result2 = [row for row in periodes if row[0] == int(CPU[0])]
         index = periodes.index(result2[0])
         #periodes[index][3] += 1 # decrement the wait time 
         if x1:
           x2=1
         Waitq.append(CPU.copy()) # moved to the waiting queue 
         Waitq.sort(key=lambda x: x[2])
         CPU.clear()
         run.clear() 
         if not x1:
           if Readyq:
             RoundRoben()
             CPU = Readyq.pop(0) #new process enter the cpu  
             run = list(filter(None, re.split(r'[{}, ]+', CPU[3])))  
      else: #if the resource free(not held by another process)
         resources.append([int(CPU[0]),int(run[0][2])]) # add the resource to the resources list 
         #CPU = ['1', '2', '3', '{R[1],R[2]}'] run=['R[1]','R[2]']
         #remove the finished parts of burst from run and cpu
         run.pop(0)
         if run: 
            CPU[3] = '{' + ','.join(run) + '}'   
         else:
           CPU.pop(3) 
           if len(CPU) == 3:
            CPU.clear() # termenated
           elif len(CPU) > 3:
             IOq.append(CPU.copy())  # move the process to IOq
             CPU.clear()

    elif run[0][0] == 'F': 
      #search on the resource num in resources list to delete it
      result = [row for row in resources if row[1] == int(run[0][2])]
      if result:
         index = resources.index(result[0])
         if x1 and Waitq:
           g=0
           while g < len(Waitq):
             A = list(filter(None, re.split(r'[{}, ]+', Waitq[g][3]))) #run store one cpu burst if cpu{R[1],10}-->['R[1]','10'] (in waitq always start with R) 
             if resources[index][1] == int(A[0][2]): #search if the resource stil held in resources list
                result1 = [row for row in periodes if row[0] == int(Waitq[g][0])] # search on the index of PID in the periodes list 
                index2 = periodes.index(result1[0])
                periodes[index2][1] += 1 # decrement the wait time 
             g+=1
         resources.pop(index) #delete the resource from the resources list
      run.pop(0)
      if run: 
        CPU[3] = '{' + ','.join(run) + '}'   
      else:
        CPU.pop(3) 
        if len(CPU) == 3:
          CPU.clear() # termenated
        elif len(CPU) > 3:
          IOq.append(CPU.copy())  # move the process to IOq
          CPU.clear()
       
    elif int (run[0][0]) > 0 and x1==0: #if it not R or F so it a time 
        if not cpu_time:
          #x1 = 1
          if Round_Roben :
            # if int(run[0]) <5:
            #   cpu_time = int(run[0]) 
            # else:
             cpu_time = 5
          else:
            cpu_time = 1000000   
          GanttChart.append([int(CPU[0]),0])
    #else :
     # break
    if run:
      if cpu_time == 0 and (run[0][0]!='F' and run[0][0]!='R') and x1 and Round_Roben:
          Readyq.append(CPU.copy()) 
          CPU.clear()


    if cpu_time>0 and run and (run[0][0]!='F' and run[0][0]!='R'):
        cpu_time-=1
        GanttChart[-1][1]+=1 
        x1=1
        run[0] = str( int(run[0])-1)
        if cpu_time and int(run[0])!=0 :
           CPU[3] = '{' + ','.join(run) + '}'
        elif cpu_time == 0 or int(run[0])==0  :
            if int(run[0])==0:
              run.pop(0)
              if run:
                CPU[3] = '{' + ','.join(run) + '}'
              else:
                x=1
                CPU.pop(3)
      
            else:
              #if not x:
                CPU[3] = '{' + ','.join(run) + '}'
                #if run[0][0]!='F' or run[0][0]!='R':
                Readyq.append(CPU.copy()) 
                CPU.clear()
    
    if not run:
      if len(CPU) <= 3:
        CPU.clear() # termenated
      elif len(CPU) > 3:
        IOq.append(CPU.copy())  # move the process to IOq
        CPU.clear()
      cpu_time=0
      break
  return x2
 
#####################################################################

def IO_f():
  global periodes,IOq,Readyq,Round_Roben, IO_time
  k=0
  while k < len(IOq): #because Processes can perform I/O simultaneously and do not wait for each other.
     
     IO = list(filter(None, re.split(r'[{}, ]+', IOq[k][3]))) #IO stor an IO burst 
     if IO:
      IO_time = int(IO[0])-1 # decrement the value of IO burst
     result1 = [row for row in periodes if row[0] == int(IOq[k][0])] #search on the PID of the process in the periodes list 
     if result1:
      index = periodes.index(result1[0]) #find the index of the PID in the periodes list
      periodes[index][2] +=1  #increment the wait time to the process
     if IO_time==0: #if IO finish the process move to the readyq
       IOq[0].pop(3)
       Readyq.append( IOq.pop(k)) #the process move to the readyq
       Readyq.sort(key=lambda x: x[2]) #sort the ready based on priority 
     else:  
       IOq[k][3] = '{'+str(IO_time)+'}' #update the value of remainder IO burst
     k+=1

###################################################################
def wait_f( x ):
  global periodes,Readyq,Waitq,resources,Round_Roben
  index=0
  g=0
  while g < len(Waitq)-x:
     run = list(filter(None, re.split(r'[{}, ]+', Waitq[g][3]))) #run store one cpu burst if cpu{R[1],10}-->['R[1]','10'] (in waitq always start with R) 
     result = [row for row in resources if row[1] == int(run[0][2])] #search if the resource stil held in resources list
     if result: # if held
       result1 = [row for row in periodes if row[0] == int(Waitq[g][0])] # search on the index of PID in the periodes list 
       index = periodes.index(result1[0])
       periodes[index][1] += 1 # decrement the wait time 
       #str(int(periodes[index][1]) + 1)
     else: # if it free
       Readyq.append( Waitq.pop(g)) 
       Readyq.sort(key=lambda x: x[2])
     g+=1

#######################################################################

def ready_f():
  global Readyq,periodes
  c=0
  while c < len(Readyq):
    result1 = [row for row in periodes if row[0] == int(Readyq[c][0])]  
    if result1:
      index = periodes.index(result1[0])
      periodes[index][3]+=1 # decrement the Ready time
    c+=1
    

#########################################################################3
def RoundRoben():
  global Readyq,Round_Roben,Round_Roben_lists
    # Get the last value of the first list
  target_value = Readyq[0][2] 
    # Find all lists that end with the same value
  Round_Roben_lists = [lst for lst in Readyq if lst[2] == target_value]
  if len(Round_Roben_lists)>1:
    Round_Roben = len (Round_Roben_lists)
  else:
   Round_Roben =0
   Round_Roben_lists.clear()
############################################################################

def deadLock():
    global Waitq, resources, neededresources
    PID_waitq = []  # List to store PIDs
    g = 0
    
    # Step 1: Build the resource allocation graph (RAG)
    while g < len(Waitq):
        run = list(filter(None, re.split(r'[{}, ]+', Waitq[g][3])))  # Extract resource and value
        # Example for {R[1],10} -> ['R[1]', '10']
        neededresources.append([int(Waitq[g][0]), int(run[0][2])])  # Store [PID, needed resource]
        PID_waitq.append(int(Waitq[g][0]))  # Store the PID
        g += 1

    # Step 2: Create lists to track which processes are waiting and which resources are available
    processes = [p[0] for p in resources]  # List of all processes
    all_resources = set([r[1] for r in resources] + [r[1] for r in neededresources])  # All unique resources

    # Step 3: Create dictionaries for quick lookup of allocated and needed resources
    allocated_dict = {sublist[0]: sublist[1] for sublist in resources}  # {PID: allocated resource}
    needed_dict = {sublist[0]: sublist[1] for sublist in neededresources}  # {PID: needed resource}

    # Step 4: Track waiting processes and available resources
    waiting_processes = set(processes)  # All processes initially waiting
    available_resources = list(all_resources)  # Start with all resources as available
    cycle_processes = []  # To store processes involved in the cycle

    # Step 5: Detect deadlock
    while waiting_processes:
        progress_made = False
        for pid in list(waiting_processes):
            if pid in needed_dict:
                needed_resource = needed_dict[pid]

                # Check if the needed resource is available
                if needed_resource in available_resources:
                    # Process can proceed, release its allocated resource (if any)
                    if pid in allocated_dict:
                        released_resource = allocated_dict[pid]
                        available_resources.append(released_resource)  # Release the resource

                    waiting_processes.remove(pid)  # Process can proceed
                    progress_made = True

        if not progress_made:
            # No progress was made, meaning deadlock has occurred
            cycle_processes.extend(waiting_processes)  # Store the processes in the cycle
            return cycle_processes  # Return the cycle

    return []


##################################################################################


def deadlockRecovery():
  global resources,Memory2,Waitq,Readyq
  cycle_pids = deadLock()    # Detect cycle and get PIDs
  if cycle_pids:
     # Remove values at odd indexes 
     highest_priority = None
     pid_with_highest_priority = None

# Step 2: Iterate through the list and find the PID with the highest priority
     for pid, _, priority, *rest in Waitq:  # Use *rest to ignore extra data
        if pid in cycle_pids:
          if highest_priority is None or priority > highest_priority:
              highest_priority = priority
              pid_with_highest_priority = pid

     for i, sublist in enumerate(Waitq):
         if sublist[0] == pid_with_highest_priority:
        # Step 2: Pop the list with PID = '4'
          popped_list = Waitq.pop(i)
          break
     for i, sublist in enumerate(Memory2):
         if sublist[0] == pid_with_highest_priority:
          Readyq.append(Memory2.copy(i))
          break
     resources = [sublist for sublist in resources if sublist[0] != 1]

     
#######################################################################

first_process = int(Memory[0][1])
while  CPU or Waitq or Readyq or IOq or Time<=first_process:   
   
  while Memory and int(Memory[0][1])==Time:
       Readyq.append(Memory.pop(0))
       periodes.append([int(Readyq[-1][0]),0,0,0]) #for the process that enter for the first time in the readyq (the process start in readyq) 
       #pid wait io ready
       Readyq.sort(key=lambda x: x[2])
  if not CPU and Readyq:
    Readyq.sort(key=lambda x: x[2])
    RoundRoben() 
    CPU = Readyq.pop(0) 
  
  if Readyq :
    ready_f()

  if IOq :
    IO_f()  
  

  if CPU:
    x1 = cpu_f()
  else:
     if GanttChart[-1][0]==-1:
      GanttChart[-1][1]+=1
     else:
      GanttChart.append([-1,1])
  
  if x1:
    if Waitq:
      wait_f(1)

  else :
    if Waitq:
      if len(Waitq)>1:
        deadlockRecovery()
        #print (Waitq,"111")
      wait_f(0)
      #print (Waitq,"222")

  Time+=1
  
print("[PID,Wait_time,IO_time,Ready_time]" ,periodes) 
print("GanttChart[PID,CPU_time]",GanttChart)
total_waiting_time = 0
total_turnaround_time = 0

for process in periodes:
      _, wait_time, io_time, ready_time = process
      result = [sublist for sublist in GanttChart if sublist[0] == process[0]]
      cputime = sum(sublist[1] for sublist in result) 
      total_waiting_time += ready_time
      turnaround_time = wait_time + io_time + ready_time + cputime
      total_turnaround_time += turnaround_time

num_processes = len(periodes)
avg_waiting_time = total_waiting_time / num_processes
avg_turnaround_time = total_turnaround_time / num_processes

print("avg_waiting_time = ",avg_waiting_time)
print("avg_turnaround_time = ",avg_turnaround_time)
  
#######################################
