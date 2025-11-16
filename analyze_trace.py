#!/usr/bin/env python3
"""
RISC-V Trace Analytics
Parse execution trace and generate visualizations
Author: Computer Architecture Assignment
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import re

def categorize_instruction(instr):
    """Categorize instruction into ALU/Load/Store/Branch"""
    instr = instr.strip().lower()
    
    # Extract instruction mnemonic (first word)
    mnemonic = instr.split()[0]
    
    # Load instructions
    if mnemonic in ['lw', 'lh', 'lb', 'lbu', 'lhu', 'ld', 'lwu']:
        return 'Load'
    
    # Store instructions
    if mnemonic in ['sw', 'sh', 'sb', 'sd']:
        return 'Store'
    
    # Branch/Jump instructions
    if mnemonic in ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu', 'blez', 'bgtz',
                     'j', 'jal', 'jalr', 'jr']:
        return 'Branch'
    
    # System calls
    if mnemonic in ['ecall', 'ebreak']:
        return 'System'
    
    # Everything else is ALU (arithmetic/logical/immediate operations)
    # This includes: add, addi, sub, and, or, xor, sll, srl, sra, 
    #                li (pseudo-instruction), la (pseudo-instruction), etc.
    return 'ALU'

def parse_trace(filename):
    """Parse the trace CSV file"""
    print(f"Reading trace file: {filename}")
    df = pd.read_csv(filename)
    print(f"Total instructions in trace: {len(df)}")
    return df

def generate_histogram(df, output_file='histogram.png'):
    """Generate histogram of instruction categories"""
    print("\nGenerating instruction category histogram...")
    
    # Categorize all instructions
    df['category'] = df['instr'].apply(categorize_instruction)
    
    # Count occurrences
    category_counts = df['category'].value_counts()
    print("\nInstruction category breakdown:")
    for cat, count in category_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {cat}: {count} ({percentage:.1f}%)")
    
    # Create histogram
    plt.figure(figsize=(10, 6))
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    bars = plt.bar(category_counts.index, category_counts.values, 
                   color=colors[:len(category_counts)])
    
    plt.xlabel('Instruction Category', fontsize=12, fontweight='bold')
    plt.ylabel('Count', fontsize=12, fontweight='bold')
    plt.title('RISC-V Instruction Category Distribution', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved histogram to: {output_file}")
    plt.close()

def generate_pc_plot(df, output_file='pc_plot.png'):
    """Generate line plot of PC vs step index"""
    print("\nGenerating PC vs step plot...")
    
    # Convert PC from hex string to integer
    df['pc_int'] = df['pc'].apply(lambda x: int(x, 16) if isinstance(x, str) else x)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df['step'], df['pc_int'], linewidth=1.5, color='#2c3e50', alpha=0.7)
    plt.scatter(df['step'], df['pc_int'], s=10, color='#e74c3c', alpha=0.5, zorder=5)
    
    plt.xlabel('Step Index (Instruction Number)', fontsize=12, fontweight='bold')
    plt.ylabel('Program Counter (PC)', fontsize=12, fontweight='bold')
    plt.title('Program Counter Trace - Control Flow Visualization', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, linestyle='--')
    
    # Format y-axis as hex
    ax = plt.gca()
    y_labels = ax.get_yticks()
    ax.set_yticklabels([f'0x{int(y):08x}' for y in y_labels])
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved PC plot to: {output_file}")
    plt.close()

def analyze_memory_accesses(df):
    """Analyze memory access patterns"""
    print("\nMemory Access Analysis:")
    
    # Count loads and stores
    loads = df[df['mem_access'].str.contains('load', na=False)]
    stores = df[df['mem_access'].str.contains('store', na=False)]
    
    print(f"  Total loads: {len(loads)}")
    print(f"  Total stores: {len(stores)}")
    print(f"  Total memory accesses: {len(loads) + len(stores)}")
    
    # Extract unique memory addresses
    if len(loads) > 0:
        load_addrs = loads['mem_access'].str.extract(r'load:(0x[0-9a-fA-F]+)')[0].unique()
        print(f"  Unique load addresses: {len(load_addrs)}")
    
    if len(stores) > 0:
        store_addrs = stores['mem_access'].str.extract(r'store:(0x[0-9a-fA-F]+)')[0].unique()
        print(f"  Unique store addresses: {len(store_addrs)}")

def detect_loops(df):
    """Detect loop patterns in PC trace"""
    print("\nLoop Detection:")
    
    # Find repeated PC values
    pc_counts = df['pc'].value_counts()
    loop_pcs = pc_counts[pc_counts > 1]
    
    if len(loop_pcs) > 0:
        print(f"  Instructions executed multiple times: {len(loop_pcs)}")
        print(f"  Most frequent PC: {loop_pcs.index[0]} (executed {loop_pcs.iloc[0]} times)")
        
        # Estimate loop iterations
        most_frequent_pc = loop_pcs.index[0]
        iterations = loop_pcs.iloc[0]
        print(f"  Estimated loop iterations: ~{iterations}")
    else:
        print("  No loops detected (all PCs executed once)")

def main():
    """Main analysis function"""
    print("=" * 60)
    print("RISC-V Trace Analytics")
    print("=" * 60)
    
    # Parse trace
    df = parse_trace('trace.csv')
    
    # Generate visualizations
    generate_histogram(df)
    generate_pc_plot(df)
    
    # Additional analyses
    analyze_memory_accesses(df)
    detect_loops(df)
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("Generated files: histogram.png, pc_plot.png")
    print("=" * 60)

if __name__ == '__main__':
    main()
