# El doble intèrpret de JSBach

![JSBach](img/bach.png)

## Extensions
### Indicar el tipus de la nota

Aquesta extensió de JSBach permet modificar el tipus de nota que es reproduirà. Aquest tipus pot tenir diferents valors:

- 1 -> rodona
- 2 -> blanca
- 4 -> negra (valor per defecte)
- 8 -> corxera
- 16 -> semi-corxera

A més es pot indicar de diferents maneres dins de la funció de reproducció:

- No indicant res, es tocaran negres
- Indicant un sol valor després de les notes
- (Només al reproduir vectors) Indicant un vector de valors en el que cada posició correspont al tipus de la nota en la mateixa posició

```jsbach
Main |:
    <:> {C D E F G A B}
    <:> {C D E F G A B } 8
    <:> {C D E F G A B} {8 8 4 16 16 16 16}
    <:> A
    <:> A 2
:|
```

### Configurar el tempo i el compàs

Aquesta extensió de JSBach permet modificar el tempo i el compàs mitjançant dues variables especials: ```_tm``` (compas) i ```tp```(tempo). ```_tm``` s'ha d'assignar amb un vector de dues dimensions on el primer element indica la durada del compàs i el segon element el tipus de nota a la que fa referència la durada del compàs, és a dir, que si ```_tm  <- {2 4}``` es reproduiran 2 negres (4) per compàs.

```jsbach
Main |:
    _tm <- {3 4}    ~~~ El compas passa a ser 3/4 ~~~
    _tp <- 120      ~~~ Es toquen 120 negres per minut ~~~
    <:> {C D E F G A B} 
:|
```

### Tocar acords

Aquesta extensió de JSBach permet tocar múltiples notes a la vegada, per fer-ho simplement s'ha d'inidcar els acords creant un vector de vectors, tots els elements que es col·loquin dins el vector interior es reproduiran al mateix moment.

```jsbach
Main |:
    <:> {{A A + 2 A + 4} {B B + 2 B + 4} C}
    d <- {{A A + 2 A + 4} {B B + 2 B + 4} C}
    <:> d
:|
```

### Generar nombres aleatòris (No és molt útil però per generar partitures horribles va perfecte)

Aquesta extensió de JSBach permet generar nombres aleatòris mitjançant una funció anomenada ```_Rand``` que té com entrada el rang en el que s'ha de generar el valor i que retorna un enter.

```jsbach
Main |:
    while i < 10 |:
        nota <- _Rand C C5
        tipus <- _Rand 1 2
        <!> nota
        <:> nota tipus * 4
        i <- i + 1
    :|
:|
```
