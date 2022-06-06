Main |:
    <!> "Introdueix la nota mes greu i la nota mes aguda de l escala"
    <?> noteMin
    <?> noteMax
    while noteMin <= noteMax |:
        ~~~ Es poden reproduir acords si es creen com a vectors dins de vectors ~~~
        d <- {{noteMin noteMin + 2 noteMin + 4}}
        <:> d 8
        <!> d[1]
        noteMin <- noteMin + 1
    :|
:|
