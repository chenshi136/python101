"""
Robot WCY 包
"""

from .api import call_zhipu_api
from .roles import get_role_system, get_role_personality
from .memory import load_memory, MEMORY_FOLDER, ROLE_MEMORY_MAP
from .logoc import get_portrait

__all__ = [
    'call_zhipu_api',
    'get_role_system',
    'get_role_personality',
    'load_memory',
    'MEMORY_FOLDER',
    'ROLE_MEMORY_MAP',
    'get_portrait',
]





