#!/usr/bin/env gnuplot

reset
# set terminal pngcairo size 700, 524  enhanced font 'Verdana,12'
set terminal postscript color enhanced eps round
set output 'sym_cont.eps'
set encoding iso_8859_1 
set xlabel 'A_0' font ", 14"
set ylabel 'E [eV]' font ", 14"
set key left bottom at 0.0 , 5 font ", 28"
# set xr [-0.001:0.4]
eV = 27.2114
# set yr [-0.0001:0.055* eV ]
# set size 0.5, 0.3
E0 = 0.4303
set tics font ", 14"
# set ytics 0,0.01*eV ,0.05*eV

p   "dws_added.txt" u ($1/2):(column(4)*eV) w l lc rgb "#feca57" lw 12 dt (1, 1) t "", \
    "dws_coup_con.txt" u 1:(column(4)*eV) w l lc rgb "#feca57" lw 10 dt (3,1) t "", \
    "dws_dse_con.txt" u 1:(column(4)*eV) w l lc "#feca57" lw  10 t "",\
    "dws_added.txt" u ($1/2):(column(3)*eV) w l lc rgb "#e84118" lw 12 dt (1, 1) t "", \
    "dws_coup_con.txt" u 1:(column(3)*eV) w l lc rgb "#e84118" lw 10 dt (3,1) t "", \
    "dws_dse_con.txt" u 1:(column(3)*eV) w l lc "#e84118" lw  10 t "",\
    "dws_added.txt" u ($1/2):(column(2)*eV) w l lc "black" lw 12 dt (1, 1) t "", \
    "dws_coup_con.txt" u 1:(column(2)*eV) w l lc "black" lw 10 dt (3,1) t "", \
    "dws_dse_con.txt" u 1:(column(2)*eV) w l lc "#black" lw 10 t "",\
    # "dws_added.txt" u 1:(column(5)*eV) w l lc rgb "#9b59b6" lw 6 t "", \
    # "dws_coup_con.txt" u 1:(column(5)*eV) w l lc rgb "#9b59b6" lw  6   t "", \
    # "dws_dse_con.txt" u 1:(column(5)*eV) w l lc "#9b59b6" lw  6 t ""