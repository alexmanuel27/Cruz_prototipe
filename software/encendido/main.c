#include <avr/interrupt.h>
#include <avr/io.h>
#include <avr/sleep.h>
#include <avr/cpufunc.h>

#include "control.h"

#define BUTTON PIN1_bm
#define ALARM PIN2_bm
#define POWER_ON PIN3_bm
#define SHUTDOWN_REQUEST PIN4_bm
#define CUT_ACK PIN5_bm

static PowerControl state;

ISR(TCB0_INT_vect)
{
    TCB0.INTFLAGS = TCB_CAPT_bm;
    uint8_t inputs = PORTA.IN;
    power_tick(&state, !(inputs & BUTTON), !(inputs & ALARM), inputs & CUT_ACK);

    if (state.powered) {
        PORTA.OUTSET = POWER_ON;
    } else {
        PORTA.OUTCLR = POWER_ON;
    }

    // Open drain. R22 pulls the Pi input up to the Pi's own 3.3 V rail.
    if (state.request_ms) {
        PORTA.DIRSET = SHUTDOWN_REQUEST;
    } else {
        PORTA.DIRCLR = SHUTDOWN_REQUEST;
    }
}

int main(void)
{
    PORTA.OUTCLR = POWER_ON | SHUTDOWN_REQUEST;
    PORTA.DIRSET = POWER_ON;
    PORTA.DIRCLR = SHUTDOWN_REQUEST | BUTTON | ALARM | CUT_ACK;
    state.alarm_was_low = !(PORTA.IN & ALARM);

    // Either oscillator fuse setting is supported. Run at 4 or 5 MHz.
    _PROTECTED_WRITE(CLKCTRL.MCLKCTRLB, CLKCTRL_PDIV_4X_gc | CLKCTRL_PEN_bm);
    bool osc16 = (FUSE.OSCCFG & FUSE_FREQSEL_gm) == FREQSEL_16MHZ_gc;
    TCB0.CCMP = osc16 ? 3999 : 4999;
    TCB0.INTFLAGS = TCB_CAPT_bm;
    TCB0.INTCTRL = TCB_CAPT_bm;
    TCB0.CTRLA = TCB_CLKSEL_CLKDIV1_gc | TCB_ENABLE_bm;
    set_sleep_mode(SLEEP_MODE_IDLE);
    sei();

    for (;;) {
        sleep_mode();
    }
}
