#!/usr/bin/env gnuplot

reset
# set terminal pngcairo size 700, 524  enhanced font 'Verdana,12'
set terminal postscript color enhanced eps 
set output 'sm_rel.eps'
set encoding iso_8859_1 
set key horizontal center bottom at 0.0 , 1.65/27.2114 font ", 16"
set xr [-3.5:3.5]
# set xlabel 'A_0' font ", 14"
# set ylabel 'E [eV]' font ", 14"
# set key left bottom at 0.0 , 1.7 font ", 10
set xr [-2.5:2.5]
eV = 1 #27.2114
set yr [-0.1/27.2114:.065]
set size 1, 0.7
E0 = 0.4303
set tics font ", 14"
# set ytics 0,0.01*eV ,0.05*eV

p   for [i = 3:10] "./pA_2mode/extra-data/E-f18-n10-η0.15.txt" u 1:((column(i)-$2)*eV) every 6::0  w p lc "#596275" ps 2 pt 7  t "",\
    for [i = 3:10] "./pA_2mode/E-f18-n10-η0.15_single.txt" u 1:((column(i)-$2)*eV) w l lc "black" lw 12 t "",\
    for [i = 3:10] "./PF_Fiest_Trunc/E-f60-n18-η0.15.txt" u 1:((column(i)-$2)*eV) w l lc rgb "#48dbfb" lw 6 t "",\
    for [i = 3:10]  "./PF_Fiest_Trunc/E-f60-n18-η0.15_Feist.txt" u 1:((column(i)-$2)*eV) w l lc rgb "#ff6b6b" lw 7 t "", \

# p   for [i = 2:4] "./pA_2mode/extra-data/E-f18-n10-η0.15.txt" u 1:(column(i)*eV) w l lc "#c8d6e5" lw 14 t "",\
#     "./pA_2mode/extra-data/E-f18-n10-η0.15.txt" u 1:(column(5)*eV) w l lc "#c8d6e5" lw 14 t "  ",\
#     for [i = 2:4]  "./PF_Fiest_Trunc/E-f60-n18-η0.15_Feist.txt" u 1:(column(i)*eV) w l lc rgb "#e74c3c" lw 6  t "", \
#     "./PF_Fiest_Trunc/E-f60-n18-η0.15_Feist.txt" u 1:(column(5)*eV) w l lc rgb "#e74c3c" lw 6  t "    ", \
#     for [i = 2:4] "./pA_2mode/E-f18-n10-η0.15_single.txt" u 1:(column(i)*eV) every 8::4 w p lc "#ff9f43" ps 1.2 pt 7 t "",\
#     "./pA_2mode/E-f18-n10-η0.15_single.txt" u 1:(column(5)*eV) every 8::4 w p lc "#ff9f43" ps 1.2 pt 7 t "  ", \
#     for [i = 2:4] "./PF_Fiest_Trunc/E-f60-n18-η0.15.txt" every 8 u 1:(column(i)*eV) w p lc "#3498db" ps 1.2 pt 7 t "",\
#     "./PF_Fiest_Trunc/E-f60-n18-η0.15.txt" every 8 u 1:(column(5)*eV) w p lc "#3498db" ps 1.2 pt 7  t "   ", 

# reset
# # set terminal pngcairo size 700, 524  enhanced font 'Verdana,12'
# set terminal postscript color enhanced eps round
# set output 'sm.eps'
# set encoding iso_8859_1 
# set xlabel 'R' font ", 14"
# set ylabel 'E [eV]' font ", 14"
# set key left bottom at 0.0 , 5
# set xr [-3.5:3.5]
# eV = 27.2114
# set yr [-0.0001:1.9 ]
# # set size 0.5, 0.3
# E0 = 0.4303
# set tics font ", 14"
# # set ytics 0,0.01*eV ,0.05*eV

# p for [i=2:5]  "./PF_Fiest_Trunc/E-f60-n18-η0.15_Feist.txt" u 1:(column(i)*eV) w l lc rgb "#feca57" lw 6 t "", \
#     for [i=2:5]  "./PF_Fiest_Trunc/E-f60-n18-η0.15.txt" u 1:(column(i)*eV) w l lc rgb "#e84118" lw 10 dt (3,4) t "", \
#     for [i=2:5]  "./pA_2mode/extra-data/E-f18-n10-η0.15.txt" u 1:(column(i)*eV) w l lc "black" lw 12 dt (1, 2) t "",\