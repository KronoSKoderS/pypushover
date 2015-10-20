"""
Priority - Collection of Priorities.

This is to be used with the 'priority' arguemnt of the PushOverManager.push_notification method.

see also: https://pushover.net/api#priority
"""
Lowest = -2     # no notification/alert
Low = -1        # quiet notification
Normal = 0      # normal
High = 1        # high-priority (bypass user's quiet hours)
Emergency = 2   # require confirmation from the user (bypass users's quiet hours)
