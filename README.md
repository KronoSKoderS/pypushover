# py-pushover
Python bindings to the Push Over API.  Supports both python 2 and 3.  

# Usage
    
Basic Usage:
-----------
    import py-pushover as po
    pm = po.PushManager('<Token>', '<Group_Key>')
    pm.push_notification('Title', 'Message Body')
    
Changing Sounds:
----------------
    # Send notification with the Long Pushover Echo notification sound
    pm.push_notification('Title', 'Message Body', sound=po.Sounds.Long_Pushover_Echo)



# Future Work:
* Emergency Priority confirmation and additional support
* Asynchronous method for `push_notification`
* User/Group Verification API
* Receipt and Callback API
* Subscriptions API
* Group Management API
* Licensing API
* BETA Open Client API