# py-pushover
Python bindings to the Push Over API.  Supports both python 2 and 3.  

# Usage
    
Basic Usage:
-----------
    import py-pushover as po
    pm = po.PushManager('<Token>', '<Group_Key>')
    pm.push_notification('Message Body', title="Title")
    
Changing Sounds:
----------------
    # Send notification with the Long Pushover Echo notification sound
    pm.push_notification('Title', 'Message Body', sound=po.Sounds.Long_Pushover_Echo)
    
Select Priority:
----------------
    # Send notification with the Lowest Priority
    pm.push_notification('Title', 'Message Body', priority=po.Priority.Lowest)
    
# Supported API's:
The following API's are currently supported:
* Message API including optional params:
    * device
    * title
    * url
    * url_title
    * priority
    * timestamp
    * sound

# Future Work:
* Emergency Priority confirmation and additional support
* Asynchronous method for `push_notification`
* User/Group Verification API
* Receipt and Callback API
* Subscriptions API
* Group Management API
* Licensing API
* BETA Open Client API