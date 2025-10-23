#!/usr/bin/env python3
"""
Analysiere den BIP143 Preimage für die Cascoin-Transaktion
"""
import sys
sys.path.insert(0, '.')

from electrum.transaction import tx_from_any, Sighash
from electrum.crypto import sha256d
from electrum import bitcoin

# Die PSBT laden
psbt_b64 = "cHNidP8BAHICAAAAAdA2I4RDEfxQbpugVxKeEtBFbGCrw875cFZFluXgVTRwAAAAAAD/////AqCGAQAAAAAAF6kUFrphKgsSkPjA/yuZodmZ6eHB4XqHBAqXAAAAAAAWABSzknYI/8HTRLmlkjVDRt8rP5aoWgAAAAAAAQEfgJaYAAAAAAAWABSLYr987dpbgwvlmiy3VGFwlUtChQEA3wIAAAAAAQHlJYy1/GqVENaEdz9fvXUQWhShENxOyqn6JaAEiLLBOAEAAAAA/v///wKAlpgAAAAAABYAFItiv3zt2luDC+WaLLdUYXCVS0KFQIchAAAAAAAWABQhcAEOA3s5914AXDQlJdTBhvbH7AJIMEUCIQDm9ekabx6aq7lbS0MfXunbPv7MgsagJndUYbEXmUfTVQIgVu7Bw0rQQSocnum+SbQBmzvYZIbNk+oQFA9C41Q0s2FBIQN7pK4C1MrRZa4atJv0pbqeI6bdCDTErZcV95ewJL4oX+h2AgAiBgLm0DT0Xu66lxi1eW6aL+EdW1rhk1mtrsAPYPDBfsvlqhAdnj0tAAAAgAAAAAAAAAAAAAAiAgI6I+U5v5y4+9JDDjzabZ4ChmPGr1W287X9n0Bo16qYGxAdnj0tAAAAgAEAAAAAAAAAAA=="

tx = tx_from_any(psbt_b64, deserialize=True)
inp = tx.inputs()[0]

print("=" * 80)
print("BIP143 PREIMAGE BERECHNUNG FÜR CASCOIN")
print("=" * 80)
print()

# Transaction Details
print("TRANSACTION DETAILS:")
print(f"  Version: {tx.version}")
print(f"  Locktime: {tx.locktime}")
print(f"  nInputs: {len(tx.inputs())}")
print(f"  nOutputs: {len(tx.outputs())}")
print()

# Input Details
print("INPUT #0 DETAILS:")
print(f"  Prevout: {inp.prevout.txid.hex()}:{inp.prevout.out_idx}")
print(f"  Value: {inp.value_sats()} sats (1.0 CAS)")
print(f"  nSequence: 0x{inp.nsequence:08x}")
print(f"  ScriptPubKey: {inp.scriptpubkey.hex()}")
print(f"  Address: {inp.address}")
print()

# BIP143 Preimage-Komponenten berechnen
print("BIP143 PREIMAGE KOMPONENTEN:")
print()

# 1. nVersion (4 bytes LE)
nVersion = int.to_bytes(tx.version, 4, 'little', signed=True)
print(f"1. nVersion: {nVersion.hex()}")

# 2. hashPrevouts
from electrum.crypto import sha256d
prevouts_data = inp.prevout.serialize_to_network()
hashPrevouts = sha256d(prevouts_data)
print(f"2. hashPrevouts: {hashPrevouts.hex()}")
print(f"   (from prevout: {prevouts_data.hex()})")

# 3. hashSequence
nSeq = int.to_bytes(inp.nsequence, 4, 'little')
hashSequence = sha256d(nSeq)
print(f"3. hashSequence: {hashSequence.hex()}")
print(f"   (from nSequence: {nSeq.hex()})")

# 4. outpoint (36 bytes)
outpoint = inp.prevout.serialize_to_network()
print(f"4. outpoint: {outpoint.hex()}")

# 5. scriptCode
# Für P2WPKH: OP_DUP OP_HASH160 <20-byte-hash> OP_EQUALVERIFY OP_CHECKSIG
pubkey_hash = inp.scriptpubkey[2:]  # Skip OP_0 and push length
scriptCode = bytes([0x76, 0xa9, 0x14]) + pubkey_hash + bytes([0x88, 0xac])
from electrum.bitcoin import var_int
scriptCode_serialized = var_int(len(scriptCode)) + scriptCode
print(f"5. scriptCode: {scriptCode_serialized.hex()}")
print(f"   Length: {len(scriptCode)} bytes")
print(f"   Format: OP_DUP OP_HASH160 <{pubkey_hash.hex()}> OP_EQUALVERIFY OP_CHECKSIG")

# 6. amount (8 bytes LE)
amount = int.to_bytes(inp.value_sats(), 8, 'little')
print(f"6. amount: {amount.hex()}")
print(f"   Value: {inp.value_sats()} sats")

# 7. nSequence (4 bytes LE)
nSequence = int.to_bytes(inp.nsequence, 4, 'little')
print(f"7. nSequence: {nSequence.hex()}")

# 8. hashOutputs
outputs_data = b''.join(out.serialize_to_network() for out in tx.outputs())
hashOutputs = sha256d(outputs_data)
print(f"8. hashOutputs: {hashOutputs.hex()}")
print(f"   (from {len(tx.outputs())} outputs, {len(outputs_data)} bytes)")

# 9. nLocktime (4 bytes LE)
nLocktime = int.to_bytes(tx.locktime, 4, 'little')
print(f"9. nLocktime: {nLocktime.hex()}")

# 10. nHashType (4 bytes LE) - WITH SIGHASH_FORKID!
sighash = Sighash.ALL | Sighash.FORKID  # 0x01 | 0x40 = 0x41
nHashType = int.to_bytes(sighash, 4, 'little')
print(f"10. nHashType: {nHashType.hex()}")
print(f"    = 0x{sighash:02x} (SIGHASH_ALL | SIGHASH_FORKID)")

print()
print("=" * 80)
print("COMPLETE PREIMAGE:")
print("=" * 80)

# Komplettes Preimage
preimage = (nVersion + hashPrevouts + hashSequence + outpoint + 
            scriptCode_serialized + amount + nSequence + 
            hashOutputs + nLocktime + nHashType)

print(f"Length: {len(preimage)} bytes")
print(f"Hex: {preimage.hex()}")
print()

# Message Hash (SHA256d)
msg_hash = sha256d(preimage)
print(f"Message Hash (SHA256d): {msg_hash.hex()}")
print()
print("=" * 80)
print("Dieser Hash sollte signiert werden mit dem Private Key!")
print("=" * 80)

