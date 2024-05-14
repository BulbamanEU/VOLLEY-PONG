# VOLLEY-PONG GAME

<p>Python kursinis darbas atliktas Ginto Kukliausko EDIf-23/1</p>
<p>Kursinio darbo metu geriau susipažinau su kodo rašymo taisyklėmis, mokiausi praktiškai naudoti objektyvinio programavimo paskaitose/laboratoriniuose išmoktą informaciją.</p>

# Įvadas

<p></p>

</p>Volley-Pong yra kompiuterinis žaidimas, parašytas Python programavimo kalba.<br> 
Žaidimo esmė permušti kamuoliuką nepaliečiant tinklo ir neleidžiant kamuoliui nukristi žaidėjo pusėje.</p>

<p>Norint naudotis aplikaciją reikia atsisiųsti .zip failą visos repository ir atidaryti .exe failą.
</p>

<p>Atsidarius programą pateiktos meniu komandos:
<ul>
  <li>Klavišas Q reiškia išejimą iš aplikacijos, žaidimo sustabdymą</li>
  <li>Klavišas SPACE reiškia žaidimo startą, pratęsimą</li>
  <li>Užsibaigus partijai klavišas R reiškia žaidimo restartavimą</li>
</ul></p>

<p>Pradėjus partiją žaidėjas kontroliuojamas A ir D klavišais.<br>
<ul>
  <li>A - judėjimas į kairę.</li>
  <li>D - judėjimas į dešinę.</li>
<li>Klavišas S kontroliuoja kamuolio atmušimo stiprumą.</li>
</ul>

# BODY and ANALYSIS

<p>Pirmiausia, kad egzistuotų ekrane objektai tokie kaip žaidėjas, tinklas, kamuolys naudojamos klasės.</p>
<p>Pradžioje sukurtos kelios tėvinės abstrakcinės klasės. </p>
![Abstract class examples](https://github.com/BulbamanEU/VOLLEY-PONG/assets/167674481/7b8ca361-07ca-406e-8aa6-8dc15039bdb7)
<p>Abstrakcinės klasės yra patogus ir aiškus būdas aprašyti interface'ą. Tai leidžia vaikinėms klasėms turėti vienodus funkcijų pavadinimus, bet ir reikalauja parašyti atitinkamus tų funkcijų veikimus.</p>
