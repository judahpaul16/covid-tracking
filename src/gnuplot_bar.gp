set terminal pngcairo size 1138,640
set output "".output_file
set datafile separator ','
set style data histogram
set style histogram cluster gap 1
set style fill solid border rgb "black"
set title 'STATE COMPARISON: TOTAL CASES AND DEATHS'
set key top left
set auto x
set yrange [0:*]
plot '../data/data.csv' using 2:xtic(1) lc 2 title 'Cases', \
        '' using 0:($2+.1):(sprintf("%d",$2)) with labels center offset -2.3,.5 notitle, \
        '' using 3:xtic(1) lc 7 title 'Deaths', \
        '' using 0:($3+.1):(sprintf("%d",$3)) with labels center offset 2.8,.5 notitle
exit