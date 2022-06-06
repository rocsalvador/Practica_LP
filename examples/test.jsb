Main |:
    _tp <- 60
    _tm <- {3 4}

    d <- {{C D E} F G A B C5 E}
    <!> d
    <:> d {4 8 8 8 8 8 8}
    <:> d 16

    <:> {Ab A#}
    <!> "El la bemmoll te un valor de:" Ab A4#
    <!> "El la sostingut te un valor de:" A4# A#

    while i < 10 |:
        <:> _Rand C C5 8
        i <- i + 1
    :|
:|
