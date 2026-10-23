"""
Unit Tests for Lab Work #6 (Functional Reactive Programming & Event Handling)
Requirement from 20 Project Topics: Independent Work (SRS) >= 5 tests per lab
"""

from password_complexity_modulation.lab6_frp_event_bus import (
    Event,
    MiniEventBus,
    ReactiveStrengthMeter,
    DynamicPolicyModulator,
    AdaptiveThrottler,
)


def test_mini_event_bus_publish_subscribe():
    """Test 1: Verify publish and subscribe mechanism on MiniEventBus."""
    bus = MiniEventBus()
    received = []

    bus.subscribe("TEST_EVENT", lambda evt: received.append(evt.payload["val"]))
    bus.publish(Event(event_type="TEST_EVENT", payload={"val": 100}))
    bus.publish(Event(event_type="OTHER_EVENT", payload={"val": 200}))

    assert len(received) == 1
    assert received[0] == 100


def test_event_bus_unsubscribe():
    """Test 2: Verify unsubscribing stops receiving events."""
    bus = MiniEventBus()
    received = []

    unsub = bus.subscribe("DATA", lambda evt: received.append(evt.payload["x"]))
    bus.publish(Event(event_type="DATA", payload={"x": 1}))
    assert len(received) == 1

    unsub()  # Unsubscribe
    bus.publish(Event(event_type="DATA", payload={"x": 2}))
    assert len(received) == 1  # No second event received


def test_reactive_strength_meter():
    """Test 3: Verify reactive password strength meter updates upon PASSWORD_INPUT."""
    bus = MiniEventBus()
    meter = ReactiveStrengthMeter()
    bus.subscribe("PASSWORD_INPUT", meter.handle_input)

    bus.publish(Event(event_type="PASSWORD_INPUT", payload={"password": "123"}))
    assert meter.latest_assessment.strength_tier == "Very Weak"

    bus.publish(Event(event_type="PASSWORD_INPUT", payload={"password": "CorrectHorseBatteryStaple2026!"}))
    assert meter.latest_assessment.strength_tier in ("Strong", "Very Strong")
    assert len(meter.history) == 2


def test_dynamic_policy_modulator_threat_escalation():
    """Test 4: Verify policy requirements dynamically escalate upon threat level increase."""
    bus = MiniEventBus()
    modulator = DynamicPolicyModulator()
    bus.subscribe("THREAT_ESCALATION", modulator.handle_threat)

    assert modulator.current_policy.min_length == 8

    # Escalate to ELEVATED
    bus.publish(Event(event_type="THREAT_ESCALATION", payload={"level": "ELEVATED"}))
    assert modulator.current_policy.min_length == 12
    assert modulator.current_policy.require_uppercase is True

    # Escalate to CRITICAL
    bus.publish(Event(event_type="THREAT_ESCALATION", payload={"level": "CRITICAL"}))
    assert modulator.current_policy.min_length == 16
    assert modulator.current_policy.require_symbols is True


def test_adaptive_throttler_exponential_backoff():
    """Test 5: Verify exponential delay modulation upon repeated failed authentications."""
    bus = MiniEventBus()
    throttler = AdaptiveThrottler(base_delay_ms=200.0)
    bus.subscribe("AUTH_FAILED", throttler.handle_auth_result)
    bus.subscribe("AUTH_SUCCESS", throttler.handle_auth_result)

    # 1st fail: 200 ms
    bus.publish(Event(event_type="AUTH_FAILED", payload={}))
    assert throttler.current_delay_ms == 200.0

    # 2nd fail: 400 ms
    bus.publish(Event(event_type="AUTH_FAILED", payload={}))
    assert throttler.current_delay_ms == 400.0

    # 3rd fail: 800 ms
    bus.publish(Event(event_type="AUTH_FAILED", payload={}))
    assert throttler.current_delay_ms == 800.0

    # Success resets backoff
    bus.publish(Event(event_type="AUTH_SUCCESS", payload={}))
    assert throttler.current_delay_ms == 0.0
    assert throttler.failed_attempts == 0


def test_event_history_recording():
    """Test 6: Verify immutable event history log is properly recorded."""
    bus = MiniEventBus()
    bus.publish(Event(event_type="EVT1", payload={"a": 1}))
    bus.publish(Event(event_type="EVT2", payload={"b": 2}))

    history = bus.get_history()
    assert len(history) == 2
    assert history[0].event_type == "EVT1"
    assert history[1].event_type == "EVT2"

