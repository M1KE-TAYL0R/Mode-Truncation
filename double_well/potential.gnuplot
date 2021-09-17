#!/usr/bin/env gnuplot

reset
# set terminal pngcairo size 700, 524  enhanced font 'Verdana,12'
set terminal postscript color enhanced eps round
set output 'sym_pot.eps'
set encoding iso_8859_1 
# set xlabel 'A_0' font ", 14"
# set ylabel 'V [eV]' font ", 14"
set key left bottom at 0.0 , 0.1
set xr [-3.2:3.2]
eV = 1
set yr [-0.0001:6 ]
set size 0.5, 0.3
E0 = 0.4303
set tics font ", 14"
set ytics 0, 2, 6

f(x) = -2.27/2.0 * x**2 + 0.125 * x**4 +2.576

p f(x) w l lc "black" lw 10 t ""