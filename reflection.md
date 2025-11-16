# Reflection: Stored-Program Concept and ISA Execution

## Understanding the Stored-Program Concept

The stored-program concept, pioneered by von Neumann, fundamentally changed computing by treating instructions and data as equivalent entities stored in the same memory. This assignment vividly demonstrates this principle through our RISC-V program where both the sum computation instructions (.text section) and the data values (.data section) reside in addressable memory locations.

When examining the execution trace, we observe the Program Counter (PC) systematically advancing through memory addresses—starting at 0x00400000 and progressing sequentially except when branches occur. This sequential fetch-decode-execute cycle is the essence of stored-program computing: the processor doesn't "know" its purpose beforehand; it simply retrieves and executes whatever instruction sits at the current PC address. The PC plot visualization clearly shows this, with horizontal progressions indicating sequential execution and vertical jumps revealing branch instructions redirecting control flow.

## The ISA as an Abstraction Layer

The RISC-V Instruction Set Architecture serves as a critical abstraction between software and hardware. Our program demonstrates how the ISA provides a standardized vocabulary of operations—arithmetic (add, addi), memory access (lw, sw), control flow (blez, bge, j), and system calls (ecall)—that programmers use without concerning themselves with transistor-level implementation.

The instruction histogram reveals the ISA's design philosophy. RISC-V's emphasis on simplicity is evident: 82% of executed instructions are ALU operations, reflecting the architecture's load-store design where computation happens in registers while memory is accessed only when necessary (1% loads, 5% stores). This separation improves performance since register operations are significantly faster than memory accesses.

## Performance Counter Insights

The performance counters embedded in our program illustrate how computer architects evaluate execution efficiency. For N=10, we executed approximately 108 instructions to compute a sum—this seems excessive for a simple task, but it reflects the overhead of instruction counting itself. In real systems, hardware performance counters track these metrics without program modification, enabling optimization without instrumentation overhead.

The branch counter (11 branches for N=10) reveals control flow costs. Each loop iteration requires a comparison, conditional branch, and unconditional jump, demonstrating why modern processors invest heavily in branch prediction hardware to minimize pipeline stalls.

## Practical Implications

This exercise demonstrates why ISA design matters profoundly. The RISC-V architecture's regularity—consistent instruction formats, uniform register access, and simple addressing modes—simplifies both compiler design and hardware implementation. Our trace shows no complex instructions requiring multiple cycles; each operation is atomic and predictable.

Moreover, the stored-program concept enables unprecedented flexibility. The same memory holding our sum program could contain a sorting algorithm or graphics renderer simply by changing the bit patterns stored there. This universality, combined with ISA abstraction, enables the software ecosystem we depend upon today.

**Word Count: 398 words**

---

## Key Takeaways

1. **Memory Unification**: Instructions and data coexist in memory, fetched identically
2. **ISA Abstraction**: Hardware complexity hidden behind standardized operations
3. **Sequential Execution**: PC advancement creates predictable, repeatable behavior
4. **Performance Measurement**: Counters quantify execution characteristics objectively
5. **Architectural Trade-offs**: RISC simplicity vs. CISC complexity reflected in instruction mix
