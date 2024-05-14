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

### Abstraction

<p>Pirmiausia, kad egzistuotų ekrane objektai tokie kaip žaidėjas, tinklas, kamuolys naudojamos klasės.<br>
Jos sukuriamos tam, kad supaprastintų objektų funkcijas, veikimą, kintamųjų išsaugojimą.</p>

```python
class Player(width_and_height, GameObject):
    def __init__(self, width, height, color=(255, 255, 255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        super().__init__(width, height)
        self._color = color
        self.x = x
        self.y = y
        self.create_shape()

    def create_shape(self):
        self.rect = pygame.Rect(self.x, self.y, self._width, self._height)

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self.rect)
```

### Encapsulation

<p>Programoje inkapsuliavimas naudojama tokiems kuriamų objektų dydžiams kaip plotis, aukštis, spalva, tam kad būtų sunkiau juos pakeisti ar pasiekti kode.<br>
Aukščio ar pločio gavimui naudojama atskira funkcija, kuri grąžina reikiamą reikšmę.</p>

### Inheritance

<p>Inheritance arba kitaip paveldėjimas padeda sumažinti kodo kartojimąsi. Kai kuriami panašūs objektai, sukuriama tėvinė klasė ir jos funkcijas paveldėja vaikinės klasės.</p>
<p>Pavyzdžiui yra sukurta tėvinė klasė, kuri turi reikalingų dydžių sukūrimą ir funkcijų aprašymą. Tėvinė klasė iškart aprašo aukštį ir plotį, kuris bus panaudotams skirtingiems objektams ir žaidėjo klasėje, ir tinklo klasėje.</p>

```python
class width_and_height():

    def __init__(self, width, height):
        self._width = width
        self._height = height

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width


class Rectangle(width_and_height, GameObject):
    def __init__(self, width, height, color=(255, 255, 255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        super().__init__(width, height)
        self._color = color
        self.x = x
        self.y = y
        self.create_shape()

    def create_shape(self):
        self.rect = pygame.Rect(self.x, self.y, self._width, self._height)

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self.rect)
```

<p>Šis pavyzdys tinka ir inkapsuliacijai pavaizduoti.</p>

<p>Abstrakcinės klasės yra patogus ir aiškus būdas aprašyti interface'ą. Tai leidžia vaikinėms klasėms turėti vienodus funkcijų pavadinimus, bet ir reikalauja parašyti atitinkamus tų funkcijų veikimus.</p>

### Polymorphism

<p>Šis objektyvinio programavimo principas naudojamas, kai skirtingos klasės turi vienodus funkcijų pavadinimus, bet skirtingus jų veikimus, dėl to yra įmanomas klasių funkcijų iškvietimas nepaisant, kuri klasė būtų.</p>
<p>Tai tikrai patogu žaidimo kūrimui, kai reikia piešti įvairius objektus, tokius kaip apskritimus, stačiakampius ar žaidėjus, ir visi jie turi vienodą funkciją, bet vykdo skirtingus veiksmus, priklausomai nuo to, kokia yra klasė.</p>

```python
    def draw(self, screen):
        pygame.draw.rect(screen, self._color, self.rect)
```
<p>Taip atrodo stačiakampio piešimas ekrane.</p>

```python
        def draw(self, screen):
        pygame.draw.circle(screen, self._color, self.center, self._radius)
```
<p>Taip atrodo apskritimo piešimas ekrane.</p>

```python
        for object in drawing_objects:
            object.draw(screen)
```
<p>Kai visi objektai yra viename masyve, juos galime visus iškviesti šiuo for ciklu.</p>


# Design Patterns

### Factory method

<p>Factory metodas patogus, kai reikia kurti daug tokių pačių principų objektų. Pavyzdžiui šiame žaidime tinklo, aplinkos objektų, kamuolio kūrimas pasitelkiamas Factory metodu, kad galima būtų nesunkiai padidinti šių daiktų skaičių.</p>

```python
class CircleFactory(ObjectFactory):
    def __init__(self, radius, center, color=(255, 255, 255), x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2):
        self._radius = radius
        self._color = color
        self._x = x
        self._y = y
        self.center = center

    def create_object(self):
        return Circle(self._radius, self.center, self._color, self._x, self._y)

visual_factory = CircleFactory(radius, center, (255, 255, 255), SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
```

<p>Aprašoma CircleFactory ir tada objekto sukūrimo metu belieka prilyginti visual_factory </p>

```python
visual = visual_factory.create_object()
```

### Builder

<p>Svarbesniems arba sudetingesnėms klasėms vertinga naudoti Builder, kuris supaprastina, aiškiau aprašo kintamuosius, jų tvarkymą, objekto veikimą.</p>
<p>Šioje programoje toks design pattern naudojamas Žaidėjo tvarkymui.</p>

```python
class PlayerBuilder():
    def __init__(self):
        self._width = 125
        self._height = 25
        self._color = (0, 255, 255)
        self._x = SCREEN_WIDTH / 2
        self._y = SCREEN_HEIGHT - 65 - self._height

    def set_width(self, width):
        self._width = width
        return self

    def set_height(self, height):
        self._height = height
        return self

    def set_color(self, color):
        self._color = color
        return self

    def set_position(self, x, y):
        self._x = x
        self._y = y
        return self

    def build(self):
        return Player(self._width, self._height, self._color, self._x, self._y)

player_builder = PlayerBuilder()
player_builder.set_color((255, 0, 0))
player_builder.set_position(100, 100)
```

### Abstraction class

<p>Sukuriama abstrakti tėvinė klasė skirta sukurti vaikinių klasių interface'ui. Patogu po to naudoti Polymorphism'ą.</p>
<p>Šiame kode aprašytas objektų piešimas, sūkurimas, kuris naudojamas keliose vaikinėse klasėse.</p>

```python
class GameObject(ABC):
    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def create_shape(self):
        pass

class ObjectFactory(ABC):
    @abstractmethod
    def create_object(self):
        pass
```

### Failo skaitymas

<p>Volley-Pong saugo informaciją .json failuose, tokią kaip kamuoliuko, žaidėjo koordinatės, kamuoliuko trajektorijos skaičiavimus ir pan. Dėl to, iš žaidimo galima išeiti, jį sustabdyti ir panorus, vėl sugrįžti į tokią pačią stadiją, kokioje buvo paliktas žaidimas.</p>

### Testing

<p>Svarbiausios formulės, kurios naudojamos žaidime testuojamos: kamuoliuko pabaigos koordinatės apskaičiavimas, kamuoliuko atsimušimo stiprumas, kamuoliuko atsimušimas nuo sienų.</p>

```python
class TestGame(unittest.TestCase):

    def test_choose_strength_short_hold(self):
        time = 0.3
        expected_strength = 0
        actual_strength = choose_strength(time)
        self.assertEqual(expected_strength, actual_strength)

    def test_choose_strength_long_hold(self):
        time = 5
        expected_strength = 3
        actual_strength = choose_strength(time)
        self.assertEqual(expected_strength, actual_strength)

    def test_ending_x(self):...

    def test_right_wall(self):...

    def test_left_wall(self):...
```

# Rezultatai

<ul>
  <li>Parašytas veikiantis žaidimo prototipas, kurį galima toliau tobulinti ir gauti galutinį produktą.</li>
  <li>Kodu stengtasi atitikti PEP8 stilių ir reikalavimus, kad kodas būtų lengviau skaitomas ir suprantamas kitiems koduotojams.</li>
  <li>Pasiektas žaidėjo, tinklo, kompiuterio ir kamuoliuko fizinis veikimas ir tarpusavio sąsaja.</li>
  <li>Įgyvendintas būsenos išsaugojimas, rašymas į failą.</li>
  <li>Įgyvendintas testavimas.</li>
</ul>

# Išvados

<p>Atliekant kursinį darbą susipažinau su PEP8 kodavimo reikalavimais ir stengiausi jų laikytis. Susidūriau su iššūkiais: kaip tvarkyti kodą , kai prisikaupia funkcijų, kintamųjų, kaip gražinti ir aiškiai rašyti kodą, kelti į skirtingus failus. Be to padalinus kodą į skirtingus failus tapo daug lengviau identifikuoti klaidas ,bei jas pašalinti.</p>

<p>Susipažinau ir savo kode naudojau pygame module, kuris pagrinde naudojamas 2D žaidimų kūrimui ir atveria grafikų nustatymus, klaviatūros, pelės įėjimo skaitymą, įvykių tvarkymą, garso kontroliavimą ir panašias atributikas naudojamas žaidimuose. </p>

<p>Dirbant su didesniu projektu negu įprastai teko naudoti Design Patterns ir OPP pillars, apie kuriuos mokiausi paskaitose, o praktiškai naudojau labaratoriniuose užsiėmimuose. Pradėjau vertinti šiuos metodus programavime ir pamačiau, kad jie ženkliai paspartina darbą.</p>

<p>Sunku buvo skaičiuoti kamuoliuko keliavimą ir tinkamai išsaugoti reikšmes, visas būsenas, kad žaidimą vėl įjungus būtų pratęsta. Išmokau naudoti unittest module, supratau kokie naudingi yra testai kode, kaip galima jais naudotis ir surasti klaidos vietą.</p>

<p>Toliau galima užbaigti žaidimo prototipą iki galutinio produkto, suteikti visiems objektams gražesnius paveikslėlius, įtraukti priešo lygio pasirinkimą, sudaryti įvairesnius atmušimo stiprumus, toliau gerinti mechanikas. Galima sukurti kelis skirtingas aikšteles, tarkim su aukštesniu ar žemesniu stogu, be stogo, aukštesniu tinklu ir pan. Prototipas ir pats žaidimas veikia labai paprastu principu, bet yra daug galimybių įtraukti daugiau funkcijų ir suteikti daugiau galimybių, veiksmų veikėjui atslikti.</p>
