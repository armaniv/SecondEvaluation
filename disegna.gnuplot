set yrange [0:0.3]
set xrange [50:210] 
set ylabel "Riduzione di perdita"
set xlabel "Num nodi"

plot    "test.dat" using 1:2 title 'Media' with linespoints pt 15 ps 2 lt rgb "#004C99", \
        "test.dat" using 1:3 title 'Min' with points ps 2 pointtype 11 lt rgb "#FF0000", \
	"test.dat" using 1:4 title 'Max' with points ps 2 pointtype 9 lt rgb "#00FF00"

pause -1 "Click to continue"
