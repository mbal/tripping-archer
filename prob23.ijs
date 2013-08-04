divisors =: i.([ #~ 0 = |)]
sumDiv =: +/ @ divisors

NB. limit is 28123
abundant =: < sumDiv
numbers =: #~ (abundant"0)
tbl =: [: ~. @ , [: +/~numbers
solution =: +/ @ (-. tbl)

time =: 6!:2
display =: (1!:2) & 2
