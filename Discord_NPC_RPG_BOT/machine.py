# Machine.py
from typing import List, Dict, Any, Set

from .sender import Sender
from .base_state import BaseState
from .base_symbol import BaseSymbol


# ==========================================================
# Machine
# ==========================================================

class Machine(Sender):
    def __init__(self):
        super().__init__()
        self.states: List[BaseState] = []
        self.relations: Dict[str, Dict[str, Any]] = {}

    def add_state(self, state: BaseState) -> None:
        self.states.append(state)

    def add_states(self, states: List[BaseState]) -> None:
        self.states.extend(states)

    # ------------------------------------------------------
    # Execução
    # ------------------------------------------------------

    def accepted_symbols(
            self,
            sender: Sender
    ) -> Set[type[BaseSymbol]]:

        symbols = set()

        for state in self.states:
            if state.is_active(self, sender):
                symbols.update(state.symbol_handlers)

        return symbols

    def receive(
        self,
        symbol: BaseSymbol,
        sender: Sender
    ) -> List[Exception]:

        handlers = []

        for state in self.states:
            if state.is_active(self, sender):
                for symbol_cls, entries in state.symbol_handlers.items():
                    if isinstance(symbol, symbol_cls):
                        handlers.extend(entries)

        handlers.sort(key=lambda h: (-h.priority, h.order))

        retornar = {
            "errors": [],
            "retornos": [],
            "called_handlers": len(handlers),
            "called_entries": 0
        }

        for entry in handlers:
            retornar["called_entries"] += 1
            try:
                resp = entry.handler(
                    machine=self,
                    sender=sender,
                    symbol=symbol
                )
                retornar["retornos"].append(resp)
            except Exception as e:
                retornar["errors"].append(e)

        return retornar
