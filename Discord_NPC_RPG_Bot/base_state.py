# BaseState.py
from typing import Callable, Dict, Type, List
from dataclasses import dataclass

from .base_symbol import BaseSymbol

# ==========================================================
# BaseState e HandlerEntry
# ==========================================================

@dataclass
class HandlerEntry:
    handler: Callable
    priority: int
    order: int


class BaseState:
    def __init__(self):
        self.symbol_handlers: Dict[Type[BaseSymbol], List[HandlerEntry]] = {}
        self._registration_counter: int = 0

    def register_symbol(
        self,
        symbol_cls: Type[BaseSymbol],
        handler: Callable,
        priority: int = 0
    ) -> None:

        entry = HandlerEntry(
            handler=handler,
            priority=priority,
            order=self._registration_counter
        )

        self._registration_counter += 1

        if symbol_cls not in self.symbol_handlers:
            self.symbol_handlers[symbol_cls] = []

        self.symbol_handlers[symbol_cls].append(entry)

    def is_active(self, machine, sender) -> bool:
        raise NotImplementedError
