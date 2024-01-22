# This code is from Julia Cartwright julia@kernel.org

set terminal png medium size 800,600
# set terminal X11 persist
set output "cyclictestnoRT.png"
set datafile commentschars "#"

set logscale y

set xrang [0:500]

# trim some of the distortion from the bottom of the plot
set yrang [0.85:*]

set xlabel "t (us)"
set ylabel "Count"

plot "nort.hist" using 1:2 with histeps title "NON-RT w/ load",    \
     "nortload.hist" using 1:2 with histeps title "NON-RT w/o load"
