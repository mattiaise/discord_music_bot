# Discord Music Bot 

Un bot musicale per Discord che permette agli utenti di riprodurre musica direttamente dai canali vocali.

## Funzionalità principali 

- **Code di riproduzione:** Aggiungi o rimuovi le canzoni nella coda.
- **Comandi semplici:** Interfaccia intuitiva per controllare il bot (play, pause, skip, stop, ecc.).
- **Prestazioni ottimizzate:** Audio di alta qualità con minima latenza.

## Dipendenze e requisiti

- **Versione di python:** `3.8.* - 3.11.*`
- **Installare le dipendenze:** `pip install -r dependencies.txt`
- **Installare FFMPEG** e inserire la cartella `bin` all'interno delle variabili di ambiente del sistema nella sezione `Path`

## Comandi disponibili 

- `!play <url>`: Riproduce una canzone.
- `!pause`: Metti in pausa la riproduzione.
- `!resume`: Riprendi la riproduzione.
- `!skip`: Salta alla prossima canzone.
- `!stop`: Interrompi la riproduzione e svuota la coda.
- `!playlist`: Riproduce la playlist preimpostata.
- `!leave`: Fa uscire il bot dal canale vocale.

## Configurazione 

Prima di utilizzare il bot inserire il proprio token all'interno del file `main.py`.

Se si ha intezione di usare il comando `!playlist` popolare il file `playlist/playlist.txt` con i link YouTube delle canzoni che si vuole riprodurre (uno per ogni riga). 

## Struttura del progetto 

```
discord-music-bot
├── src
│   ├── main.py           # File principale del bot
│   ├── music_cog.py      # File dei comandi
│   ├── help.cog.py       # File del comando help
├── playlists
│   ├── triste.txt        # Lista di canzoni tristi
│   ├── prepartita.txt    # Lista di canzoni dance
├── dependecies.txt       # File che mostra le dipendenze
└── README.md             # Documentazione
```
