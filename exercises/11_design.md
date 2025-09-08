# Design using co-pilot

We want to write a build system in C/C++.

Here is a one paragraph specification of the tool:

The tool should accept a buildfile called `Buildit` in which the user
specifies targets and sources. The tool will read the `Builtit` file and
will determins which targets need to be built and in what order.

The tool should have a rich command line interface for building specific
targets, cleaning and anything else which is pertinent.

The tool should be written in C/C++.

Build the tool (called it `Buildit`) in two different ways:
- Tell co-pilot to build it just using the paragraphs above.
- Tell co-pilot to build a high level specification for the tool,
    review the specification and modify it to your needs and then
    build the tool.

Compare the results.
