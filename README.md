Leetcode Downloader  
=======

This script can be used to download all your leetcode submissions.  

Usage:  
----

    ./leetcode_downloader.py USERNAME PASSWORD
    
Node:  
-----
(1) C++ is the only supported language. But you can easily modify this script to support others.  
(2) This script will only download the latest successful submission for each problem. And if your latest submission is not in the most recent submission page of the problem, a warning will be printed and the current problem will be skipped.    
(3) If a piece of code for one problem is found locally, the problem will be skipped. So if you want to replace the old local AC codes with the new ones, you have to delete the old ones manually.  

License:  
--------
Do What the Fuck You Want to Public License  

