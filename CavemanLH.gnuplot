set yrange [0:0.6]
set xrange [60:250] 
set ylabel "Riduzione di perdita messaggi H"
set xlabel "Num nodi"

plot    "caveman.dat" using 1:2 title 'Pop' with linespoints ps 2, \
        "caveman.dat" using 1:4 title 'Cut-point'  with linespoints ps 2, \
	      "caveman.dat" using 1:6 title 'Interfacce'  with linespoints ps 2, \
        "caveman.dat" using 1:8 title 'Interfacce + Cut-point'  with linespoints ps 2 \

pause -1 "Click to continue"