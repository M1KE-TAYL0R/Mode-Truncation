#!/usr/bin/env gnuplot

reset
# set terminal pngcairo size 700, 524  enhanced font 'Verdana,12'
set terminal postscript color enhanced eps round
set output 'sym_omega.eps'
set encoding iso_8859_1 
# set xlabel 'A_0' font ", 14"
# set ylabel 'E [eV]' font ", 14"
set key left bottom at 0.0 , 0.1 font ", 10"
# set xr [-0.001:0.4]
eV = 1/1.949497794077403867e-02
# set yr [-0.75:0.75 ]
set size 0.5, 0.5
E0 = 0.4303
set tics font ", 14"
# set ytics -0.6,0.3 ,0.6

# i = 3

# p  for [i = 2:4] "Coup-f22-n10-p20000_omega_wide.txt" u ($1*eV):(column(i)*eV)  w l lc "#1e90ff" lw 2 t ""
p   for [i = 2:9] "Add-f22-n10-p20000_omega_wide.txt" u ($1*eV/2):(column(i)*eV) w l lw 1 t "",\
#    for [i = 2:4] "DSE-f22-n10-p20000_omega_wide.txt" u ($1*eV):(column(i)*eV) w l lc rgb "#ff6b6b" lw 2 t ""