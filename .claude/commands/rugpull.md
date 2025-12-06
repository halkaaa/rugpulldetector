# Rug Pull Detector - Solana Token Security Analysis

Analyze the provided Solana token address for potential rug pull risks and security issues.

## Task

1. Install dependencies if not already installed:
   - Run: `pip install -r requirements.txt`

2. Execute the Solana Rug Pull Detector analysis:
   - Run: `python src/solana_analyzer.py <TOKEN_ADDRESS>`
   - Where TOKEN_ADDRESS is the Solana token mint address provided by the user

3. The script will:
   - Fetch token metadata from Solscan
   - Analyze holder distribution for concentration risks
   - Check liquidity pools and trading activity
   - Detect potential honeypot characteristics
   - Generate a comprehensive security report

4. Display the markdown report to the user

5. Save the report as a markdown file in the current directory

## Important Notes

- This tool uses FREE public APIs (Solscan, public RPC endpoints)
- Analysis has limitations due to free-tier restrictions
- Always recommend users perform additional manual verification
- Emphasize this is NOT financial advice
- Remind users to test sells with small amounts before investing

## Expected Output

A detailed markdown report containing:
- Overall risk assessment (LOW/MEDIUM/HIGH/EXTREME)
- Critical red flags
- Warnings and positive indicators
- Holder distribution analysis
- Liquidity analysis
- Trading activity patterns
- Actionable recommendations
- Important disclaimers

If you encounter any errors, help the user troubleshoot and provide guidance.
