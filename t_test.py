# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 21:07:07 2019

@author: Mingliang Wang
"""
import datetime
from random import randint
import requests
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy import stats


localhost ='127.0.0.1'

# set the max and min values for item
min_value = 1
max_value = 10
 
# Create arrays to store the response time of requests
N = 10
network_delay = np.zeros((N,2))
start_test = time.time()
app_type = ['safe', 'vulnerable']
text_file = open("network_delay.txt", "w")
for type_num in range(0,2):
    for j in range(0,N,1):
        item = str(randint(min_value,max_value))
        id_num = str(1)
        #    randint(min_value-1,max_value-5)
        url = 'http://'+ localhost + ':5000/' + app_type[type_num]+'/'+ item + '/page?id='+ id_num 
        start = time.time() # record the start time
        r = requests.get(url)
        network_delay[j,type_num] = time.time() - start # calculate the response time
        # record the url and response
        text_file.write(url +'  '+'%s\r\n' %network_delay[j,type_num])
text_file.close()

np.mean(network_delay[:,0])
np.mean(network_delay[:,1])
np.std(network_delay[:,0])
np.std(network_delay[:,1])
np.mean(network_delay[:,0])/2+np.mean(network_delay[:,1])/2

#plot the data of the tests    
plt.figure(1, figsize=(10,4))
plt.subplot(121)
plt.title('network delay')
plt.plot(network_delay[:,0],'-x',label='safe')
plt.plot(network_delay[:,1],'-o',label='vuln')
plt.ylabel('Response time')
plt.xlabel('Request') 
plt.legend(loc='upper left')  
plt.subplot(122)  
plt.figure(1, figsize=(8,4))
network_delay_time = np.concatenate((network_delay[:,0], network_delay[:,1]),axis=0)
plt.hist(network_delay_time,density = True, bins =20)
plt.xlabel('Response time')
plt.ylabel('Probability') 
# Create arrays to store the response time of requests
N=5
A_attack_time = np.zeros((N,1))
A_other_time = np.zeros((N,1))
B_attack_time = np.zeros((N,1))
B_other_time = np.zeros((N,1))

# Use for loop to send out the requests
for j in range(0,N,1):
#    attack request of the safe url we call A
    item = str(randint(min_value,max_value))
    sleep_time = str(2)
#    randint(min_value-1,max_value-5)
    url_A_attack = 'http://'+ localhost + ':5000/safe/'+ item + '/page?id=SLEEP(' + sleep_time + ')'
    start = time.time() # record the start time
    r = requests.get(url_A_attack)
    A_attack_time[j] = time.time() - start # calculate the response time

 #    attack request of the vulnerable url
    url_B_attack = 'http://'+ localhost + ':5000/vulnerable/'+ item + '/page?id=SLEEP(' + sleep_time + ')'
    start = time.time()
    r = requests.get(url_B_attack)
    B_attack_time[j] = time.time() - start


## set the significant level alpha = 10**(-6) = type I error
alpha = 10**(-6)

start_alg = time.time()
# we can use the package to do the t test
tA, pA = stats.ttest_ind(A_attack_time,network_delay_time, equal_var=False)
tB, pB = stats.ttest_ind(B_attack_time,network_delay_time, equal_var=False)
alg_time = time.time() - start_alg
print('algorithm time'+' '+ str(alg_time))

# decision
if pA < alpha:
    print('the url A is vulnerable')
else:
    print('the url A is safe')

if pB < alpha:
    print('the url B is vulnerable')
else:
    print('the url B is safe')
test_time =  time.time() - start_test
print('test time'+' '+ str(test_time))

#plot response time vs each request
plt.figure(2, figsize=(10,4))
plt.subplot(121)
plt.plot(A_attack_time, 'r-o', label='attack')
plt.title('response time of safe url')
plt.xlabel('request #')
plt.ylabel('Response time')
plt.plot(network_delay_time,'-x',label='network delay')
plt.xlabel('request #')
plt.ylabel('Response time')
plt.legend(loc='upper right')       
plt.subplot(122)
plt.title('response time of vulnerable url')
plt.plot(B_attack_time,'r-o',label='attack')
plt.xlabel('request #')
plt.ylabel('Response time')
plt.plot(network_delay_time,'-x',label='network delay')
plt.legend(loc='upper right')  


#plot the boxplot of the tests
plt.figure(3, figsize=(10,4))
plt.subplot(121)
plt.boxplot([A_attack_time,network_delay_time])
plt.title('Blind SQL injection test for SAFE url')
plt.xticks([1, 2], ['attack', 'network delay'])
plt.ylabel('Response time')
plt.subplot(122)
plt.boxplot([B_attack_time,network_delay_time])
plt.title('Blind SQL injection test for VULNERABLE url')
plt.ylabel('Response time')
plt.xticks([1, 2], ['attack', 'network delay'])
