The printer logic is currently the only section of the logic that I have traced out (see [logic](./logic.md) for details
on the technique used). In the machine at the Arithmeum, this logic is located in the rightmost column (F) of the upper
front right processor PCB. The easiest way to check whether this is the same on another machine is to check whether the
base of transistor 39 is connected to one of the pins of the printer position sensor (see [printer
section](./printer.md)). Additionally, there should be 12 small ceramic capacitors between transistors 1-14, an
electrolytic capacitor inside the logic around transistor 17, and only a single collector resistor for each of the
transistors 27-37.

Transistors 1-14 form a 5-bit counter, indicating the current position of the 20-character type wheel. The first stage
is implemented as a standard RS latch consisting of two NOR gates (one transistor each), while the later stages use
T-flip-flops: The base of a "propagation" transistor is connected to the inverted output of the previous stage through a
capacitor (red, dog-bone type). This produces a pulse whenever the previous stage switches from logical 1 to logical 0
(inverted output: 0 to 1, i.e. 0V to -10V). This pulse is connected to the bases of both transistors in a (TODO name of
this). This counter is fairly sensitive to the values of the capacitors used for both propagation and within the stages,
similar to mechanical calculators with an "instantaneous" carry mechanism.

The 5 outputs bits of the counter are then fed into a comparator. The other input represents the character to be
printed, i.e. the print buffer. When both inputs are identical, the printer hammer is triggered. The comparator circuit
uses a total of 13 transistors, nearly a third of the column (two per bit and three extra to collect the results). For
each input bit, the circuit computes `Ac NOR !Ap` and `!Ac NOR Ap`, where `Ac` is the counter output bit and `Ap` is the
bit in the printer buffer. When both bits are equal, both of these expressions are zero since (exactly) one of the
inputs is 1. When the bits differ, both inputs will be 0 in one expression and both 1 in the other. The former
expression will therefore evaluate to 1. Taking the `OR` (or `NOR`) over all of these values then gives the comparison
result. Presumably due to fan-in limitations, the results of bits 0, 1 and 2 are combined first (`comp0To2`) using an
`OR` gate (`NOR` followed by `NOT`) and only then combined with the remaining results. The inverted signals do not have
to be computed explicitly, the negations of both `Ac` and `Ap` are available from the circuits providing their
non-negated values. 

The counter can be reset by one of two mechanisms. The first is the signal labeled `reset`, which is a buffered version
of the magnetic sensor in the print wheel. `bit0` is not reset by this, presumably since its state is implied by the
state of the motor. The other bits are reset to excess-3 zero, i.e. `1100`. These bits also contain the corresponding
excess-3 value when printing digits. The other reset signal is provided by transistor 26 and is currently somewhat
mysterious. Confusingly, it does not reset either `bit0` or `bit1`.

After the machine is powered on, the position of the type wheel is unknown. As a result, the counter output can only be
trusted after the first time it is reset by the magnetic sensor. This logic is not located in column `F`, and also
appears to be partially broken on the Arithmeum machine. Based on the behavior of that machine, it seems like this is
achieved by pulling all (some?) print buffer bits to `1` for a fixed period at the start of the first print cycle. Since
this is not a valid combination that will ever be reached by the counter, this prevents any printing until the wheel has
completed at least one revolution. In the Arithmeum machine, the inputs are held in this state permanently, but only
some of them. Due to this, the printer works if the first digit is 5 or more (so that the highest bit is set in
excess-3), but spins the print wheel indefinitely if the first digit is 4 or less. After this first digit, all digits
work as expected.

### Connections

This table provides the known base connections of transistors in this column. The same name is used for a transistor and
its collector signal. For signals that I do not understand yet I simply use the transistor number. The collector signal
is the logical NOR of the base signals. Due to the construction method, it is possible and often likely that some base
connections are missing. `cap(S)` indicates that the base is connected to the collector of `S` through a ceramic
capacitor, while `elcap(S)` indicates a connection through an electrolytic capacitor.

|Transistor ID|Collector signal name|Base connections (potentially incomplete)                     |
|-------------|---------------------|--------------------------------------------------------------|
| 1           |bit0                 |nbit0, cap(reset0)                                            |
| 2           |nbit0                |bit0, cap(set0)                                               |
| 3           |prop1                |cap(nbit0)                                                    |
| 4           |bit1                 |prop1, nbit1, cap(nbit1), reset                               |
| 5           |nbit1                |prop1, bit1, cap(bit1)                                        |
| 6           |prop2                |cap(nbit1)                                                    |
| 7           |bit2                 |prop2, nbit2, 26, cap(nbit2), reset                           |
| 8           |nbit2                |prop2, bit2, cap(bit2)                                        |
| 9           |prop3                |cap(nbit2)                                                    |
|10           |bit3                 |prop3, nbit3, cap(nbit3)                                      |
|11           |nbit3                |prop3, bit3, 26, cap(bit3), reset                             |
|12           |prop4                |cap(nbit3)                                                    |
|13           |bit4                 |prop4, nbit4, cap(nbit4)                                      |
|14           |nbit4                |prop3, bit4, 26, cap(bit4), reset                             |
|15           |                     |18, nCompAll                                                  |
|16           |                     |15                                                            |
|17           |                     |                                                              |
|18           |                     |elcap(17)                                                     |
|19           |nCompAll             |compNBit3, compBit3, compNBit4, compBit4, comp0To2            |
|20           |                     |                                                              |
|21           |reset0               |18                                                            |
|22           |set0                 |18                                                            |
|23           |                     |reset0, set0                                                  |
|24           |                     |nbit0, reset0, set0                                           |
|25           |                     |bit0, nbit1, nbit2, bit3, bit4, 18                            |
|26           |                     |cap(25)                                                       |
|27           |compBit0             |bit0                                                          |
|28           |compNBit0            |nbit0                                                         |
|29           |compNBit1            |nbit1                                                         |
|30           |compBit1             |bit1                                                          |
|31           |compNBit2            |nbit2                                                         |
|32           |compBit2             |bit2                                                          |
|33           |compNBit3            |nbit3                                                         |
|34           |compBit3             |bit3                                                          |
|35           |compNBit4            |nbit4                                                         |
|36           |compBit4             |bit4                                                          |
|37           |nComp0To2            |compBit0, compNBit0, compNBit1, compBit1, compNBit2, compBit2 |
|38           |comp0To2             |nComp0To2                                                     |
|39           |nSensor              |[to printer sensor]                                           |
|40           |reset                |nSensor                                                       |
