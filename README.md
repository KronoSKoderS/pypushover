# py-pushover
Python bindings to the Push Over API.  Supports both python 2 and 3.  

# Usage
    
Basic Usage:
-----------
    import py_pushover as py_po
    pm = py_po.PushManager('<Token>', '<Group_Key>')
    pm.push_notification('Message Body', title="Title")
    
Changing Sounds:
----------------
    # Send notification with the Long Pushover Echo notification sound
    pm.push_notification('Title', 'Message Body', sound=py_po.Sounds.Long_Pushover_Echo)
    
Select Priority:
----------------
    # Send notification with the Lowest Priority
    pm.push_notification('Title', 'Message Body', priority=py_po.Priority.Lowest)
    pm.push_notification('Title', 'Message Body', priority=py_po.Emergency, retry=30, expire=3600)

Check Receipt:
--------------
    # Can check that last responses receipt (Note push notificiaton with a priority of Emergency is required first)
    pm.check_receipt()
    # Can check a custom receipt
    pm.check_receipt('<receipt token>')



    
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
* <strike>Receipt API</strike>
* Subscriptions API
* Group Management API
* Licensing API
* BETA Open Client API