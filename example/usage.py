import asyncio
from tinkoff_acquiring import TinkoffAcquiringAPIClient, TinkoffAPIException

async def main():
    client = TinkoffAcquiringAPIClient('your_terminal_key', 'your_secret')
    try:
        # Creating a payment
        response = await client.init_payment(
            amount=100,
            order_id='use_random_order_id',
            description='Payment for order 12345',
        )
        payment_id = response['PaymentId']
        print(f"Follow the link to complete the payment: {response['PaymentURL']}")
        
        # Getting payment status
        state = await client.get_payment_state(payment_id)
        print(f"Payment status: {state['Status']}")

        # Confirming the payment
        confirm = await client.confirm_payment(payment_id)
        print(f"Payment confirmation status: {confirm['Status']}")

        # Canceling the payment
        cancel = await client.cancel_payment(payment_id)
        print(f"Payment cancellation status: {cancel['Status']}")

    except TinkoffAPIException as e:
        print(f"Error: {e}")

asyncio.run(main())
