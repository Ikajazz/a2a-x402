import os
import json
from a2a_x402 import X402Agent, PaymentStatus

class WhaleAlertAgent(X402Agent):
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        super().__init__(merchant_id=self.config['agent_id'], 
                         wallet=self.config['merchant_config']['wallet_address'])

    async def handle_request(self, request):
        # 1. Cek Pembayaran via x402 Protocol
        payment_verified = await self.verify_x402_payment(request)
        
        if not payment_verified:
            # Kirim Header 402 Payment Required jika belum bayar
            return self.generate_402_response(
                amount=self.config['merchant_config']['pricing']['summary_request'],
                asset="USDC",
                memo="Payment for Whale Alert Summary #001"
            )

        # 2. Proses Data (Mock data untuk Pioneer)
        whale_data = self.get_latest_whale_alerts()
        
        return {
            "status": "success",
            "data": whale_data,
            "message": "Thank you for your payment. Here is the latest intelligence."
        }

    def get_latest_whale_alerts(self):
        # In production, ini akan narik data dari Whale Alert API atau On-chain monitor
        return [
            {"time": "2026-06-08 08:15", "asset": "ETH", "amount": "5,000", "from": "Unknown", "to": "Coinbase", "type": "Exchange Inflow"},
            {"time": "2026-06-08 08:12", "asset": "USDC", "amount": "10,000,000", "from": "Binance", "to": "Unknown Wallet", "type": "Whale Withdrawal"}
        ]

if __name__ == "__main__":
    agent = WhaleAlertAgent("vdc_config.json")
    print(f"Agent {agent.config['name']} is ready on {agent.config['merchant_config']['wallet_address']}")
