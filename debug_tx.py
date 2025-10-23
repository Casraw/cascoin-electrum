#!/usr/bin/env python3
"""
Debug-Tool für Cascoin Elektrum Transaktionen
"""
import sys
import os

# Füge Electrum zum Python-Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from electrum import constants, bitcoin
from electrum.transaction import Sighash

# Cascoin ist bereits als Standard-Netzwerk gesetzt

print("=" * 60)
print("Cascoin Electrum Transaction Debugger")
print("=" * 60)
print()

# Test 1: SIGHASH Flags
print("1. SIGHASH-Konfiguration:")
print(f"   SIGHASH_ALL: 0x{Sighash.ALL:02x}")
print(f"   SIGHASH_FORKID: 0x{Sighash.FORKID:02x}")
print(f"   Combined: 0x{Sighash.ALL | Sighash.FORKID:02x}")
print(f"   Is 0x41 valid? {Sighash.is_valid(0x41)}")
print()

# Test 2: Adressen
test_addresses = [
    "M9yLNXc1EjirQWPaZBZjNVv6KvRyeasFJg",  # P2SH (empfänger)
]

print("2. Adress-Analyse:")
for addr in test_addresses:
    try:
        script = bitcoin.address_to_script(addr)
        print(f"   Adresse: {addr}")
        print(f"   Script: {script.hex()}")
        if script[0] == 0xa9:
            addr_type = "P2SH"
        elif script[0] == 0x76:
            addr_type = "P2PKH"
        elif script[0] == 0x00:
            addr_type = "P2WPKH/P2WSH (Segwit)"
        else:
            addr_type = f"Unknown (0x{script[0]:02x})"
        print(f"   Typ: {addr_type}")
    except Exception as e:
        print(f"   Adresse: {addr}")
        print(f"   Fehler: {e}")
    print()

# Test 3: Netzwerk-Info
print("3. Netzwerk-Konfiguration:")
print(f"   NET_NAME: {constants.net.NET_NAME}")
print(f"   TESTNET: {constants.net.TESTNET}")
print(f"   SEGWIT_HRP: {constants.net.SEGWIT_HRP}")
print(f"   ADDRTYPE_P2PKH: {constants.net.ADDRTYPE_P2PKH}")
print(f"   ADDRTYPE_P2SH: {constants.net.ADDRTYPE_P2SH}")
print()

print("=" * 60)
print("HINWEISE:")
print("- Empfängeradresse M9yLNXc1EjirQWPaZBZjNVv6KvRyeasFJg ist P2SH")
print("- Cascoin benötigt SIGHASH_FORKID (0x41) für alle Signaturen")
print("- BIP143-Format wird für alle Transaktionen verwendet")
print()
print("Wenn der Fehler 'Signature must be zero' auftritt:")
print("1. Prüfen Sie, ob die INPUT-Adresse Segwit oder Legacy ist")
print("2. Prüfen Sie die Log-Datei für Preimage-Details")
print("3. Stellen Sie sicher, dass der UTXO-Wert korrekt ist")
print("=" * 60)

