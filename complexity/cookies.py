#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""
    Complexity: cookies.py
    ~~~~~~~~~~~~~~~~~~~~~~
    
    Cookie Tools.

    :copyright: (c) 2014 Luke Southam <luke@devthe.com>.
    :license: New BSD, see LICENSE for more details.
"""

import hmac

try:
    from secrets import COOKIE_SECRET as SECRET
except ImportError:
    print "Critical Error: Can't load cookie secret from secrets.py."
    print "                (Did you remember to create the file?"
    print "                 It's not in the source code repository!)"
    import sys
    sys.exit(1)

# SECRET = '' # base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

class Cookie(object):
    """
    Cookie object to sign and check cookie values.
    Usage:
        >>> print Cookie("I'm some data") # Create a Cookie
        "I'm some data|real-signature"

        >>> print Cookie("I'm some data").data  # get that DATA!
        "I'm some data"
        
        >>> # Untrustworthy source? check that signature!
        >>> print Cookie("I'm some data|real-signature", False).data
        "I'm some data"

        >>> # Well this ones dodgy
        >>> print Cookie("I'm some data|fake-signature", False).data
        None

    """
    def __init__(self, data, new=True):
        if new or data is None:
            self.data = data
        else:
            self.data, self._hash = data.split('|')
            if self != Cookie(self.data):
                self.data = None

    @property
    def hash(self):
        if self.data is None:
            return

        if hasattr(self, '_hash'):
            return self._hash
        
        self._hash = hmac.new(SECRET, self.data).hexdigest()

        return self._hash

    @property
    def value(self):
        if self.data is not None:
            return "%s|%s" % (self.data, self.hash)

    def __str__(self):
        return self.value

    def __ne__(self, other):
        if not isinstance(other, Cookie):
            raise NotImplemented

        return self.value != other.value or self.hash != other.hash

