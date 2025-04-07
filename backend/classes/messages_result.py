"""
    Messages for UI
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203,C0412

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Optional

@dataclass_json
@dataclass
class MessagesResult:
    """Messages result"""
    messages    : Optional[list[str]] = field(default_factory=list)
    debugs      : Optional[list[str]] = field(default_factory=list)
    errors      : Optional[list[str]] = field(default_factory=list)
    used_tokens : Optional[int]       = 0
    used_cost   : Optional[float]     = 0.0
    
    def add_tokens(self, tokens : int, cost : float):
        """Add tokens"""
        self.used_tokens += tokens
        self.used_cost   += cost
        
    def message(self, message : str):
        """Add message"""
        if not self.messages:
            self.messages = []
        self.messages.append(message)
        
    def debug(self, message : str):
        """Add debug"""
        if not self.debugs:
            self.debugs = []
        self.debugs.append(message)
        
    def error(self, message : str):
        """Add error"""
        if not self.errors:
            self.errors = []
        self.errors.append(message)    
        
    def merge(self, other : 'MessagesResult'):
        """Merge"""
        if other.messages:
            if not self.messages:
                self.messages = []
            self.messages.extend(other.messages)
        if other.debugs:
            if not self.debugs:
                self.debugs = []
            self.debugs.extend(other.debugs)
        if other.errors:
            if not self.errors:
                self.errors = []
            self.errors.extend(other.errors)
        self.used_tokens += other.used_tokens
        self.used_cost   += other.used_cost