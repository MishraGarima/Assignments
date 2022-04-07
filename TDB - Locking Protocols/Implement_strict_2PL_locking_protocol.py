#TDB Practical Assignment 2B
#Python Code to Implement Strict Two-Phase Locking Protocol

from datetime import datetime

data_item_locks = {}
lock_holders = {}
lock_point = {}
commit_status = {}
waiting = {}

def get_lock(item, lock, transaction):
    #in growing phase
    if lock_point[transaction]==0:
        #data item not present
        if item not in data_item_locks.keys():
            data_item_locks[item] = lock
            lock_holders[item] = []
            lock_holders[item].append(transaction)
            waiting[item] = []
            commit_status[transaction] = 0
            return str(datetime.now())+" Lock Acquired on "+item+" by "+transaction
        #data item present
        else:
            #already in exclusive lock
            if data_item_locks[item]=="X":
                waiting[item].append((transaction,lock))
                return str(datetime.now())+" Cannot Acquire Lock on "+item
            #in shared lock
            else:
                #want to acquire exclusive lock
                if lock=="X":
                    waiting[item].append((transaction, lock))
                    return str(datetime.now())+" Cannot Acquire Lock on "+item
                #want to acquire share lock
                else:
                    #not already itself has shared lock
                    if transaction not in lock_holders[item]:
                        lock_holders[item].append(transaction)
                        data_item_locks[item] = lock
                        return str(datetime.now())+" Lock Acquired on "+item+" by "+transaction
    #in shrinking phase
    else:
        return str(datetime.now())+" Cannot Acquire Lock as Transaction is in Shrinking Phase"

def revoke_lock(item, transaction):
    #exclusive lock
    if data_item_locks[item]=="X":
        #transcation committed
        if commit_status[transaction]==1:
            data_item_locks[item]=None
            lock_holders[item].remove(transaction)
        #transaction not committed
        else:
            return str(datetime.now())+"Cannot Revoked Lock on "+item
    #shared lock
    else:
        lock_holders[item].remove(transaction)
    #if no lock holder present put none
    if len(lock_holders[item])==0:
        data_item_locks[item]=None
    return str(datetime.now())+" Lock Revoked on "+item

def check_waiting():
    it_del = []
    #for all data items
    for item in data_item_locks.keys():
        #if no lock acquired
        if data_item_locks[item] == None:
            #there exist waiting
            if len(waiting[item])!=0:
                #serve waiting
                transaction = waiting[item][0][0]
                lock = waiting[item][0][1]
                while lock=="S":
                    print(get_lock(item, lock, transaction))
                    del waiting[item][0]
                    #if no waiting
                    if len(waiting[item])==0:
                        lock = None
                    #for more in waiting list
                    else:
                        transaction = waiting[item][0][0]
                        lock = waiting[item][0][1]
            #no waiting
            else:
                it_del.append(item)
    #delete unnecessary item
    for it in it_del:
        del data_item_locks[it]
        del waiting[it]
        del lock_holders[it]
    #delete transaction holding no data item
    t_present = 0
    t_list = []
    for t in lock_point.keys():
        for i in lock_holders.keys():
            if t in lock_holders[i]:
                t_present = 1
        if t_present==0:
            t_list.append(t)
    for trans in t_list:
        del lock_point[trans]

instruction = input("Enter instruction:")
#for no interrupt occur
while instruction!="stop":
    #obtain instruction elements
    instruction = str(instruction)
    current_transaction = instruction.split(" ")[0]
    if instruction.split(" ")[1]=="COMMIT":
        commit_status[current_transaction] = 1
    else:
        data_item = instruction.split(" ")[1][2]
        lock_type = instruction.split(" ")[1][0]

        #check lock point
        if current_transaction not in lock_point.keys():
            lock_point[current_transaction] = 0
            print("Growing Phase for "+current_transaction)
        else:
            if lock_type=="U":
                lock_point[current_transaction] = 1
                print("Shrinking Phase for "+current_transaction)

        #acquire or revoke lock
        if (lock_type=="S") or (lock_type=="X"):
                print(get_lock(data_item,lock_type,current_transaction))
        else:
            if lock_point[current_transaction]==1:
                print(revoke_lock(data_item, current_transaction))
                check_waiting()

        print("Data Item and Lock : ",data_item_locks)
        print("Data Item Lock Holders : ",lock_holders)
        #print(lock_point)
        print("Waiting for Item : ",waiting)

        if len(lock_point)==0:
            print("All Transactions Ended")
            break

    #get next instruction
    instruction = input("Enter instruction:")