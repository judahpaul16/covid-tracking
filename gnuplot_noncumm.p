set term gif animate delay 30 enhanced font "arial,14" size 1280,720
set output "graph.gif"
set grid ls 100
set datafile separator ','
set xdata time
set xtics rotate
system("cp ny_curve.dat data.dat")
set title '2020 COVID-19 STAT CHANGES OVER TIME IN NEW YORK (NON-CUMULATIVE)'
unset ylabel
set timefmt '%m/%d/%y'
do for [ii=1:system('wc -l data.dat')] { 
	system('sleep 0.3')
	plot 'data.dat' every ::1::ii u 1:2 w p lw 3 lc 2 title 'NEW INFECTIONS AS OF DAY '.(ii+1), \
	'' every ::1::ii u 1:2 w l lw 6 lc 2 notitle smooth bezier, \
	'' every ::1::ii u 1:3 w p lw 3 lc 3 title 'NEW HOSPITALIZATIONS AS OF DAY '.(ii+1), \
	'' every ::1::ii u 1:3 w l lw 6 lc 3 notitle smooth bezier, \
	'' every ::1::ii u 1:4 w p lw 3 lc 7 title 'NEW DEATHS AS OF DAY '.(ii+1), \
	'' every ::1::ii u 1:4 w l lw 6 lc 7 notitle smooth bezier
	}