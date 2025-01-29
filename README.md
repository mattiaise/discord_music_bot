# Discord Music Bot 

Un bot musicale per Discord che permette agli utenti di riprodurre musica direttamente dai canali vocali.

## Funzionalità principali 

- **Code di riproduzione:** Aggiungi o rimuovi le canzoni nella coda.
- **Comandi semplici:** Interfaccia intuitiva per controllare il bot (play, pause, skip, stop, ecc.).
- **Prestazioni ottimizzate:** Audio di alta qualità con minima latenza.

## Dipendenze e requisiti

- **Versione di python:** `3.8.* - 3.11.*`
- **Installare le dipendenze:** `pip install -r dependencies.txt`

## Comandi disponibili 

- `!play <url>`: Riproduce una canzone.
- `!pause`: Metti in pausa la riproduzione.
- `!resume`: Riprendi la riproduzione.
- `!skip`: Salta alla prossima canzone.
- `!stop`: Interrompi la riproduzione e svuota la coda.
- `!playlist`: Riproduce la playlist preimpostata.
- `!leave`: Fa uscire il bot dal canale vocale.

## Struttura del progetto 

```
discord-music-bot
├── src
│   ├── main.py           # File principale del bot
│   ├── music_cog.py      # File dei comandi
│   ├── help.cog.py       # File del comando help
├── playlists
│   ├── triste.py         # Lista di canzoni tristi
│   ├── prepartita.py     # Lista di canzoni dance
├── dependecies.txt       # File che mostra le dipendenze
├── token.txt             # Token del bot discord
└── README.md             # Documentazione
```
