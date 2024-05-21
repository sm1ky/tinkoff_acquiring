import aiohttp
import hashlib
import logging

class TinkoffAPIException(Exception):
    pass

class TinkoffAcquiringAPIClient:
    API_ENDPOINT = 'https://securepay.tinkoff.ru/v2/'

    def __init__(self, terminal_key, secret):
        self.terminal_key = terminal_key
        self.secret = secret
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def send_request(self, endpoint, params):
        async with aiohttp.ClientSession() as session:
            params['TerminalKey'] = self.terminal_key
            params['Token'] = self.generate_token(params)

            async with session.post(self.API_ENDPOINT + endpoint, json=params) as response:
                response_data = await response.json()
                self.logger.info(f"Response data: {response_data}")
                if response.status != 200 or not response_data.get('Success'):
                    error_message = response_data.get('Message', 'Unknown error')
                    self.logger.error(f'API request failed: {error_message}')
                    raise TinkoffAPIException(error_message)
                return response_data

    def generate_token(self, params):
        ignore_keys = ['Shops', 'Receipt', 'Data']
        for key in ignore_keys:
            if key in params:
                del params[key]

        params['Password'] = self.secret
        sorted_params = sorted(params.items())
        token_str = ''.join(str(value) for _, value in sorted_params)
        return hashlib.sha256(token_str.encode('utf-8')).hexdigest()

    async def init_payment(self, amount, order_id, description, receipt=None, success_url: str = None, fail_url: str = None):
        params = {
            'Amount': int(amount),
            'OrderId': order_id,
            'Description': description,
        }
        if success_url:
            params['SuccessURL'] = success_url
        if fail_url:
            params['FailURL'] = fail_url
        if receipt:
            params['Receipt'] = receipt
        return await self.send_request('Init', params)

    async def get_payment_state(self, payment_id):
        params = {'PaymentId': payment_id}
        return await self.send_request('GetState', params)

    async def confirm_payment(self, payment_id):
        params = {'PaymentId': payment_id}
        return await self.send_request('Confirm', params)

    async def cancel_payment(self, payment_id):
        params = {'PaymentId': payment_id}
        return await self.send_request('Cancel', params)

