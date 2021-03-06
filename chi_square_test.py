# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 11:09:23 2019

@author: miwan
"""
from random import randint
import requests
import numpy as np
import time
import matplotlib.pyplot as plt
from scipy import stats

localhost ='127.0.0.1'

# set the max and min values for item
min_value = 1
max_value = 3


# Create arrays to store the response time of requests
N = 10
A_response_time = np.zeros((N,1)) # url A is the safe url
B_response_time = np.zeros((N,1)) # url B is the vulnerable url
sleep_time = np.zeros((N,1))
start_test = time.time()


N = 10
network_delay = np.zeros((N,2))

app_type = ['safe', 'vulnerable']

# Use for loop to send out the requests for network delay
#for j in range(0,N-1,1):
#    item = str(randint(min_value,max_value))
#    id_num = str(1)
#    item = str(randint(min_value,max_value))
#    # network delay for url b
#    url = 'http://'+ localhost + ':5000/' + app_type[0]+'/'+ item + '/page?id='+ id_num
#    start = time.time() # record the start time
#    r = requests.get(url)
#    A_response_time[j] = time.time() - start # calculate the response time
#    
#    # network delay for url b
#    url = 'http://'+ localhost + ':5000/' + app_type[1]+'/'+ item + '/page?id=' + id_num
#    start = time.time() # record the start time
#    r = requests.get(url)
#    B_response_time[j] = time.time() - start # calculate the response time
#        # record the url and response

#plt.hist(np.concatenate((A_response_time,B_response_time), axis = 0),density = True, bins =20)

 "simulation"
for j in range(0, N-1,1):
    A_response_time[j] = abs(np.random.lognormal(0.98, 0.5, 1)[0]) # url A is the safe url
    B_response_time[j] = abs(np.random.lognormal(0.98, 0.5, 1)[0])# url B is the vulnerable url

start_test = time.time()
item = str(randint(min_value,max_value))
# set the sleep time
sleep = 3
#    sleep = 0.5*j # instead of the catergorical input, we can also set sleep time as a series of real number
sleep_time[N-1] = sleep  # varied from 0 to 3
'request of the safe url'
url_A = 'http://'+ localhost + ':5000/safe/'+ item + '/page?id=SLEEP(' + str(sleep) + ')'
start = time.time() # record the start time
r = requests.get(url_A) 
A_response_time[N-1] = time.time() - start # calculate the response time

# 'simulation'
#A_response_time[N-1] = abs(np.random.lognormal(0.98, 0.5, 1)[0])

'request of the vulnerable url'
url_B = 'http://'+ localhost + ':5000/vulnerable/'+ item + '/page?id=SLEEP('+ str(sleep) + ')'
start = time.time()
r = requests.get(url_B)
B_response_time[N-1] = time.time() - start

# 'simulation'
#B_response_time[N-1] = abs(np.random.lognormal(0.98, 0.5, 1)[0]) + 5* sleep

mean_A = np.mean(np.log(A_response_time))
sigma_A = np.var(np.log(A_response_time))
epsilon_A =  np.log(A_response_time) - mean_A
phi =  np.mat(sleep_time)

chi2_A = N/sigma_A* np.mat(epsilon_A).T* phi*np.linalg.inv(phi.T*phi)*phi.T*np.mat(epsilon_A)

mean_B = np.mean(np.log(B_response_time))
sigma_B = np.var(np.log(B_response_time))
epsilon_B =  np.log(B_response_time) - mean_B
chi2_B = N/sigma_B* np.mat(epsilon_B).T* phi*np.linalg.inv(phi.T*phi)*phi.T*np.mat(epsilon_B)

'calculate the p value'
p_A = 1- stats.chi2.cdf(chi2_A, df=1)
p_B = 1- stats.chi2.cdf(chi2_B, df=1)


alpha =10**(-6)
# decision
if p_A < alpha:
    print('the url A is vulnerable')
else:
    print('the url A is safe')

if p_B < alpha:
    print('the url B is vulnerable')
else:
    print('the url B is safe')
    
plt.figure(1, figsize=(8,4))
plt.title('response time')
plt.plot(sleep_time, B_response_time,'ro',label='vuln')
plt.plot(sleep_time, A_response_time,'bx',label='safe')
plt.ylabel('Response time')
plt.xlabel('Sleep time') 
plt.legend(loc='upper left')   

# Calculate the test time
test_time =  time.time() - start_test
print('Total test time'+' '+ str(test_time))
 

#critical_value = chi2.ppf(q=1-alpha , df=1)
#plt.figure(2)
#accept_region_xs = np.arange(0, critical_value, 0.001)
#plt.fill_between(accept_region_xs, chi2.pdf(accept_region_xs, 1), color='green')
#reject_region_xs = np.arange(critical_value, critical_value+2, 0.001)
#plt.fill_between(reject_region_xs, chi2.pdf(reject_region_xs, 1), color='red')





