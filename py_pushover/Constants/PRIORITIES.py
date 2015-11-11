"""
Priority - Collection of Priorities.

This is to be used with the 'priority' argument of the push_message function/method.

see also: https://pushover.net/api#priority
"""
LOWEST = -2     # no notification/alert
LOW = -1        # quiet notification
NORMAL = 0      # normal
HIGH = 1        # high-priority (bypass user's quiet hours)
EMERGENCY = 2   # require confirmation from the user (bypass users's quiet hours)
