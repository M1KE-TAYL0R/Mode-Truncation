#!/usr/bin/env gnuplot

reset
# set terminal pngcairo size 700, 524  enhanced font 'Verdana,12'
set terminal postscript color enhanced eps round
set output 'asym_abs.eps'
set encoding iso_8859_1 
# set xlabel 'A_0' font ", 14"
# set ylabel 'E [eV]' font ", 14"
set key left bottom at 0.0 , 0.1 font ", 10"
set xr [-0.001:1]
eV = 1/1.726058296249575186
set yr [-0.0001:2 ]
set size 0.5, 0.5
E0 = 0.4303
set tics font ", 14"
# set ytics 0,0.01*eV ,0.05*eV

p    for [i = 2:13] "./pf-2/E-f22-n10-p20000_abs.txt" u 1:(column(i)*eV) every 8::0  w p lc "#596275" ps 1.6 pt 7  t "",\
   for [i = 2:13] "./PF/E-f60-n18-p20000_abs.txt" u 1:(column(i)*eV) w l lc "black" lw 12 t "",\
    for [i = 2:13]  "./Feist/E-f60-n18-p20000_abs.txt" u 1:(column(i)*eV) w l lc rgb "#ff6b6b" lw 5 t "", \
    for [i = 2:13] "./pA/E-f18-n15-p20000_abs_single.txt" u 1:(column(i)*eV) w l lc rgb "#48dbfb" lw 4 t "", \