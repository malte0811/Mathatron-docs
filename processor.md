> This section is not based on reverse engineered data from the machine at the Arithmeum, instead it is essentially a
> summary of the patent US 4611307.

The Mathatron is a [serial computer](https://en.wikipedia.org/wiki/Serial_computer), processing one 4-bit digit at a
time. This allows the processor to work on 48-bit registers with much fewer transistors than one might expect from
modern machines: The processor only has to be aware of its current position within the register and to be able to
perform basic digit-wise operations. Therefore, the transistor count depends (mostly) logarithmically on the register
size, rather than the linear or often super-linear dependence found in modern processors. On the other hand, processing
time is linear in the size of the registers: Only a single digit is processed in each "processor cycle". The serial
nature of the processor also explains the choice of shift registers for the main memory: they form the "natural" data
storage for a serial processor, presenting data in the digit-by-digit form required by serial processors.

The control logic of the processor is organized as a state machine[^1]. Each state is kept for 96 1-bit memory pulses,
i.e. each register is fully shifted through twice in each state. Confusingly, according to the patent the switch between
states ocurs at memory pulse 72, i.e. half-way through the second "pass" of the registers. Figures 8-10 in the patent
show the state sequences for various operations. The index of the state is shown in the top left of each box, while the
circled numbers describe the various "subcommands" controlling the datapath of the processor during this state. These
subcommands can describe direct "actions" (e.g. 51="Print the + character"), but can also describe the "routing" of
information within the processor (e.g. 6="transfer adder output to exponent position of buffer"). All subcommands are
described in the list starting in column 18 of the patent.

### Floating point handling

The state machine diagrams shown in the various subfigures of figure 8 are relatively basic, describing short, fixed
sequences of states. The diagrams in figures 7, 9 and 10 are more interesting. Figure 7 is essentially a formal
description of the [parenthesis handling](./parentheses.md). I have not analyzed figure 10 (describing printing and
single-digit deletion) yet, as it seems to contain some errors and undocumented signals. Figure 9 describes the logic
used to perform a single arithmetic operation on the floating point registers.

TODO describe and include annotated version of figure 9

According to the patent, the worst-case time for a single operation is 125 "cycles" of 96 memory pulses lasting 75µs
each, i.e. nearly a full second. I have not worked out the example for which this worst-case runtime ocurs, it should be
something along the lines of a multiplication/division involving 99...99.

[^1]: The states are referred to as "cycles" in the patent. I will use the modern term "state" in this explanation.
