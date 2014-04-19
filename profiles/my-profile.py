#!python
# Your code goes here.
# This profile act as re-visit. When test1 and test have the same
# profile as below.If test1 views test's profile, then test will send
# a message('Nice to meet you') to test1, and test1 can see all the
# message sent from others to test. In this way, the two users can
# leave message to each other.
# Note:You can send yourself a message by view your own profile
# With the new api 'send_msg' and 'get_msg'
import time
global api

api.call('send_msg',msg='Nice to meet you!')
print 'Hello, <i>', api.call('get_visitor'), '</i>'
print '<p>I leave a message for you!</p>'
print 'my message wall:</br>'
wels = api.call('get_msg')
for (k, v) in wels.items():
    print 'from', k, '<ul>'
    i = 0
    for vv in v:
        print '<li>', vv[0], vv[1], '</li>'
    print '</ul>'
