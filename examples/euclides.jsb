~~~ programa que llegeix dos enters i n'escriu el seu maxim comu divisor ~~~

Main |:
    <!> "Escriu dos nombres"
    <?> a
    <?> b
    Euclides a b
:|

Euclides a b |:
    while a /= b |:
        if a > b |:
            a <- a - b
            <:> a % 8 + A
        :| else |:
            b <- b - a
            <:> b % 8 + A
        :|
    :|
    <!> "El seu MCD es" a
:|
