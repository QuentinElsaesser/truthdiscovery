# read_file.py

Read a file and return two lists (in the form of an adjacency matrix).

# file format

The format of a file that represent a graph is simple.

If a line start with a '#', we ignore this line.

The first line in the graph without a '#' is :

- *number of sources* *number of objects* *number of facts*

We represent all the facts with an integer (from 1 to *number of facts*).

Then, in the file, we have the links between the sources and the facts :

- The first line will be the facts claimed by the source 1, the second line for the source 2, etc.

The character '-' is the separator between the sources and the objects.

Now we have the facts linked to the objects in the same way as the sources. The first line for the object 1, etc.

Example :

```
#nbsrc nbobj nbfct
5 2 4
#links between sources and facts
#source 1
2,4
#source 2
4
#source 3
1
-
#links between objects and facts
#object 1
1,2
3,4
```