"""Closure-register primitives for phase-before-pi experiments."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


@dataclass(frozen=True)
class ClosureRegister:
    """Finite cycle state with no primitive radian or geometry assumption."""

    modulus: int
    state: int = 0

    def __post_init__(self) -> None:
        if self.modulus <= 0:
            raise ValueError("modulus must be positive")
        object.__setattr__(self, "state", self.state % self.modulus)

    @property
    def cycle_fraction(self) -> Fraction:
        """Return the phase as completed-cycle fraction k/N."""
        return Fraction(self.state, self.modulus)

    @property
    def full_closure(self) -> bool:
        """True when the register has returned to the cycle origin."""
        return self.state == 0

    @property
    def half_closure(self) -> bool:
        """True at the opposite cycle point when the register has even size."""
        return self.modulus % 2 == 0 and self.state == self.modulus // 2

    def advance(self, ticks: int = 1) -> "ClosureRegister":
        """Advance by ticks modulo the closure count."""
        return ClosureRegister(self.modulus, self.state + ticks)


@dataclass(frozen=True)
class RelationClosureEvent:
    """One relation-channel update and its closure readout."""

    step: int
    channel: str
    before_state: int
    after_state: int
    full_closure: bool
    half_closure: bool

    @property
    def label_free_readout(self) -> tuple[int, bool, bool]:
        """Readout with channel labels erased for relabeling tests."""
        return (self.after_state, self.full_closure, self.half_closure)


@dataclass(frozen=True)
class RelationClosureTrace:
    """A finite walk among relation channels, not positions in space."""

    channels: tuple[str, ...]
    modulus: int
    events: tuple[RelationClosureEvent, ...]

    @property
    def label_free_readout(self) -> tuple[tuple[int, bool, bool], ...]:
        """Closure/interference receipt independent of channel names."""
        return tuple(event.label_free_readout for event in self.events)

    @property
    def full_closure_count(self) -> int:
        return sum(1 for event in self.events if event.full_closure)

    @property
    def half_closure_count(self) -> int:
        return sum(1 for event in self.events if event.half_closure)


def run_relation_closure_trace(
    channels: Iterable[str],
    schedule: Iterable[int],
    modulus: int,
    *,
    initial_state: int = 0,
    ticks_per_update: int = 1,
) -> RelationClosureTrace:
    """Run a relation-channel schedule through a closure register.

    The schedule names eligible relation channels by index. It does not name
    x/y/z directions, positions, angles, radians, or spatial neighbors.
    """
    channel_tuple = tuple(channels)
    if not channel_tuple:
        raise ValueError("channels must not be empty")
    if len(set(channel_tuple)) != len(channel_tuple):
        raise ValueError("channels must be unique")

    register = ClosureRegister(modulus, initial_state)
    events: list[RelationClosureEvent] = []
    for step, channel_index in enumerate(schedule):
        if channel_index < 0 or channel_index >= len(channel_tuple):
            raise ValueError("schedule channel index out of range")
        before_state = register.state
        register = register.advance(ticks_per_update)
        events.append(
            RelationClosureEvent(
                step=step,
                channel=channel_tuple[channel_index],
                before_state=before_state,
                after_state=register.state,
                full_closure=register.full_closure,
                half_closure=register.half_closure,
            )
        )

    return RelationClosureTrace(
        channels=channel_tuple,
        modulus=modulus,
        events=tuple(events),
    )
