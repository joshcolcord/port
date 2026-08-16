---
title: "On building fast systems"
date: "jun 02 2026"
description: "A deep dive into system performance, low-level optimization, and latency trade-offs in modern hardware."
github_link: "https://github.com/joshcolcord/fast-systems"
slug: "building-fast-systems"
---

Performance is rarely about doing things faster. More often, it is about avoiding doing them at all, or doing them in parallel, or organizing them to respect the underlying physics of the machine. When we build software today, the layers of abstraction hide the hardware in ways that encourage inefficient design.

In typical system development, memory layouts and cache access patterns dictate the actual execution speed far more than the number of instructions executed. A single cache miss that pulls data from main memory can stall the processor for hundreds of cycles, during which time nothing useful is achieved.



### Hardware-Conscious Data Structure Layout

To minimize latency, we must arrange data sequentially in memory to maximize cache locality. Consider a naive approach using pointer-heavy trees or lists; each pointer traversal is a potential cache miss. Instead, packing structures into arrays (e.g., using contiguous buffers) allows the hardware prefetcher to load adjacent data before the CPU even requests it.

By understanding how cache line alignment works, we can prevent false sharing in multi-threaded contexts, align critical structures to 64-byte boundaries, and design systems that scale elegantly across physical CPU cores.

### Reducing Tail Latency

Throughput is a global metric, but tail latency is what users experience. In high-performance systems, preventing the 99th percentile latency spike requires managing scheduling queues and system interrupts with great care.

During my scheduling experiments, I found that taking control of resource allocation at the application level is key to avoiding garbage collection pauses, heavy thread context-switching overheads, and lock contention. When you eliminate these overheads, the tail latency naturally aligns close to average latency.
