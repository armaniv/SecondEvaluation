set yrange [0:0.25]
set xrange [60:250] 
set ylabel "Riduzione di perdita messaggi LSA"
set xlabel "Num nodi"

plot    "waxman.dat" using 1:3 title 'Pop' with linespoints ps 2, \
        "waxman.dat" using 1:5 title 'Cut-point'  with linespoints ps 2, \
	      "waxman.dat" using 1:7 title 'Interfacce'  with linespoints ps 2, \
        "waxman.dat" using 1:9 title 'Interfacce + Cut-point'  with linespoints ps 2 \

pause -1 "Click to continue"