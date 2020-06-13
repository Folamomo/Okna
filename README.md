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
