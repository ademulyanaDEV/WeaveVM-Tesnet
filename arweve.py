from web3 import Web3
from eth_account import Account
import time
import sys
import random  # Tambahkan pustaka random

# Detail jaringan
private_key = ''  # GANTI DENGAN PRIVATE KEY ANDA
rpc_url = 'https://testnet.wvm.dev'  # JANGAN DIGANTI
chain_id = 9496  # JANGAN DIGANTI
contract_address = '0x1a3Dd576467eAb8189796da67e4AE1df8afF6422'  # JANGAN DIGANTI
my_address = '0x32D0FAF8FB05FCCcd88D6E82431c3A37391C6CAC'  # GANTI DENGAN ADDRESS EVM ANDA

# Koneksi ke jaringan
web3 = Web3(Web3.HTTPProvider(rpc_url))
if not web3.is_connected():
    raise Exception("Tidak dapat terhubung ke jaringan")

# Buat akun dari private key
account = Account.from_key(private_key)

# Data transaksi untuk bridge ( Jangan Diganti )
data = '0xd0e30db0'

# Fungsi untuk membuat dan mengirim transaksi
def send_bridge_transaction():
    # Ambil nonce untuk alamat pengirim
    nonce = web3.eth.get_transaction_count(my_address)

    # Generate nilai acak untuk jumlah ETH
    random_value = random.uniform(0.00000100, 0.00000200)  # Ambil angka random antara 0.00000100 dan 0.00000200
    value_in_wei = web3.to_wei(random_value, 'ether')

    # Estimasi gas
    try:
        gas_estimate = web3.eth.estimate_gas({
            'to': contract_address,
            'from': my_address,
            'data': data,
            'value': value_in_wei
        })
        gas_limit = gas_estimate + 10000  # Tambahkan buffer gas
    except Exception as e:
        print(f"Error estimating gas: {e}")
        return None

    # Buat transaksi
    transaction = {
        'nonce': nonce,
        'to': contract_address,
        'value': value_in_wei,
        'gas': gas_limit,  # Gunakan gas limit yang diestimasi
        'gasPrice': web3.eth.gas_price,
        'chainId': chain_id,
        'data': data
    }

    # Tanda tangani transaksi dengan private key
    try:
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    except Exception as e:
        print(f"Error signing transaction: {e}")
        return None

    # Kirim transaksi
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(f"Error sending transaction: {e}")
        return None

# Jalankan script sampai dihentikan secara manual
successful_txs = 0

try:
    while True:
        tx_hash = send_bridge_transaction()
        if tx_hash:
            successful_txs += 1
            print(f"Tx Hash: {tx_hash} | Total Tx Sukses: {successful_txs}")
        time.sleep(20)  # Delay 20 detik setiap transaksi
except KeyboardInterrupt:
    print("\nScript dihentikan oleh pengguna.")
    print(f"Total transaksi sukses: {successful_txs}")
    sys.exit(0)
