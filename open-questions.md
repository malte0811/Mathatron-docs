This list contains some strange details I found and was unable to explain, as well as general questions about the
history of Mathatron machines.
- Two parallel resistors in the "resistor cage" dissipate 20W each, for 40W total. There is no forced-air cooling in
    this area, and even without the cover attached the resistors reach 80°C (176°F) within 20 seconds. Both the
    temperature and the total wasted power would suggest that this is not the intended behavior. On the other hand, the
    resistors are Ohmite power resistors rated for operation up to 350°C, so it may be the correct behavior after all.
    There is also another resistor in the resistor cage dissipating multiple Watts, but nowhere near as much as this
    pair.
- Is the -10V rail intended to be at that voltage? In the Arithmeum machine, it seems to be too close to 10V to be
    caused by broken regulation. On the other hand, this would mean that the main logic levels of the machine are -10V
    and 0V. Both the [main Mathatron patent](./patents/US4611307-mathatron-latest.pdf) and some documentation[^1]
    suggest that it should be -5V and 0V.
- What is the correct value, and the purpose, of the large resistor on top of the resistor cage? In the Arithmeum
    machine this is a fixed-value dark green resistor without any markings. In measurements, it shows a very low value,
    but this could also be some other circuitry in parallel with the resistor. In pictures of other machines, this
    resistor seems to be adjustable rather than fixed-value.
- On the right side of the "mixed board", a white/purple striped wire leaves the board and enters a wire harness, only
    to leave the harness a few centimeters later and connect to the board again. The endpoints of the wire are already
    connected by a trace on the board. Was this intended to confuse reverse engineering efforts, or spot direct clones?
    Or is it an artifact from an earlier revision of the machine?
- What is the correct wiring behind the 15-BJT board? In the Arithmeum machine, it appears that this section has been
    modified in some earlier attempted repair/restauration (newer resistor style). Some high-precision resistors are
    placed between DC signals that are also connected by far lower-precision resistors, while some base connections are
    missing series resistors. It seems likely that this was a mistake during the earlier changes.
- The Mathatron at the Arithmeum seems to be a custom model, probably similar to IBMs "Request Price Quotation". How
    does it differ from a normal 8-48S, which seems to be what the customizations are based on?
- What is the full model history of the Mathatron calculator? For example, the [machine owned by Mohamad H.
    Hassoun](./known-machines.md) looks identical to the Arithmeum machine on the outside, but uses a different layout
    of the logic unit and contains an additional board in the top section.
