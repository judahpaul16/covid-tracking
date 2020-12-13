set term gif animate delay 30 enhanced font "roboto,14" size 1280,720
set output "graph_cumm.gif"
set grid ls 25
set datafile separator ','
set xdata time
set timefmt '%Y-%m-%d'
set xtics rotate
set title 'CUMMULATIVE COVID-19 STATS FOR '.state
set xlabel 'DATE'
set ylabel 'INFECTIONS/DEATHS'
do for [ii=1:num_lines] {
        plot 'data.csv' every ::1::ii u 1:2 w p lw 2 lc 2 title 'INFECTIONS AS OF DAY '.(ii+1), \
        '' every ::1::ii u 1:2 w l lw 5 lc 2 notitle smooth bezier, \
        '' every ::1::ii u 1:3 w p lw 2 lc 7 title 'DEATHS AS OF DAY '.(ii+1), \
        '' every ::1::ii u 1:3 w l lw 5 lc 7 notitle smooth bezier
};
exit