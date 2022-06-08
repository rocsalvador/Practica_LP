# El doble intèrpret de JSBach

![img](img/bach.png)

JSBach és un llenguatge de programació orientat a la composició algorísmica. Amb JSBach s'utilitzen construccions imperatives per generar composicions que donen lloc a partitures que poden ser desades en diferents formats digitals.

![Més informació](https://github.com/jordi-petit/lp-jsbach-2022)

## Dependències

Per tal de que el programa s'executi i generi tots els arxius de sortida es necessiten els següents programes:

- ```antlr4-python3-runtime```
- ```antlr4```
- ```lilypond```
- ```timidity```
- ```ffmpeg```

Per instal·lar ```antlr4-python3-runtime```:

```bash
pip3 install antlr4-python3-runtime
```

Per instal·lar la resta (a Ubuntu o derivats):

```bash
sudo apt install antlr4 lilypond timidity ffmpeg
```

## Execució

```bash
antlr4 -Dlanguage=Python3 -no-listener -visitor jsbach.g4

python3 src/jsbach.py source_file.jsb [initial_procedure]
```

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

### Sostinguts i bemolls

Aquesta extensió de JSBach permet tocar notes amb el to modificat, ja sigui amb un sostingut o un bemoll. Per indicar el to d'una nota es pot fer de diferents maneres:

```jsbach
Main |:
    ~~~ Indicant amb una b (bemoll) o un # (sostingut) darrere la nota ~~~
    <:> A4b A#
    ~~~ Sumant 0.25 (bemoll) o 0.75 (sostingut) a la nota base ~~~
    <:> A + 0.25 A + 0.75
:|
```

### Generar nombres aleatòris (Perfecte per composar)

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
