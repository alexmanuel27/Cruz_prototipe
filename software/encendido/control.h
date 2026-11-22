#ifndef CRUZ_CONTROL_H
#define CRUZ_CONTROL_H

#include <stdbool.h>
#include <stdint.h>

enum { DEBOUNCE_MS = 30, HOLD_MS = 5000, SHUTDOWN_PULSE_MS = 250 };

typedef struct {
    uint16_t held_ms;
    uint16_t request_ms;
    uint8_t debounce_ms;
    bool pressed;
    bool consumed;
    bool alarm_was_low;
    bool powered;
} PowerControl;

static inline void power_tick(PowerControl *state, bool button_low,
                              bool alarm_low, bool linux_finished)
{
    bool wake_alarm = alarm_low && !state->alarm_was_low;
    state->alarm_was_low = alarm_low;

    if (button_low == state->pressed) {
        state->debounce_ms = 0;
    } else if (++state->debounce_ms == DEBOUNCE_MS) {
        state->pressed = button_low;
        state->debounce_ms = 0;
        if (!state->pressed) {
            state->consumed = false;
        }
    }

    if (state->request_ms) {
        --state->request_ms;
    }

    if (state->powered && linux_finished) {
        state->powered = false;
        state->held_ms = 0;
        state->request_ms = 0;
        state->consumed = state->pressed || button_low;
        return;
    }

    if (!state->powered && wake_alarm && !linux_finished) {
        state->powered = true;
        state->held_ms = 0;
        state->consumed = state->pressed || button_low;
    }

    if (!state->pressed || !button_low) {
        state->held_ms = 0;
        return;
    }

    if (!state->consumed && ++state->held_ms >= HOLD_MS) {
        state->consumed = true;
        state->held_ms = 0;
        if (state->powered) {
            state->request_ms = SHUTDOWN_PULSE_MS;
        } else if (!linux_finished) {
            state->powered = true;
        }
    }
}

#endif
