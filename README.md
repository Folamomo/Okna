# Generacja danych
## Przygotowanie modelu
Modele powinny być realistycznie wyskalowane. 
Okna powinny być połączone w 1 obiekt.
Dla każdego okna zaznaczamy 4 wierzchołki i dodajemy je do Vertex group.
Kamera powinna mieć wszytkie parametry ustawione jak domyślna kamera w Blenderze.
Do renderowania używamy presetu HDTV720p
W zakładce Scripting otwieramy nowy plik teksotwy i wklejamy do niego zawartość skrypt.py
Otwieramy konsolę aby widzieć postępy (Windows: Window>Toggle System Console, Linux: Uruchomić Blendera z poziomu terminala)

## Ustawienia parametrów skryptu
Ustawiamy ścieżkę zapisu danych wejściowych
```python
#Parameters
save_path = 'D:/Render/model7/side16/'
```
Wybieramy kamerę
```python
#camera object
camera = bpy.data.objects["Camera"]
```
Podajemy nazwy Vertex grup odpowiadających widocznym oknom, od góry od dołu, od lewej do prawej
Podajemy nazwę obiektu w którym wybrane grupy się znajduja
```python
selectedGroups = ["Okno5", "Okno6"]
#object containing selected groups
ob = bpy.data.objects["Window.002"]
```
Wybieramy cel kamery(najlepiej centrum budynku) i zakresy z których będziemy losować pozycję kamery
(xmin może być mniejszy niż xmax, działa i tak)
```python
#Target for camera
lookAt = Vector((0.0, 0.0, 1.0))
#Possible camera locations
xmin = 15.0
xmax = 30.0
ymin = -30.0
ymax = -15.0
zmin = 0.10
zmax = 3.0
```
Wybieramy liczbę lokacji do wylosowania (najlepiej najpierw przetestować z 1)
```python
#Number of locations to render
amount = 1
```

Niestety implementacja skryptów w Blenderze powoduje jego zawieszanie na czas działania skryptu.

## Gotowe dane
Gotowe dane i modele znajdują się w folderze https://drive.google.com/drive/folders/19oj42FEjVagk-jeRzYNcaa4z53RW0Ttw?usp=sharing

# Sieć neuronowa 
## Dane wejściowe sieci
Należy ustawić zmienną images_path tak żeby wskazywała na nadrzędny folder zawierający dane wejściowe. 
Drzewo katalogów powinno wyglądać następująco:
    > nazwa_katalogu_nadrzędnego
        > model1
            > side1
                > left1.png
                > right1.png
                > left2.png
                > right2.png
                > ...
                > out.json
            > side2
            > ...
        > model2
        > model3
        > ...
itd.

left{nr}.png right{nr}.png to zdjęcia kolejno z lewej i prawej kamery, a out.json to plik z danymi do tych zdjęć (nachylenie kamery oraz wektory od kamery do rogu okna)
Zmienna nonVector określa jaką liczbę ustawimy jako brak okna, w założeniu powinna to być bardzo niska liczba (bazowo jest to -1000).

Sieć jest domyślnie ustawiona na zdjęcia 1280:720
Zdjęcia są zamieniane na czarno białe, a dane z json jest konwertowany na tablicę 3 wymiarową w postaci [Zdjęcie][Wektor][x,y,z].

Po wczytaniu dane są mieszane i dzielone na zbiory uczący i treningowy.

## Struktura sieci
Kod służący do trenowania sieci nueronowej znajduję się w pliku KerasWindowsDetection.ipynb.
Jest to czterowarstwowa sieć konwolucyjna. 
Sieć uczy sie 50 epok, ale przerywa dalszą naukę jeśli przez 5 epok z rzeu nie nastąpi porawa wyniku.
Wynik uczenia jest zapisany w pliku "best_model.hdf5".

### Funkcja straty
W KerasWindowsDetection.ipynb jest funkcja o nazwie my_loss. 
Działa ona w ten sposób, że jeśli w danym miejscu powinna być wartość nonVector, a przewidziana przez model wartość jest mniejsza bądź równa połowie wartości nonVector to zwraca błąd równy zero dla pozostałych sytuacji funkcja zwraca kwadrat różnicy wartości przewidzianej i rzeczywistej, następnie wylicza średnią ze wszystkich błędów.
Oprócz customowej funkcji testowane były też "huber_loss", oraz "mse". W celu ich przetestowania można odkomentować odpowiednią linię "model.compile".
Bazowo jest ustawiona funkcja "mse".

# Skrypt standalone
Skrypt korzysta z wyszkolonej sieci która jest zapisana w pliku "best_model.hdf5".
Link do modelu: https://drive.google.com/file/d/16hNsGldNptIkKIyglmbXicstbAzCLIV6/view?usp=sharing

Można go uruchomić dla dowolnej pary zdjęć (lewa i prawa kamera), a jako wynik zwraca tablicę wektorów biegnących od kamery do rogów okna bundynku, oraz dwa parametry oznaczające nachylenie kamery.
Uruchomienie skryptu: "python WindowDetection.py ścieżka_do_lewego_zdjęcia ścieżka_do_prawego_zdjęcia"

# Dane do testowania
https://drive.google.com/drive/folders/1X71-J7XdtrwUdXhKsMGhcZJd6FqzZDB9?usp=sharing
