# RISC-V Assembly Program: Sum of 1 to N
# Author: Computer Architecture Assignment
# Description: Computes S = 1 + 2 + ... + N and tracks execution metrics
# Handles N=0 correctly (result 0)

.data
    # Input data
    N:              .word 10            # Input value (change this to test different values)
    
    # Output data
    sum:            .word 0             # Result: sum of 1 to N
    
    # Performance counters
    total_instr:    .word 0             # Total instructions executed
    total_loads:    .word 0             # Total load operations
    total_stores:   .word 0             # Total store operations
    total_branches: .word 0             # Total branches taken

.text
.globl main

main:
    # Load N from memory
    la      a0, N                       # Load address of N
    lw      s0, 0(a0)                   # s0 = N (save for later use)
    
    # Initialize sum and loop counter
    li      s1, 0                       # s1 = sum (accumulator)
    li      s2, 1                       # s2 = current number (i = 1)
    
    # Initialize performance counters
    li      s3, 0                       # s3 = instruction counter
    li      s4, 0                       # s4 = load counter
    li      s5, 0                       # s5 = store counter
    li      s6, 0                       # s6 = branch counter
    
    # Count initial instructions
    addi    s3, s3, 7                   # Count: la, lw, 4 li, this addi
    addi    s4, s4, 1                   # Count: 1 load (lw N)
    
    # Check if N <= 0 (edge case)
    blez    s0, end_loop                # if N <= 0, skip to end
    addi    s3, s3, 1                   # Count: blez
    addi    s6, s6, 1                   # If we reach here, branch NOT taken
    
loop:
    # Add current number to sum
    add     s1, s1, s2                  # sum = sum + i
    addi    s3, s3, 1                   # Count: add
    
    # Check if we've reached N
    bge     s2, s0, end_loop            # if i >= N, exit loop
    addi    s3, s3, 1                   # Count: bge
    
    # Increment current number
    addi    s2, s2, 1                   # i++
    addi    s3, s3, 1                   # Count: addi
    
    # Branch back to loop start
    j       loop                        # jump to loop
    addi    s6, s6, 1                   # Count branch taken (j always taken)

end_loop:
    # Adjust counters for final branch taken
    addi    s3, s3, 1                   # Count the j instruction
    addi    s6, s6, 1                   # Count final branch (bge or blez)
    
    # Store sum to memory
    la      a0, sum
    sw      s1, 0(a0)
    addi    s3, s3, 2                   # Count: la, sw
    addi    s5, s5, 1                   # Count store
    
    # Store total instructions
    la      a0, total_instr
    addi    s3, s3, 8                   # Count remaining: 4*(la+sw) = 8 more
    sw      s3, 0(a0)
    addi    s5, s5, 1                   # Count store
    
    # Store total loads
    la      a0, total_loads
    sw      s4, 0(a0)
    addi    s5, s5, 1                   # Count store
    
    # Store total stores
    la      a0, total_stores
    addi    s5, s5, 1                   # Count this store too
    sw      s5, 0(a0)
    
    # Store total branches
    la      a0, total_branches
    sw      s6, 0(a0)
    
    # Exit program
    li      a7, 10                      # Exit syscall
    ecall

# Algorithm Explanation:
# For N=10: sum = 1+2+3+4+5+6+7+8+9+10 = 55
# For N=0: sum = 0 (loop never executes)
#
# Register Usage:
#   s0 = N (input value)
#   s1 = sum (accumulator)
#   s2 = i (loop counter, 1 to N)
#   s3 = total instruction count
#   s4 = total load count
#   s5 = total store count
#   s6 = total branch taken count
