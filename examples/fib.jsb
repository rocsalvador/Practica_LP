Fib n |:
    ant_2 <- 0
    ant_1 <- 1
    while n > 1 |:
        aux <- ant_1
        ant_1 <- ant_1 + ant_2
        ant_2 <- aux
        n <- n - 1
        <:> ant_1 % 8 + A 8
    :|
    <!> ant_1
:|


Main |:
    <?> n
    Fib n
:|
