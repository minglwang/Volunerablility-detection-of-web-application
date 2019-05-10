# Web_application_vulnerability_detection
> Time based algorithm to detect the vulnerability of SQL injection attacks
<p align ="center">
  <img width ="400" height ="300", src = https://github.com/minglwang/Web_App_Vulnerability_Detection/blob/master/confidence%20interval.png>
</p>  

# Table of Content
- [Description](#discription)
- [How To Use](#how-to-use)

# Description
**Blind SQL injections** are time-based SQL attacks that request web applications to sleep for a specified amount of time (*Sleep time*) . Typically, the response time of **vulnerable web applications will be affected** by such attacks **while safe web application will not**. However, the response time is contaiminated by the *stochastic network delay*. In other word,

*Response time = Sleep time + Stochastic network delay*

So the response time based descrimination of a web application will result in **false positive** (type I error) which means we classify the safe web application as a vulnerable one. 

To deal with the false positive problem and make sure the is online appliable, we designed a time-based algorithm such that **the false positive rate** less than a small positive value, e.g. 0.01% and can be **completed within a few seconds**.

Two approaches are developed
1. a t-test approach
2. Chi-square test approach. 

Both approaches contain sampling the *stochastic network delay* which may take 1 or 2 minutes. This sampling can do offline.
The t-test approach takes about a 1-2 minutes which is too long for online usage.
The advantage of Chi-square test is that it can do the discrimination (detection) by only one request which **completes within a few seconds** and maintain the **the false positive rate** at the same time.

The basic idea of the two approaches are explained in 
[report file](https://github.com/minglwang/Web_App_Vulnerability_Detection/blob/master/Mingliang_Report.pdf). 

# How To Use
The procedure of using the code is 
1. run "app.py" which is a Python code simulating the web applications (both safe and unsafe ones).
2. run the "t_test.py" to run the t-test approach
3. run the "chi_square_test.py" to run the proposed chi-square test approach 

[Back To The Top](#Web_application_vulnerability_detection)

