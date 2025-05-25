> This section is not based on reverse engineered data from the machine at the Arithmeum, instead it is essentially a
> summary of parts of US patent 4611307.

#### General operation

To use a Mathatron as a basic calculcator, the `PROGRAM MODE` switch has to be set to `NORMAL`[^1]. After turning the
main power switch to `ON`, the `START` key has to be used to prepare the machine for operation. This causes the `READY`
light to come on. After this, the machine can be operated using "normal" (infix) mathematical expressions, e.g. `12 + 17
/  4`. All entered numbers and operators are printed to the paper tape. After each keypress, the `READY` light should
briefly go out before coming back on[^2]. Pressing `=` prints the result of the expression and returns the machine to
"standby" mode (i.e. `START` has to be pressed before the next computation).

- Opening brackets at the start and closing brackets at the end of the expression can be ommited.
- The `ZEROS` button allows the user to use scientific notation: Entering a number `a`, pressing `ZEROS` and entering a
    number `b` corresponds to entering the number `a * 10^b`[^3].

The 8 data registers[^4] are referred to as `S1` to `S8`. To store a value in one of them, enter the value (or a formula
computing the value) and press the `=S` key, followed by the index of the data register. The `STORE` light will come on
while the Mathatron waits for the register index to be entered[^5]. After this, the value can be used in computations by
entering `S` followed by the register index at any point inside the formula. The register contents can also be printed
using `PRINT` followed by the register index.

#### Programming

The Mathatron is programmed by selecting the `LEARN` mode and entering a sequence of equations. These equations will
typically use the `S`-registers for intermediate results and possibly some inputs. To run the program, the `AUTO` button
is used in one of the other modes (`NORMAL`, `BRANCH`, `STOP`). The Mathatron will then essentially simulate the same
sequence of keystrokes used to create the program.  
Every time a constant[^6] is encountered, the program is interrupted and the user is asked to input the correct
value[^7]. This makes programming for "simple" repetitive tasks very intuitive: To compute e.g. the same expression for
every row of a table, it is enough to enter the expression once for the first row while in `LEARN` mode. Afterwards, it
is enough to enter the contents of the table into the calculator, treating `AUTO` as a "next field" key.  The behavior
upon reaching the end of the entered program depends on the selected mode:
1. In `NORMAL` mode, the program continues from the start as an infinite loop.
2. In `STOP` mode, the program will stop after a single execution. It may be necessary to press the `AUTO` button once
   for every unused program step (of 24 or 48) to return to the start of the program, but this may be a mistake in the
   patent.
3. In `BRANCH` mode, the program will be repeated if the last result computed before the end of the program was
   negative. This is primarily intended for iterative numerical methods (e.g. Newton's method), where the last result
   might indicate whether the remaining error is below some set threshold. In this application, no values are entered
   into the program. The `BRANCH` mode can also be used to accumulate some expression over an arbitrary number of input
   values, e.g. computing $\sum_{i = 0}^n x_i^2$.

#### Prewired programs

Each Mathatron calculator comes with a number of "pre-wired" programs. These are commonly used programs that can be used
at the push of a button. The most common example (present in all machines?) is the square-root program, approximating
the square root of the value in register `S1` and storing the result in `S3`. Other programs are available depending on
the type of Mathatron, e.g. `8-48S` machines contain pre-wired programs for various statistical functions. These
pre-wired programs are entered into the same program storage used for user programs. This has two direct consequences
that may not be obvious from general information on the Mathatron:
- Using a pre-wired program automatically erases the current user program.
- Pre-wired programs (including the square-root function) cannot be used as steps in user programs.

#### A note on Turing completeness

It is not entirely clear whether the Mathatron (in `BRANCH` mode) should be considered Turing complete. This question is
of interest since Turing completeness is often a consideration when deciding whether a device should be considered a
computer or a calculator. Clearly, the computation model needs to be generalized to provide arbitrary amounts of memory.
Since there is no indirect addressing, this has to be done by making the memory available in each register infinite
instead of providing an infinite number of registers. There are (at least) two somewhat natural ways to generalize the
floating point values stored in the registers:
1. Registers store rational numbers.
2. Registers store a product of an integer with a power of 10. Here, the exponent cannot be an arbitrary integer, since
   e.g. division by 3 would not have a well-defined result. Instead, the exponent has to have a fixed minimum value.

Intuitively, the important difference between these two approaches is that the second allows access to individual digits
of an integer value `a`: For example, the last (least significant) digit can be accessed using `a - (a / 10^(e - 1)) *
10^(e - 1)`, where `e` is the minimum value of the implicit exponent. The second part of the formula can be interpreted
as shifting `a` to the right and then back such that the least significant digit cannot be expressed in the intermediate
result. This allows a register to be used as an infinite stack (or one side of the tape of a turing machine).

See [On the control power of integer division](https://www.sciencedirect.com/science/article/pii/0304397583901299) for a
full proof that the second model is Turing complete, noting that this number model is equivalent to integers. I am not
aware of a proof that the first model is not Turing complete. Some results from the same paper suggest that it is not,
but they only apply to numbers that can appear as intermediate results after a fixed number of iterations. These values
*can* be computed as the final program output (after a non-constant number of iterations), so this is not enough to
prove incompleteness.

[^1]: `BRANCH` and `STOP` are likely to work as well, but this has not been tested and is not specified in the patent.
[^2]: The `READY` light is extinguished during processor activity. This can cause confusion since there is no external
    way to distinguish between operation and "standby" (`START` not pressed/computation completed).
[^3]: If the patent is accurate, negative values of `b` are not supported.
[^4]: Or 4 in a Mathatron 4-24
[^5]: This light bulb is missing in the Bonn machine, it is not clear when it was removed.
[^6]: A constant is defined as a numerical constant followed by an operator. It is not clear whether `=S` is considered
    an operator in this context.
[^7]: For more complex programs, this is of course a problematic behavior: Such programs are likely to contain constants
    that are not supposed to be modified (e.g. π). The documentation stores these "global" constants in register before
    the program is started, which still seems cumbersome and error-prone.
