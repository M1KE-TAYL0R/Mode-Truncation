#!/usr/bin/env gnuplot

reset
# set terminal pngcairo size 700, 524  enhanced font 'Verdana,12'
set terminal postscript color enhanced eps round
set output 'sym_perturb_1.eps'
set encoding iso_8859_1 
# set xlabel 'A_0' font ", 14"
# set ylabel 'E [eV]' font ", 14"
set key left bottom at 0.0 , 0.1 font ", 10"
set xr [-0.001:0.4]
eV = 1/1.949497794077403867e-02
set yr [-0.75:0.75 ]
set size 0.5, 0.4
E0 = 0.4303
set tics font ", 14"
set ytics -0.6,0.3 ,0.6

i = 2

p  "Coup-f22-n10-p20000_p.txt" u 1:(column(i)*eV)  w l lc "#48dbfb" lw 6 t "",\
   "Add-f22-n10-p20000_p.txt" u 1:(column(i)*eV) w l lc "black" lw 6 t "",\
   "DSE-f22-n10-p20000_p.txt" u 1:(column(i)*eV) w l lc rgb "#ff6b6b" lw 6 t ""