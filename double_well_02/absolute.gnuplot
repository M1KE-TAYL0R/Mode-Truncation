#!/usr/bin/env gnuplot

reset
# set terminal pngcairo size 700, 524  enhanced font 'Verdana,12'
set terminal postscript color enhanced eps round
set output 'asym_abs.eps'
set encoding iso_8859_1 
# set xlabel 'A_0' font ", 14"
# set ylabel 'E [eV]' font ", 14"
set key right bottom at 0.85 , 9/27.2114 font ", 14"
# set xr [-0.001:0.4]
eV = 1/1.726058296249575186 #27.2114
set yr [-0.0001:2.75]
set size 0.5, 0.5
E0 = 0.4303
set tics font ", 14"
# set ytics 0,0.01*eV ,0.05*eV

p   for [i = 2:13] "./pf-2/E-f22-n10-p20000_abs.txt" u 1:(column(i)*eV) w l lc "#c8d6e5" lw 9 t "",\
    for [i = 2:13]  "./Feist/E-f60-n18-p20000_abs.txt" u 1:(column(i)*eV) every 5::0  w p lc rgb "#e74c3c" ps 1 pt 7 t "", \
    for [i = 2:13] "./PF/E-f60-n18-p20000_abs.txt" u 1:(column(i)*eV) every 10::5 w p lc rgb "#3498db" ps 1 pt 7 t "", \
    for [i = 2:13] "./pA/E-f18-n15-p20000_abs_single.txt" u 1:(column(i)*eV) every 10::0  w p lc "#ff9f43" ps 1 pt 7  t "",\
    # "./pf-2/E-f22-n10-p20000_abs.txt" u 1:(column(2)*eV) w l lc "#c8d6e5" lw 9 t "  ",\
    # "./Feist/E-f60-n18-p20000_abs.txt" u 1:(column(2)*eV) every 5::0  w p lc rgb "#e74c3c" ps 1 pt 7  t "     ", \
    # "./PF/E-f60-n18-p20000_abs.txt" u 1:(column(2)*eV) every 10::5 w p lc rgb "#3498db" ps 1 pt 7  t "   ", \
    # "./pA/E-f18-n15-p20000_abs_single.txt" u 1:(column(2)*eV) every 10::0  w p lc "#ff9f43" ps 1 pt 7  t "   "

# p for [i = 2:7]  "./Feist/E-f60-n18-p10000_abs.txt" u 1:(column(i)*eV) w l lc rgb "#feca57" lw 6 t "", \
#     for [i = 2:7] "./PF/E-f60-n18-p10000_abs.txt" u 1:(column(i)*eV) w l lc rgb "#e84118" lw 6 t "", \
#     for [i = 2:7] "./pf-2/E-f22-n10-p20000_abs.txt" u 1:(column(i)*eV) w l lc "black" lw 12 dt (1, 2) t "",\
#     "./Feist/E-f60-n18-p10000_abs.txt" u 1:(column(2)*eV) w l lc rgb "#feca57" lw 6 t "Untruncated DSE", \
#     "./PF/E-f60-n18-p10000_abs.txt" u 1:(column(2)*eV) w l lc rgb "#e84118" lw 6 t "Truncated DSE", \
#     "./pf-2/E-f22-n10-p20000_abs.txt" u 1:(column(2)*eV) w l lc "black" lw 12 dt (1, 2) t "Exact"

# reset
# # set terminal pngcairo size 700, 524  enhanced font 'Verdana,12'
# set terminal postscript color enhanced eps round
# set output 'asym_abs.eps'
# set encoding iso_8859_1 
# set xlabel 'A_0' font ", 14"
# set ylabel 'E [eV]' font ", 14"
# set key right bottom at 0.97 , 15 font ", 28"
# # set xr [-0.001:0.4]
# eV = 27.2114
# set yr [-0.0001:100]
# # set size 0.5, 0.3
# E0 = 0.4303
# set tics font ", 14"
# # set ytics 0,0.01*eV ,0.05*eV
# p for [i = 2:7]  "./Feist/E-f60-n18-p20000_abs.txt" u 1:(column(i)*eV) w l lc rgb "#feca57" lw 6 t "", \
#     for [i = 2:7] "./PF/E-f60-n18-p20000_abs.txt" u 1:(column(i)*eV) w l lc rgb "#e84118" lw 10 dt (3,4) t "", \
#     for [i = 2:7] "./pf-2/E-f22-n10-p20000_abs.txt" u 1:(column(i)*eV) w l lc "black" lw 12 dt (1, 2) t "",\
#     "./Feist/E-f60-n18-p20000_abs.txt" u 1:(column(2)*eV) w l lc rgb "#feca57" lw 6 t "   ", \
#     "./PF/E-f60-n18-p20000_abs.txt" u 1:(column(2)*eV) w l lc rgb "#e84118" lw 10 dt (3,4) t "  ", \
#     "./pf-2/E-f22-n10-p20000_abs.txt" u 1:(column(2)*eV) w l lc "black" lw 12 dt (1, 2) t "  "