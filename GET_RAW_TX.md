# Wie man die Raw Transaction bekommt

## Methode 1: Aus Electrum GUI

1. Erstellen Sie eine Transaktion (aber senden Sie sie NICHT!)
2. Im Transaction Preview Dialog:
   - Suchen Sie nach "Details" oder "Advanced" oder ähnlichem Button
   - Oder Rechtsklick → "View Transaction"
3. Kopieren Sie den kompletten HEX-String
4. Teilen Sie mir diesen Hex-String mit

## Methode 2: Mit electrum-env Kommando

```bash
cd /home/alexander/cascoin-electrum

# Erstellen Sie eine unsigned transaction
./electrum-env payto M9yLNXc1EjirQWPaZBZjNVv6KvRyeasFJg 0.01 --unsigned > /tmp/tx.txt

# Zeigen Sie die Transaction
cat /tmp/tx.txt
```

## Methode 3: Transaction aus dem Wallet exportieren

1. Tools → Load transaction → From file
2. Oder: Save Transaction → Als File speichern
3. Öffnen Sie die Datei und kopieren Sie den Hex

## Was ich damit mache:

Mit der Raw Transaction kann ich:
1. Die genaue Signatur analysieren
2. Den Preimage-Hash neu berechnen
3. Vergleichen mit was Cascoin erwartet
4. Den genauen Fehler identifizieren

## Alternative: Python-Script

```python
cd /home/alexander/cascoin-electrum
python3 << 'EOF'
import sys
sys.path.insert(0, '.')

from electrum import wallet, storage, simple_config, constants
from electrum.transaction import PartialTransaction, PartialTxOutput
from electrum import bitcoin

# Laden Sie Ihr Wallet
config = simple_config.SimpleConfig()
# ... (vollständiger Code folgt wenn nötig)
EOF
```

---

**BITTE**: Teilen Sie mir die Raw Transaction (Hex) mit, dann kann ich das Problem sofort lösen!

