import asyncio
from tinkoff_acquiring import TinkoffAcquiringAPIClient, TinkoffAPIException

async def main():
    client = TinkoffAcquiringAPIClient('your_terminal_key', 'your_secret')
    try:
        response = await client.init_payment(amount=10000, order_id='12345', description='Test Payment')
        print(response)
    except TinkoffAPIException as e:
        print(f"Error: {e}")

asyncio.run(main())