set yrange [0:0.5]
set xrange [50:260] 
set ylabel "Riduzione di perdita messaggi H"
set xlabel "Num nodi"
set title "Grafi Caveman L_H"

plot    "caveman.dat" using 1:2:10  w yerrorbars lt rgb "#FF0000" notitle,  "" using 1:2 w lines lt rgb "#FF0000" title "Pop",  \
        "caveman.dat" using 1:4:12  w yerrorbars lt rgb "#00CC00" notitle,  "" using 1:4 w lines lt rgb "#00CC00" title "Cut-point",  \
	      "caveman.dat" using 1:6:14  w yerrorbars lt rgb "#FFC000" notitle,  "" using 1:6 w lines lt rgb "#FFC000" title "Interfacce",  \
        "caveman.dat" using 1:8:16  w yerrorbars lt rgb "#606060" notitle,  "" using 1:8 w lines lt rgb "#606060" title "Interfacce + Cut"

pause -1 "Click to continue"