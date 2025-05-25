> This section is not based on reverse engineered data from the machine at the Arithmeum, instead it is essentially a
> summary of the patent US 4611307.

One of the main selling points of the Mathatron was its capability to handle parentheses in a mathematically correct
manner. The algorithm used for this is probably best explained by starting with an example without any parentheses. When
moving through the computation from left to right, the result can always be stored in the form `X + Y * current_number`,
where `+` may be replaced by `-` and `*` may be replaced by `/`.

|Entered formula |`12`|`*` |`2` |`+` |`18`|`/` |`3` |`-` |`7` |`*` |`4` |
|----------------|----|----|----|----|----|----|----|----|----|----|----|
|`X`             |    |    |    |`24`|`24`|`24`|`24`|`30`|`30`|`30`|`30`|
|`+` or `-`      |    |    |    |`+` |`+` |`+` |`+` |`-` |`-` |`-` |`-` |
|`Y`             |    |`12`|`12`|    |    |`18`|`18`|    |    |`7` |`7` |
|`*` or `/`      |    |`*` |`*` |    |    |`/` |`/` |    |    |`*` |`*` |
|`current_number`|`12`|    |`2` |    |`18`|    |`3` |    |`7` |    |`4` |

The final result can easily be evaluated from the last column by first combining `Y` and `current_number` according to
the multiplication-type operator (`*`) and then combining the result with `X` according to the addition-type operator
(`-`):
```
X - Y * current_number = 30 - 7 * 4 = 30 - 28 = 2
```

To handle parentheses, we can add a stack that stores the values of `X` and `Y` (and the operators) for the part of the
formula before the parenthesis. The value inside the parentheses can then be evaluated as above when the parenthesis is
closed. The resulting value is stored as the `current_number` and the `X` and `Y` values present before the opening
parenthesis are restored from the stack. The state of all registers is now as if the value of the parentheses had been
entered as a number manually.

In the Mathatron, `X` corresponds to `R2`, `Y` corresponds to `R1`, and `current_number` corresponds to buffer register
`B`. The multiplication-type operator is stored as the operation attached to `R1`, while the addition-type operation is
attached to `R2`. Shifting is performed by moving each register `Rn` to register `Rn+2`. This process is described in
more detail in figure 4 of the patent. Empty values in the example computation above are replaced by special "identity"
codes in the Mathatron, which does not affect a value it is combined with.

Since only `R1` to `R4` exist, it seems like the Mathatron can only handle one level of parentheses [^1]. The example
computation performed in columns 16 and 17 of the patent also suggest this, since it uses all 4 registers to handle a
single level of parentheses. However, this is contradicted by the first paragraph of column 10 of the patent, which
claims that one level of parentheses can be handled using just `R1` and `R2`, while two levels can be handled using `R1`
to `R4`. Until this can be tested on a working machine, I would give more weight to the example computation and assume
that only a single level of parentheses can be handled by the hardware. Obviously, the algorithm works for arbitrary
levels of parentheses, so supporting more levels would "only" mean adding registers. It is not clear whether the machine
supports the use of two levels if one of them is the "top level": The expression `(1 + 2 * (3 + 4)) / 5` contains two
levels of parentheses in the first part, but at no point are there more than two levels with non-identity values.

[^1]: I.e. `1 + 2 * (3 + 4 * 5)` can be computed, but `1 + 2 * (3 + 4 * (5 + 6 * 7))` cannot.
