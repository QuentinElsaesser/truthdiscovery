# all_methods.py

Run and show the results on a specific graph for our methods (plurality rule and Borda rule with the two normalizations).

The path of the file with the graph can be written in the main of this file or in the command line.

python3 -m v4.main.all_methods.py examples/graphes/article.txt

with the graph at path : examples/graphes/article.txt 

# main_borda.py

Run and show the results on a specific graph for the Borda rule.

The normalization and the path of the file must be specified in the command line :

python3 -m v4.main.borda_method.py *normalization* ../examples/graphes/article.txt

if the *normalization* isn't specified, by default we use the normalization A. You can choose 2 normalizations : A or C.

with the graph at path : examples/graphes/article.txt 

# comparaison.py

Same as all_methods.py.

# main_plurality.py

Run and show the results on a specific graph for the plurality rule.

The normalization and the path of the file must be specified in the command line :

python3 plurality_method.py *normalization* ../examples/graphes/article.txt

if the *normalization* isn't specified, by default we use the normalization A. You can choose 2 normalizations : A or O.

../examples/graphes/article.txt is the path of the file with the graph

# Display

Reliability sources :
1 : 0.0 - [1] ; 2 : 0.5 - [2] 

Reliability facts :
1 : 0.5 - 0 - [1] ; 2 : 1.5 - 1 - [2]

- The source 1 has a reliability of 0.0 and the source 1 claims one fact ([1])
- The source 2 has a reliability of 0.5 and the source 2 claims two facts ([2])
- The fact 1 has a reliability of 0.5, the source that claim it will receice a score of 0 and the fact 1 is claimed by one source ([1])
- The fact 2 has a reliability of 1.5, the source that claim it will receice a score of 1 and the fact 2 is claimed by two sources ([2])

Possibility to change the display of the facts in graph/obj function str_trust_f()