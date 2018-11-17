# Assignment 3: Question 24 Unit 4

## Intro
Timing circuits are a crucial component of VLSI chips. Here’s a simple model of such a timing circuit. Consider a complete balanced binary tree with 𝑛 leaves, where 𝑛 is a power of two. Each edge 𝑒 of the tree has an associated length 𝑙𝑒, which is a positive number. The distance from the root to a given leaf is the sum of the lengths of all the edges on the path from the root to the leaf.
The root generates a clock signal which is propagated along the edges to the leaves. We’ll assume that the time it takes for the signal to reach a given leaf is proportional to the distance from the root to the leaf. Now, if all leaves do not have the same distance from the root, then the signal will not reach the leaves at the same time, and this is a big problem. We want the leaves to be completely synchronized, and all to receive the signal at the same time. To make this happen, we will have to increase the lengths of certain edges, so that all root-to-leaf paths have the same length (we’re not able to shrink edge lengths). If we achieve this, then the tree (with its new edge lengths) will be said to have zero skew. Our goal is to achieve zero skew in a way that keeps the sum of all the edge lengths as small as possible. 

### Operation to be Performed
Give an algorithm that increases the lengths of certain edges so that the resulting tree has zero skew and the total edge length is as small as possible. 

### Example 
Consider the tree in Figure 4.20, in which letters name the nodes and numbers indicate the edge lengths. 

![alt text](figure420.png)

The unique optimal solution for this instance would be to take the three length-1 edges and increase each of their lengths to 2. The resulting tree has zero skew, and the total edge length is 12, the smallest possible.

## Running

### Required packages
Please install networkx
```
pip install networkx
``` 