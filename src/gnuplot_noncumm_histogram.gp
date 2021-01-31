set term gif animate delay 30 enhanced font "roboto,14" size 1280,720
set output "".output_file
set grid ls 25
set datafile separator ','
set xdata time
set timefmt '%Y-%m-%d'
set xtics rotate
set title 'NON-CUMMULATIVE COVID-19 STATS FOR '.state
unset ylabel
set style histogram errorbars linewidth 1
set style fill solid 0.3
set bars front
do for [ii=1:num_lines] {
        plot '../data/data.csv' every ::1::ii u 1:2 with boxes lc 2 title word(cases,ii+1).' NEW CASES ON DAY '.(ii+1), \
        '' every ::1::ii u 1:3 with boxes lc 7 title word(deaths,ii+1).' NEW DEATHS ON DAY '.(ii+1), \
};
exit