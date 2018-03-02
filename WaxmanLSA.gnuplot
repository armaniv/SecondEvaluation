set yrange [0:0.25]
set xrange [50:260] 
set ylabel "Riduzione di perdita messaggi LSA"
set xlabel "Num nodi"
set title "Grafi Waxman L_LSA"

plot    "waxman.dat" using 1:3:11  w yerrorbars lt rgb "#FF0000" notitle,  "" using 1:3 w lines lt rgb "#FF0000" title "Pop",  \
        "waxman.dat" using 1:5:13  w yerrorbars lt rgb "#00CC00" notitle,  "" using 1:5 w lines lt rgb "#00CC00" title "Cut-point",  \
	      "waxman.dat" using 1:7:15  w yerrorbars lt rgb "#FFC000" notitle,  "" using 1:7 w lines lt rgb "#FFC000" title "Interfacce",  \
        "waxman.dat" using 1:9:17  w yerrorbars lt rgb "#606060" notitle,  "" using 1:9 w lines lt rgb "#606060" title "Interfacce + Cut"

pause -1 "Click to continue"