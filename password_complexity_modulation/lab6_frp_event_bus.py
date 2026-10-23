"""
Lab Work #6: Functional Reactive Programming (FRP) & Event Handling
Satbayev University CSE6031 / Functional Programming Course Project
Topic: Password Complexity Modulation

Key Requirements:
1. Mini Event Bus architecture.
2. Keystroke / input events and timer events.
3. Subscriber / handler functions (Reactive Password Strength Meter, Dynamic Policy Escalator, Adaptive Throttler).
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any
import time
from .functional_core import assess_password, EntropyAssessment, ComplexityPolicy


@dataclass(frozen=True)
class Event:
    """Immutable event structure."""
    event_type: str
    payload: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)


class MiniEventBus:
    """
    Mini Functional Reactive Event Bus.
    Supports event subscription, unsubscription, filtered stream dispatch, and subscriber pipelines.
    """
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Event], None]]] = {}
        self._event_history: List[Event] = []

    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> Callable[[], None]:
        """Subscribes a pure or side-effecting handler. Returns an unsubscribe thunk."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

        def _unsubscribe():
            if event_type in self._subscribers and handler in self._subscribers[event_type]:
                self._subscribers[event_type].remove(handler)
        return _unsubscribe

    def publish(self, event: Event) -> None:
        """Dispatches an event to all registered subscribers."""
        self._event_history.append(event)
        handlers = self._subscribers.get(event.event_type, [])
        for handler in handlers:
            handler(event)

    def get_history(self) -> List[Event]:
        """Returns immutable copy of event log."""
        return list(self._event_history)

    def clear(self) -> None:
        self._subscribers.clear()
        self._event_history.clear()


# =========================================================
# REACTIVE SUBSCRIBERS / HANDLERS
# =========================================================

class ReactiveStrengthMeter:
    """Subscriber: Reacts to 'PASSWORD_INPUT' events and updates live metrics."""
    def __init__(self):
        self.latest_assessment: EntropyAssessment = assess_password("")
        self.history: List[EntropyAssessment] = []

    def handle_input(self, event: Event) -> None:
        if event.event_type == "PASSWORD_INPUT":
            pwd = event.payload.get("password", "")
            self.latest_assessment = assess_password(pwd)
            self.history.append(self.latest_assessment)


class DynamicPolicyModulator:
    """
    Subscriber: Complexity Modulation Engine.
    Reacts to 'SECURITY_THREAT_DETECTED' or rapid failed attempts
    by escalating minimum password complexity policy.
    """
    def __init__(self):
        self.current_policy = ComplexityPolicy(
            min_length=8,
            require_digits=True,
            require_uppercase=False,
            require_symbols=False,
            min_entropy_bits=35.0,
        )
        self.threat_level = "NORMAL"

    def handle_threat(self, event: Event) -> None:
        if event.event_type == "THREAT_ESCALATION":
            level = event.payload.get("level", "ELEVATED")
            self.threat_level = level
            if level == "ELEVATED":
                self.current_policy = ComplexityPolicy(
                    min_length=12,
                    require_digits=True,
                    require_uppercase=True,
                    require_symbols=False,
                    min_entropy_bits=55.0,
                )
            elif level == "CRITICAL":
                self.current_policy = ComplexityPolicy(
                    min_length=16,
                    require_digits=True,
                    require_uppercase=True,
                    require_symbols=True,
                    min_entropy_bits=80.0,
                )


class AdaptiveThrottler:
    """
    Subscriber: Implements exponential backoff delay based on failed attempts.
    Ties directly to Lab 6 Exponential distribution delay modeling.
    """
    def __init__(self, base_delay_ms: float = 200.0, rate_lambda: float = 0.5):
        self.failed_attempts = 0
        self.current_delay_ms = 0.0
        self.base_delay_ms = base_delay_ms
        self.rate_lambda = rate_lambda

    def handle_auth_result(self, event: Event) -> None:
        if event.event_type == "AUTH_FAILED":
            self.failed_attempts += 1
            # Exponential backoff delay
            self.current_delay_ms = self.base_delay_ms * (2 ** (self.failed_attempts - 1))
        elif event.event_type == "AUTH_SUCCESS":
            self.failed_attempts = 0
            self.current_delay_ms = 0.0

