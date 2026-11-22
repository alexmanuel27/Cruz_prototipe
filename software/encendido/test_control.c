#include <assert.h>

#include "control.h"

static void advance(PowerControl *state, unsigned ms, bool button, bool alarm, bool ack)
{
    for (unsigned tick = 0; tick < ms; ++tick) {
        power_tick(state, button, alarm, ack);
    }
}

int main(void)
{
    PowerControl state = {0};
    const unsigned long_press = HOLD_MS + DEBOUNCE_MS - 1;

    advance(&state, long_press - 1, true, false, false);
    assert(!state.powered);
    advance(&state, 1, true, false, false);
    assert(state.powered && !state.request_ms);
    advance(&state, HOLD_MS * 2, true, false, false);
    assert(state.powered && !state.request_ms);

    advance(&state, DEBOUNCE_MS, false, false, false);
    advance(&state, HOLD_MS - 1, true, false, false);
    advance(&state, DEBOUNCE_MS, false, false, false);
    assert(state.powered && !state.request_ms);
    advance(&state, long_press, true, false, false);
    assert(state.powered && state.request_ms == SHUTDOWN_PULSE_MS);
    advance(&state, HOLD_MS, true, false, false);
    assert(state.powered && !state.request_ms);
    advance(&state, 1, true, false, true);
    assert(!state.powered);
    advance(&state, HOLD_MS * 2, true, false, false);
    assert(!state.powered);

    advance(&state, DEBOUNCE_MS, false, false, false);
    advance(&state, 1, false, true, false);
    assert(state.powered);
    advance(&state, 1, false, true, true);
    assert(!state.powered);
    advance(&state, HOLD_MS * 2, false, true, false);
    assert(!state.powered);
    advance(&state, 1, false, false, false);
    advance(&state, 1, false, true, false);
    assert(state.powered);

    PowerControl stale_alarm = {.alarm_was_low = true};
    advance(&stale_alarm, 100, false, true, false);
    assert(!stale_alarm.powered);
}
