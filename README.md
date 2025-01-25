# Discord Music Bot 

Un bot musicale per Discord che permette agli utenti di riprodurre musica direttamente dai canali vocali.

## Funzionalità principali 

- **Code di riproduzione:** Aggiungi o rimuovi le canzoni nella coda.
- **Comandi semplici:** Interfaccia intuitiva per controllare il bot (play, pause, skip, stop, ecc.).
- **Prestazioni ottimizzate:** Audio di alta qualità con minima latenza.

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
├── dependecies.txt       # File che mostra le dipendenze
├── songs.txt             # Playlist di default
├── token.txt             # Token del bot discord
└── README.md             # Documentazione
```
