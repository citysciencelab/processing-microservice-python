extensions [nw gis]

globals [
  wohngebäude
  rothenburgsort
  strassen
  gewaesser
  gruenanlagen
  anzahl_anwohner

  network_mode
  anwohner_standorte
  verfügbare-handwerksleistungen
]

; Verschiedene Agententypen
breed [ anwohnerschaft anwohner ]
anwohnerschaft-own [ verfügbares-einkommen mietrechtliche-kenntnisse umzugsentscheidung? weggezogen? ]

breed [gebäudeeigentümerschaft gebäudeeigentümer]
gebäudeeigentümerschaft-own [typ investitionsbereitschaft mieteinnahmen ]

breed [bebauung gebäude]
bebauung-own [ anzahl_wohnungen grundflache brutto_grundflache wärmebedarf_unsaniert wärmebedarf_saniert saniert? aktueller_wärmebedarf anwohner_im_gebäude]

breed [gewerbetreiberschaft gewerbebetreiber]

breed [handwerkerschaft handwerker]

breed [beratungsleistungen beratungsleistung]


; Verschiedene Netzwerke
undirected-link-breed [wohnverhältnisse wohnverhältnis ]
wohnverhältnisse-own [gemietet? preisbindung? mietkosten]

undirected-link-breed [eigentumsverhältnisse eigentumsverhältnis]
eigentumsverhältnisse-own [modernisierungs-status verbleibende-zeit]

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;; Modell-Setup  ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


to setup
  ; Alles zurücksetzen
  clear-all


  ; Laden der Daten von Rothenburgsort
  set wohngebäude gis:load-dataset "data/wohngebeude_rothenburgsort_waerme.json"
  set rothenburgsort gis:load-dataset "data/rothenburgsort.json"
  set strassen gis:load-dataset "data/strassen_rbo.json"
  set gewaesser gis:load-dataset "data/gewaesser_rbo.json"
  set gruenanlagen gis:load-dataset "data/gruenanlagen_rbo.json"
  set anzahl_anwohner 8945


  ; Wohnhäuser erstellen
  foreach gis:feature-list-of wohngebäude [ this-vector-feature ->
    gis:create-turtles-inside-polygon this-vector-feature bebauung 1 [
      set shape "house"
      set size 0.5
      set hidden? true
      set saniert? random-float 1 < (Anteil-Modernisierte-Wohnungen-zu-Beginn / 100) ; Basierend auf dem Slider die Sanierung zuweisen
      set anwohner_im_gebäude floor brutto_grundflache / 32.6 ; Nach Stadtteilprofil 2022 gibt es 32.6 m2 Wohnfläche je Einwohner in Rothenburgsort

      ; Den Wärmebedarf anpassen
      ifelse saniert?
      [set aktueller_wärmebedarf wärmebedarf_saniert]
      [set aktueller_wärmebedarf wärmebedarf_unsaniert]

    ]
  ]

  ; Gebäudeeigentümer erstellen auf der Grundlage des Zensus 2011
  ; (https://www.statistik-nord.de/fileadmin/maps/zensus2011_hh/index.html)


  ; Gebäude den jeweiligen Eigentümern zuordnen
  ask bebauung [
    ; Zufällig die Eigentümerschaft zuteilen
    let zufall random-float 1
    hatch-gebäudeeigentümerschaft 1 [
      set typ (ifelse-value
        zufall <= 0.16  [ "privatwirtschaftliches Unternehmen" ] ; 16% der Wohnungen sind im Besitz von privatwirschaftlichen Unternehmen
        zufall <= 0.7  [ "öffentliches Unternehmen/Genossenschaft" ] ; 54% der Wohnungen sind im Besitz von öffentlichen Unternehmen oder Genossenschaften
        zufall <= 0.89  [ "Privatperson" ] ; 19% der Wohnungen sind im Besitz von Privatpersonen
        ["WEG" ]) ; 12% der Wohnungen sind im Besitz von WEGs

      set investitionsbereitschaft "niedrig"
      set hidden? true

      create-eigentumsverhältnis-with myself [
        ifelse [saniert?] of other-end [
          set modernisierungs-status "erledigt"
        ][
          set modernisierungs-status "nicht begonnen"
        ]
      ]

    ]
  ]


  ; Anwohner erstellen - Schritt für Schritt die Gebäude befüllen
  while [(count anwohnerschaft) < anzahl_anwohner] [
    ask n-of 1 bebauung [
      let aktuelle_anwohner_im_gebäude count my-wohnverhältnisse

      if anwohner_im_gebäude > aktuelle_anwohner_im_gebäude
      [
        hatch-anwohnerschaft 1 [
          set shape "person"
          set size 0.5
          set hidden? true
          set umzugsentscheidung? false
          set weggezogen? false

          ; Einkommen der Anwohner
          ; nach Stadtteilprofil 2022: 3780 Sozialversicherungspflichtig Beschäftigte

          ; Wohnverhältnis ausgestalten
          create-wohnverhältnis-with myself [

            ; In 6% der Fälle sind die Wohnungen von den Eigentümer:innen bewohnt
            let zufall_vermietet random-float 1

            ifelse zufall_vermietet < 0.06 [ set gemietet? false ][ set gemietet? true ]


            ; Falls vermietet, Miete festlegen auf Grundlage der Marktanalyse des Hamburger Wohnungsmarktes
            ; https://www.vnw.de/fileadmin/user_upload/2019-10-29_Studientext-CRES-Studie-HH-Mietwohnungsmarkt19-MW_V9.pdf

            if gemietet? [
              ; Laut Stadtteilprofil sind 20% der Wohnungen in Rothenburgsort Sozialwohnungen und damit preisgebunden
              let zufall_preisbindung random-float 1
              ifelse zufall_preisbindung < 0.2 [
                set preisbindung? false
                set mietkosten random-normal 7.08 0.735
              ][
                set preisbindung? true
                set mietkosten random-normal 5.99 0.59
              ]
            ]
          ]
        ]
      ]
    ]
  ]


  ; Karte anzeigen
  set network_mode false
  show-map
  update-visualization


  reset-ticks
end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;; Funktionen zur Visualisierung ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

to show-map
  ; Anzeigen der Geodaten auf der Karte
  ask patches [ set pcolor white]
  ask links [hide-link]
  gis:set-world-envelope (gis:envelope-union-of (gis:envelope-of wohngebäude)
    (gis:envelope-of wohngebäude))
  gis:set-drawing-color black
  gis:fill wohngebäude 1

  gis:set-drawing-color grey
  gis:fill strassen 1

  gis:set-drawing-color blue
  gis:fill gewaesser 1

  gis:set-drawing-color green
  gis:fill gruenanlagen 1


  ; Wechseln zwischen dem Netzwerkmodus und dem Kartenmodus
  set network_mode false

  ask patches with [pxcor < -10 and pycor < -10] [
    set pcolor grey - 3
  ]


end

to show-network
  ;ask patches [set pcolor black]
  ask eigentumsverhältnisse [show-link]
  ;layout-tutte gebäudeeigentümerschaft eigentumsverhältnisse 6
  set network_mode true

end

to gebäude-anzeigen
  ask bebauung [
    set hidden? false
  ]
end

to gebäude-ausblenden
  ask bebauung [
    set hidden? true
  ]
end

to anwohner-anzeigen
  ask anwohnerschaft [
    set hidden? false
  ]
end

to anwohner-ausblenden
  ask anwohnerschaft [
    set hidden? true
  ]
end

to eigentümer-anzeigen
  ask gebäudeeigentümerschaft [
    set hidden? false
  ]
end

to eigentümer-ausblenden
  ask gebäudeeigentümerschaft [
    set hidden? true
  ]
end

to clear-map
  ask patches [set pcolor black]
end


to update-visualization
  ask bebauung with [saniert? = false] [
    set color red
  ]

  ask bebauung with [saniert? = true] [
    set color green
  ]

end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;; Funktionen zur Simulation ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


to go
  if aktuelles-jahr > 2020 + Simulationszeit [stop]

  ; Prozess der Mieterhöhung simulieren
  mieterhöhung-prozess

  ; Prozess der Verdrängung simulieren
  verdrängung-prozess

  tick
end


to mieterhöhung-prozess ; Auf Basis des gemeinsam modellierten Prozesses

  ; Verfügbare Handwerksleistungen für diesen Monat zurücksetzen
  set verfügbare-handwerksleistungen Verfügbarkeit-Handwerks-und-Bauleistungen

  ; Gebäudeeigentümer:innen treffen Modernisierungsentscheidungen
  ask gebäudeeigentümerschaft [

    ; Überlegen, ob eine Modernisierungsentscheidung getroffen wird
    ask my-eigentumsverhältnisse with [modernisierungs-status = "nicht begonnen"] [
      if modernisierungsentscheidung-treffen [investitionsbereitschaft] of myself [
        set modernisierungs-status "in Finanzierung"
      ]
    ]


    ; Falls getroffen, nach Finanzierung suchen
    ask my-eigentumsverhältnisse with [modernisierungs-status = "in Finanzierung"] [
      if finanzierung-suchen [
        set modernisierungs-status "in Planung"
        set verbleibende-zeit Dauer-Planung-und-Genehmigung-der-Modernisierung
      ]
    ]


    ; Planung und Genehmigung abwarten
    ask my-eigentumsverhältnisse with [modernisierungs-status = "in Planung"] [
      ifelse verbleibende-zeit > 0 [
        set verbleibende-zeit (verbleibende-zeit - 1)
      ] [
        set modernisierungs-status "in Bau"

        ; Wegzug findet bei Modernisierungsankündigung statt
        ask [my-wohnverhältnisse] of other-end [

          let zufall-wegzug random-float 1
          if zufall-wegzug < (Umzugsentscheidung-bei-Modernisierungsankündigung / 100) [
            ask both-ends [

              if is-anwohner? self [
                set umzugsentscheidung? true

              ]
            ]
          ]
        ]
      ]
    ]

    ; Bau je nach Verfügbarkeit ausführen
    ask my-eigentumsverhältnisse with [modernisierungs-status = "in Bau"] [
      if verfügbare-handwerksleistungen > 0 [
        set verfügbare-handwerksleistungen (verfügbare-handwerksleistungen - 1)
        set modernisierungs-status "erledigt"

        ; Gebäude auf saniert umstellen
        ask other-end [
          set saniert? true
          set aktueller_wärmebedarf wärmebedarf_saniert
          set color green
        ]

        ; Modernisierungsmieterhöhung durchführen
        ; Gesamtkosten der Sanierung berechnen
        let umlage Durchschnittliche-Kosten-für-energetische-Modernisierung * (Maximale-Modernisierungsmieterhöhung / 100) / 12 / [brutto_grundflache] of other-end
        let anzahl_mieter:innen count ([my-wohnverhältnisse] of other-end) with [gemietet?]

        if anzahl_mieter:innen > 0 [
          let erhöhung_pro_mieter umlage / anzahl_mieter:innen
          if erhöhung_pro_mieter > 1 [show erhöhung_pro_mieter]


          ; Miete erhöhen
          ask [wohnverhältnisse] of other-end [
            if gemietet? and not preisbindung? [
              set mietkosten (mietkosten + erhöhung_pro_mieter)
            ]
          ]
        ]


      ]
    ]
  ]


end

to-report modernisierungsentscheidung-treffen [invest-bereitschaft]
  let wahrscheinlichkeit-modernisierung 0
  set wahrscheinlichkeit-modernisierung (ifelse-value
    invest-bereitschaft = "niedrig"  [ 0.01 ]
    invest-bereitschaft = "mittel"  [ 0.4 ]
    invest-bereitschaft = "hoch"  [ 0.75 ]
    [0 ]) ;

  ; Entscheidung wird zufällig getroffen
  ifelse random-float 1 < wahrscheinlichkeit-modernisierung [ report true  ] [ report false ]

end

to-report finanzierung-suchen
  let wahrscheinlichkeit-finanzierung 0
  set wahrscheinlichkeit-finanzierung (ifelse-value
    Verfügbare-Fördermittel = "niedrig"  [ 0.05 ]
    Verfügbare-Fördermittel = "mittel"  [ 0.25 ]
    Verfügbare-Fördermittel = "hoch"  [ 0.5 ]
    [0 ]) ;

  ; Entscheidung wird zufällig getroffen
  ifelse random-float 1 < wahrscheinlichkeit-finanzierung [ report true  ] [ report false ]

end

to verdrängung-prozess
  ask anwohnerschaft with [umzugsentscheidung?] [
     setxy [pxcor] of one-of patches with [pcolor = grey - 3] [pycor] of one-of patches with [pcolor = grey - 3]

  ]
end


to-report aktuelles-jahr
  let simulierte_zeit (ticks / 12)
  set simulierte_zeit floor simulierte_zeit

  report simulierte_zeit + 2020
end

to-report aktueller-monat
  report ticks mod 12 + 1

end
@#$#@#$#@
GRAPHICS-WINDOW
1016
10
1639
484
-1
-1
15.0
1
10
1
1
1
0
1
1
1
-20
20
-15
15
0
0
1
ticks
30.0

BUTTON
32
30
98
63
Setup
setup
NIL
1
T
OBSERVER
NIL
S
NIL
NIL
1

BUTTON
112
29
255
62
Simulation starten
go
T
1
T
OBSERVER
NIL
G
NIL
NIL
1

BUTTON
1017
494
1140
527
Karte anzeigen
show-map
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
1249
494
1396
527
Netzwerk anzeigen
show-network
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
1489
493
1639
526
Karte zurücksetzen
clear-map
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
348
45
406
90
Monat
aktueller-monat
17
1
11

SLIDER
31
136
476
169
Anteil-Modernisierte-Wohnungen-zu-Beginn
Anteil-Modernisierte-Wohnungen-zu-Beginn
0
100
31.0
1
1
%
HORIZONTAL

PLOT
684
313
1009
437
Anwohner
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "plot count (anwohnerschaft with [not weggezogen?])"

BUTTON
1018
553
1176
586
Wohngebäude anzeigen
gebäude-anzeigen
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
1018
590
1176
623
Wohngebäude ausblenden
gebäude-ausblenden
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
1187
554
1395
587
Anwohner:innen anzeigen
anwohner-anzeigen
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
1187
591
1395
624
Anwohner:innen ausblenden
anwohner-ausblenden
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
1405
551
1637
584
Gebäudeeigentümer anzeigen
eigentümer-anzeigen
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
1405
590
1636
623
Gebäudeeigentümer ausblenden
eigentümer-ausblenden
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

PLOT
814
180
1008
305
Mietkosten
€ / m2 und Monat
NIL
0.0
20.0
0.0
10.0
true
false
"" ""
PENS
"Mietkosten" 0.5 1 -16777216 true "" "histogram [mietkosten] of wohnverhältnisse"

CHOOSER
32
285
209
330
Verfügbare-Fördermittel
Verfügbare-Fördermittel
"keine" "niedrig" "mittel" "hoch"
3

SLIDER
32
181
475
214
Dauer-Planung-und-Genehmigung-der-Modernisierung
Dauer-Planung-und-Genehmigung-der-Modernisierung
1
36
17.0
1
1
Monate
HORIZONTAL

PLOT
684
10
1009
174
Status Gebäudemodernisierung
Monate
NIL
0.0
10.0
0.0
10.0
true
true
"" ""
PENS
"Nicht begonnen" 1.0 0 -2139308 true "" "plot count eigentumsverhältnisse with [modernisierungs-status = \"nicht begonnen\"]"
"In Finanzierung" 1.0 0 -7500403 true "" "plot count eigentumsverhältnisse with [modernisierungs-status = \"in Finanzierung\"]"
"In Planung" 1.0 0 -5207188 true "" "plot count eigentumsverhältnisse with [modernisierungs-status = \"in Planung\"]"
"In Bau" 1.0 0 -723837 true "" "plot count eigentumsverhältnisse with [modernisierungs-status = \"in Bau\"]"
"modernisiert" 1.0 0 -8330359 true "" "plot count eigentumsverhältnisse with [modernisierungs-status = \"erledigt\"]"

SLIDER
32
219
475
252
Verfügbarkeit-Handwerks-und-Bauleistungen
Verfügbarkeit-Handwerks-und-Bauleistungen
0
25
8.0
1
1
Gebäude pro Monat
HORIZONTAL

SLIDER
32
360
543
393
Umzugsentscheidung-bei-Modernisierungsankündigung
Umzugsentscheidung-bei-Modernisierungsankündigung
0
25
8.0
1
1
%
HORIZONTAL

SLIDER
31
403
542
436
Durchschnittliche-Kosten-für-energetische-Modernisierung
Durchschnittliche-Kosten-für-energetische-Modernisierung
5000
50000
9000.0
1000
1
€
HORIZONTAL

MONITOR
285
46
342
91
Jahr
aktuelles-jahr
17
1
11

SLIDER
31
447
543
480
Maximale-Modernisierungsmieterhöhung
Maximale-Modernisierungsmieterhöhung
0
100
8.0
1
1
% der Modernisierungskosten
HORIZONTAL

PLOT
580
179
810
305
Durchschnittliche Miete pro qm
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -16777216 true "" "plot mean [mietkosten] of wohnverhältnisse"

SLIDER
32
71
256
104
Simulationszeit
Simulationszeit
0
20
15.0
1
1
Jahre
HORIZONTAL

@#$#@#$#@
## WHAT IS IT?

(a general understanding of what the model is trying to show or explain)

## HOW IT WORKS

(what rules the agents use to create the overall behavior of the model)

## HOW TO USE IT

(how to use the model, including a description of each of the items in the Interface tab)

## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.3.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
