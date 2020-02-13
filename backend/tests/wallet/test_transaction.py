from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
import pytest

def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)
    print(transaction.output[recipient])
    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount
    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key
    assert Wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match='Amount exceeds balance'):
        Transaction(Wallet(), 'recipient', 9001)


def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    with pytest.raises(Exception, match='Amount exceeds balance'):
        transaction.update(sender_wallet, 'new_recipient', 9001)