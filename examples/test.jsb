Foo |:
:|

Fib n |:
:|

Main |:
    a <- 10
    b <- 20
    c <- a - b
    d <- {A0 B4 A4 C8}
    e <- d[0]
    f <- #d
    g <- a /= b
    <!> a "->" b
    if a = b |: <!> a <!> b :| else |: a <- b :|

    while a > 0 |:
        ~~~ <!> a ~~~
        a <- a - 1
        Fib a
    :|
:|
