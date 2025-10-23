# Cascoin Electrum Transaction Debug

## Aktueller Status

### ✅ Was implementiert ist:
1. **SIGHASH_FORKID (0x41)** - wird zu allen Signaturen hinzugefügt
2. **BIP143 Preimage-Format** - für alle Transaktionen (Segwit und Legacy mit FORKID)
3. **nSequence = 0xffffffff** - finale Transaktion, kein RBF
4. **locktime = 0** - keine Zeitsperre
5. **COIN = 10000000** - 7 Dezimalstellen (korrekt für Cascoin)
6. **base_sighash** Berechnungen für FORKID-Kompatibilität

### ❌ Aktuelles Problem:
**Fehler**: "Signature must be zero for failed CHECK(MULTI)SIG operation"

**Bedeutung**: Die Signatur wird erstellt, ist aber **ungültig** bei der Verifizierung.

## Mögliche Ursachen

### 1. UTXO-Value Mismatch
BIP143 benötigt den exakten UTXO-Wert im `amount`-Feld des Preimage.
- Wenn dieser Wert falsch ist → ungültige Signatur
- Cascoin hat 7 Dezimalstellen, nicht 8!

### 2. ScriptCode Problem
Für P2WPKH (Segwit `cas1q...`) sollte der ScriptCode sein:
```
76 a9 14 <20-byte-pubkey-hash> 88 ac
OP_DUP OP_HASH160 <pubkeyhash> OP_EQUALVERIFY OP_CHECKSIG
```

### 3. Preimage-Serialisierung
BIP143-Format mit SIGHASH_FORKID:
```
nVersion + hashPrevouts + hashSequence + outpoint + scriptCode + 
amount + nSequence + hashOutputs + nLocktime + nHashType (4 bytes, 0x41000000)
```

## Debug-Schritte

### Option 1: Testen mit Legacy-Wallet
Erstellen Sie ein neues Wallet:
1. File → New/Restore
2. Wählen Sie einen **Legacy-Typ** (nicht Segwit)
3. Senden Sie Coins dorthin
4. Versuchen Sie, von dort zu senden

**Grund**: Testen ob das Problem Segwit-spezifisch ist

### Option 2: Raw Transaction analysieren
1. Erstellen Sie eine Transaktion (aber senden Sie sie NICHT)
2. Im Transaction-Dialog: "Show Details" oder ähnlich
3. Kopieren Sie die **Raw Transaction** (Hex-String)
4. Teilen Sie mir den Hex-String mit

**Vorteil**: Ich kann die exakte Transaktion analysieren

### Option 3: Komodo Wallet vergleichen
Da Komodo Wallet funktioniert:
1. Erstellen Sie dieselbe Transaktion in Komodo Wallet
2. Exportieren Sie die Raw Transaction
3. Vergleichen Sie sie mit Electrum

## Technische Details

### Ihre Wallet-Adresse
- `cas1q8judx239yxv5cula9l2at4skprmpqmskax0hzh`
- Typ: **P2WPKH (Native Segwit)**
- ScriptPubKey: `00143cb8d32a2521994c73fd2fd5d5d61608f6106e16`

### Empfänger-Adresse
- `M9yLNXc1EjirQWPaZBZjNVv6KvRyeasFJg`
- Typ: **P2SH**
- ScriptPubKey: `a91416ba612a0b1290f8c0ff2b99a1d999e9e1c1e17a87`

## Nächste Schritte

Bitte wählen Sie eine der folgenden Optionen:

1. **Legacy-Wallet testen** (Option 1 oben)
2. **Raw Transaction teilen** (Option 2 oben) 
3. **Mit Komodo vergleichen** (Option 3 oben)

Oder teilen Sie mir mit, wenn Sie weitere Fehlerdetails haben!

---

**Stand**: Oktober 23, 2025
**Cascoin Electrum Version**: 4.6.2+cascoin

