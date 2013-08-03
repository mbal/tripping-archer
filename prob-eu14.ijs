collatz =: mul ` halve @. even
even =: 0 = 2&|
halve =: %&2
mul =: [: >: 3&*

NB. cache to improve performance.
cache =: (2+1e6) $ 0

lenColl =: 3 : 0
    l =. 1
    o =. y
    while. -. (y = 1) do.
        y =. collatz y
        if. y < 1e6 do.
            NB. yeah, it seems that *. (and) is not short-circuiting
            NB. it also seems that this j-mode sucks.
            if. ((y { cache) > 0) do.
                l =. l + (y { cache)
                y =. 1
            else.
                l =. l + 1
            end.
        else.
            l=.l+1
        end.
    end.
    cache =: l o } cache
    l
)

helper =: 1+ (i. (>./))

NB. example call: solution 1e6
NB. takes about 50 seconds
solution =: [: helper lenColl"0 @ (1+ i.)