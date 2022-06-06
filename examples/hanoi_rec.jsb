~~~ Notes de Hanoi ~~~

Main |:
    src <- {C4 D E F G}
    dst <- {}
    aux <- {}
    HanoiRec #src src dst aux
:|

HanoiRec n src dst aux |:
    if n > 0 |:
        HanoiRec (n - 1) src aux dst
        note <- src[#src]
        8< src[#src]
        dst << note
        <:> note 8
        HanoiRec (n - 1) aux dst src
    :|
:|
