Program pro snadnou tvorbu výřezů kloubů z RTG snímků
========================================
**Program projde jednotlivé snímky ve složce, uživatel klikáním myší
vytváří ze snímku čtvercové výřezy (v předem daném pořadí). Je to
nejrychlejší možný způsob vytváření výřezů. Program je plně podřízen
jedinému účelu – vytvořit z RTG snímků celých rukou nový dataset snímků
jednotlivých kloubů.**

# Vstupy a výstupy
## Vstupy
-  Obrázek, resp. složka s obrázky

## Výstupy
Pro každý jeden snímek:
-   Výřezy kloubů (jeden výřez za každé kliknutí myší) – ukládají se do
    výstupní složky
-   Soubor obsahující souřadnice označených kloubů pro případné další
    zpracování nebo úpravy – ukládá se do vstupní složky k původnímu
    snímku
    
# Ovládání programu
1. Do kódu je potřeba zadat adresu složky se vstupními snímky a program
   spustit
2. Program postupně prochází a zobrazuje jednotlivé snímky ve složce.
   Klikáním myší se označují klouby. Ke každému kliknutí program vytvoří
   výřez označeného kloubu a bokem uloží jeho souřadnice pro případné
   další využití. 
3. Klouby se automaticky pojmenovávají v pořadí zobrazeném na obrázku
   níže. Toto pořadí je při klikání nutné dodržet, jinak budou výřezy
   pojmenované špatně. Pokud nějaký kloub na snímku ruky chybí (amputace
   apod.) je přesto potřeba někam kliknout. Ukázkový obrázek znázorňuje
   pravou ruku, v případě levé ruky je nutné zachovávat stejné pořadí
   prstů (tzn. začínat u ukazováčku a končit u malíčku)
   
   
   ![Zdroj: https://mywwwzone-heckyeahllc.netdna-ssl.com/wp-content/uploads/hand-x-ray-768x923.jpg](dokumentace/posloupnost-kliknuti.jpg)
4. Na další snímek se přejde po stisknutí libovolné klávesy. 
5. Pro projdutí všech snímků ve složce se program sám ukončí.

# Podrobný popis funkčnosti
-   V zadané složce i podložkách program hledá všechny soubory s
    příponami jpg, jpeg, png, tif a tiff.
-   Uživatel na každém snímku klikáním myší vyznačí pozice kloubů,
    program automaticky uloží výřez a pojmenuje ho složením původního
    názvu souboru a lékařského označení daného kloubu. Aktuální oblast k
    vyřezání program ve snímku zvýrazní barevným rámečkem.
-   Je ošetřeno, že nelze vyznačit více než 12 uvedených kloubů.
-   Všechny výřezy kloubů prstů mají rozlišení 299 x 299 pixelů, což je
    vstupní rozměr do neuronové sítě architektury Inception. Kloub
    zápěstní má větší rozměr 500 x 500 px. K výřezům příliš blízko
    okrajů, které by jinak měly rozměr menší, se dolepí prázdné černé
    místo tak, aby zmíněné rozlišení zůstalo zachováno. Tuto funkci je
    možné vypnout nastavením příslušného parametru na False.
-   Velikost výřezu je napevno nastavená v pixelech, protože všechny
    snímky, na které je program určený, mají přibližně stejné rozměry.
    Pokud by se objevily snímky s výrazně většími rozměry, bude potřeba
    rozměr výřezu navázat relativně k rozměru snímku.
-   Výřezy zachovávají původní příponu snímků (např. výřez z png bude
    opět png).
-   Do složky se vstupním snímkem se ukládají i metadata – souřadnice
    označených kloubů. Souřadnice si knihovna OpenCV sama přepočítá z
    rozměrů okna se snímkem na rozměry skutečného snímku.
-   Metadata se ukládají ve formátu, který je čitelný pouze strojově, a
    lze je přečíst v jiném programu napsaném v Pythonu (součástí tohoto
    repozitáře). Metadata se ukládají pomocí knihovny Pickle jako
    serializovaný výstup programátorských objektů. Tyto objekty
    využívají datovou strukturu *slovník*. Pro jeden snímkem vznikne
    jeden slovník, kde klíčem je lékařská zkratka kloubu a hodnotou je
    pole se souřadnicemi *x* a *y*.
-   CHYBÍ: možnost k výřezům ukládat popisky (diagnóza, míra poškození,
    apod.)



