HI-BUG: Heterogeneous Implicit Bounded Universal (Comparative) Graph
=======================================================================

OVERVIEW
--------
HI-BUG is a conceptual framework for studying computation by combining two
familiar models:

  • A Cellular Automaton (CA) for local, massively parallel computation
  • A Turing-machine-like controller (TM) for global, sequential computation

The goal is not to propose a new machine that "beats" classical models, but
to provide a structured way to generate and analyze large (often exponential)
state graphs while keeping computational assumptions explicit and honest.

HI-BUG is intended as:

  • an analysis tool
  • a comparison framework
  • a playground for reasoning about complexity, scaling, and even
    quantum-like behavior from a computational perspective


-----------------------------------------------------------------------

READING NOTE
------------
HI-BUG uses several terms (e.g. bounded, universal, implicit) in a
framework-specific sense. Precise clarifications appear in the section
"HI-BUG Terminology (Clarifications)" below. Claims about scaling and
complexity should be read strictly in that context.


-----------------------------------------------------------------------

CORE COMPONENTS
---------------

1. The CA Band (Local, Parallel)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The CA lives on a finite periodic band (a ring) of size n.

Each cell:
  • has a finite local state
  • updates using the same rule everywhere
  • only reads a bounded local neighborhood
  • has no access to absolute position

The CA is:
  • massively parallel
  • uniform
  • independent of the total band size n

This band represents local mixing, propagation, and geometry. Importantly,
it admits a clean infinite-band limit (n → ∞).


-----------------------------------------------------------------------

2. The TM / Controller (Global, Sequential)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The TM:
  • can read the entire CA band
  • has its own persistent memory band of size m
  • performs global aggregation, counting, and decision-making

The TM:
  • operates sequentially
  • is allowed to depend on the total band size n
  • may run at a different frequency than the CA

This component represents global computation that cannot be achieved by
strictly local rules.


-----------------------------------------------------------------------

3. Update Semantics
~~~~~~~~~~~~~~~~~~
Computation proceeds in rounds.

CA updates and TM updates are both allowed, but:
  • they do not need to occur at the same rate
  • their relative frequency is part of the model design

This explicitly separates fast local dynamics from rare global coordination.


-----------------------------------------------------------------------

EXPLICIT RULES AND "CHEATING"
----------------------------
HI-BUG is designed to make assumptions explicit, not to forbid power.
Certain extensions are allowed, but must always be stated clearly:

  • CA cells may be given read access to the TM memory band
  • The TM may overwrite individual CA cells directly
  • The TM may broadcast global signals to the CA

These features are not illegal, but they fundamentally change the
computational power of the system. Any discussion of complexity or scaling
must state whether such features are enabled.


-----------------------------------------------------------------------

HI-BUG TERMINOLOGY (CLARIFICATIONS)
----------------------------------

Bounded
~~~~~~~
"Bounded" means that HI-BUG is defined, by default, for finite CA band size n
and finite controller memory m. Infinite limits (e.g. n → ∞) are used only as
an analytical lens to study scaling behavior, not as the operational
definition of the machine.

Universal
~~~~~~~~~
"Universal" does not mean Turing-universal in the classical sense. It means
that many different computational models (pure CA, CA with global
aggregation, TM-like machines, hybrid systems) can be represented and
compared within a single framework by examining their induced configuration
graphs.

Implicit
~~~~~~~~
HI-BUG compares machines via their induced state-transition graphs, not via
their descriptions. The configuration graph "forgets" how it was generated;
only reachability structure, transients, and attractors remain. Two different
machines that induce isomorphic graphs are equivalent for analysis purposes.

Heterogeneous
~~~~~~~~~~~~~
The model explicitly separates:
  • local vs global computation
  • parallel vs sequential updates
  • uniform CA dynamics vs non-uniform controller logic

This separation is intentional and central to the framework.

On Scaling and Diagonalization Intuition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
HI-BUG makes a structural distinction that is often implicit in complexity
discussions: local, uniform computation scales naturally with system size,
while global aggregation becomes increasingly expensive. Arguments that rely
on unrestricted global inspection or self-reference implicitly assume
oracle-like access in the large-n limit. HI-BUG does not forbid such access,
but requires it to be stated explicitly.


-----------------------------------------------------------------------

SCALING AND THE INFINITE LIMIT
-----------------------------
A key motivation for HI-BUG is that CA and TM behave very differently as band
size grows.

The CA:
  • scales naturally to infinite size
  • remains local and uniform
  • does not gain extra power from larger n

The TM:
  • becomes increasingly expensive as n grows
  • may require full-band passes
  • does not survive the infinite limit without effectively becoming some
    type of oracle

This asymmetry helps clarify:
  • why many classical proof techniques break down (e.g. diagonalization,
    oracle arguments)
  • why some NP problems scale geometrically while others do not
  • why "global reasoning" and "local dynamics" should not be conflated


-----------------------------------------------------------------------

CONFIGURATION GRAPH PERSPECTIVE
-------------------------------
Each HI-BUG machine induces a configuration graph:

  • Nodes: complete system states (CA ring band + TM memory band)
  • Edges: deterministic update steps

This graph is typically exponential in band size, by design.

HI-BUG treats:
  • language recognition
  • complexity
  • cryptographic hardness
  • dynamical behavior

as questions about reachability, transients, and basin structure in this
graph.


-----------------------------------------------------------------------

WHY THIS IS USEFUL
-----------------
HI-BUG provides a shared interface to:
  • compare different computational models without erasing structure
  • study NP problems and cryptographic constructions geometrically
  • reason about which assumptions introduce oracle-like power
  • explore the relationship between locality, global aggregation, and
    scaling


-----------------------------------------------------------------------

QUANTUM-INSPIRED MOTIVATION (OPTIONAL)
-------------------------------------
HI-BUG can also be used as a theory-crafting tool for quantum mechanics.

CA rules can model local conservation and flow (e.g. Schrödinger /
Madelung-like dynamics), while the TM represents rare global events, such as
measurement collapse, where global aggregation is unavoidable and local
rules alone are insufficient.

This interpretation is exploratory and not a claim about physical reality;
it is offered purely as a computational lens.


-----------------------------------------------------------------------

THIS REPOSITORY
---------------
The code here is a toy implementation of the HI-BUG framework.

  • CA rules are randomly generated lookup tables
  • The TM computes simple global properties (e.g. parity over the band)
  • Different rule selections induce different configuration graphs
  • Basic graph generation and analysis tools are included

The state space grows exponentially with band size — that is the point.

This repository is a starting point for:
  • experimenting with different machine families
  • visualizing configuration graphs
  • comparing computational structures


-----------------------------------------------------------------------

STATUS
------
Code and documentation are work in progress.
The framework is intentionally flexible.
Contributions, experiments, and reinterpretations are welcome.

If this model helps you reason more clearly about computation, complexity,
or physics-adjacent ideas, feel free to use it and share it.
