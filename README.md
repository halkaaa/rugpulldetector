# Solana Rug Pull Detector

AI-Powered cryptocurrency security analysis tool that helps investors identify scams, honeypots, and red flags in Solana tokens before investing.

## Overview

The Solana Rug Pull Detector is a comprehensive security analysis tool that evaluates tokens across 6 critical dimensions using on-chain data, smart contract analysis, and pattern recognition. It generates detailed security reports with clear risk ratings (LOW/MEDIUM/HIGH/EXTREME) and actionable recommendations.

### What It Does

Analyzes Solana tokens for:
- Contract security vulnerabilities
- Liquidity pool status and locks
- Holder distribution and concentration risks
- Honeypot characteristics
- Trading activity patterns
- Project metadata completeness

### Key Features

- **Multi-Dimensional Analysis**: 6 core security checks
- **Free-Tier APIs**: Works with Solscan and public RPC endpoints
- **Clear Risk Ratings**: LOW/MEDIUM/HIGH/EXTREME classifications
- **Detailed Reports**: Markdown reports with evidence-based verdicts
- **100+ Scam Indicators**: Comprehensive red flag detection
- **Easy Integration**: Slash command for Claude Code or standalone CLI

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone or download this repository**

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

That's it! The tool uses free public APIs and requires no API keys.

## Usage

### Option 1: Claude Code Slash Command (Recommended)

If you're using Claude Code:

```
/rugpull <SOLANA_TOKEN_ADDRESS>
```

Example:
```
/rugpull EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```

### Option 2: Command Line Interface

```bash
python detect.py <SOLANA_TOKEN_ADDRESS>
```

Example:
```bash
python detect.py DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263
```

### Option 3: Python Module

```python
from src.solana_analyzer import SolanaRugPullDetector, format_markdown_report

detector = SolanaRugPullDetector()
results = detector.analyze_token("TOKEN_ADDRESS")
report = format_markdown_report(results)

print(report)
```

## Analysis Framework

### 1. Contract Security
- Verifies token metadata completeness
- Checks for malicious functions (mint, pause, blacklist)
- Validates token program type
- Reviews ownership status

### 2. Liquidity Analysis
- Confirms presence of liquidity pools
- Checks lock status and duration
- Validates platform legitimacy
- Analyzes liquidity ratios

### 3. Holder Distribution
- Identifies concentration risks
- Tracks top holder percentages
- Detects developer holdings
- Flags suspicious wallet clusters

### 4. Honeypot Detection
- Tests sell functionality indicators
- Checks for hidden taxes
- Identifies transaction restrictions
- Analyzes transfer patterns

### 5. Metadata & Project Research
- Validates token information
- Checks supply and decimals
- Reviews holder counts
- Assesses completeness

### 6. Trading Activity Analysis
- Detects wash trading patterns
- Identifies coordinated pumps
- Analyzes volume patterns
- Checks address diversity

## Understanding Results

### Risk Levels

| Level | Score | Description | Action |
|-------|-------|-------------|--------|
| **EXTREME** | 60-100 | Multiple critical red flags | DO NOT INVEST |
| **HIGH** | 40-59 | Significant warning signs | Extreme caution required |
| **MEDIUM** | 20-39 | Some concerning indicators | Additional research needed |
| **LOW** | 0-19 | Fewer red flags | Still perform DYOR |

### Critical Red Flags

- Top holder owns >50% of supply
- No liquidity pools found
- Missing token metadata
- Fewer than 10 holders
- Top 10 holders control >80%
- No recent trading activity

### Warning Signs

- Top holder owns 15-30%
- Low holder count (10-50)
- Cannot verify liquidity lock
- Suspicious wash trading patterns
- Limited address diversity

### Positive Indicators

- Holder count >100
- Top holder <10% of supply
- Multiple liquidity pools active
- Diverse trading addresses
- Complete metadata present

## Output Format

The tool generates a comprehensive markdown report containing:

1. **Overall Risk Assessment**
   - Risk level and score
   - Visual risk indicator

2. **Critical Findings**
   - Red flags (critical issues)
   - Warnings (concerning indicators)
   - Green flags (positive signals)

3. **Detailed Analysis**
   - Token information
   - Holder distribution breakdown
   - Liquidity status
   - Trading activity metrics

4. **Recommendations**
   - Risk-appropriate action items
   - Verification steps
   - Best practices

5. **Disclaimers**
   - Tool limitations
   - Manual verification guidance
   - Risk warnings

## Example Report Structure

```markdown
# Solana Rug Pull Detector Report

**Token Address**: `DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263`
**Risk Level**: **MEDIUM**
**Risk Score**: 35/100

## Critical Red Flags
- Top holder owns 25% of supply

## Warnings
- Cannot verify liquidity lock status
- Limited trading history

## Positive Indicators
- 500+ unique holders
- Multiple liquidity pools found
- Active trading with diverse addresses

[... detailed analysis sections ...]
```

## Use Cases

### 1. Pre-Investment Screening
Screen new tokens before buying:
```bash
python detect.py <NEW_TOKEN_ADDRESS>
```

### 2. Honeypot Detection
Verify a token isn't a honeypot:
```bash
python detect.py <SUSPICIOUS_TOKEN>
```

### 3. Portfolio Audit
Check tokens you already hold:
```bash
python detect.py <HELD_TOKEN_1>
python detect.py <HELD_TOKEN_2>
```

### 4. Comparative Analysis
Compare multiple tokens:
```bash
python detect.py <TOKEN_A>
python detect.py <TOKEN_B>
# Compare risk scores and flags
```

### 5. pump.fun Tokens
Analyze new memecoin launches:
```bash
python detect.py <PUMP_FUN_TOKEN>
```

## Limitations

### Data Limitations
- Uses free-tier APIs with rate limits
- Cannot fully simulate sell transactions
- Limited contract code analysis depth
- No team background verification
- Data may lag in fast markets

### Tool Limitations
- Cannot predict sophisticated future scams
- Reduces but doesn't eliminate risk
- Public data only - no insider information
- No financial advice provided

### What This Tool CANNOT Do
- Predict future rug pulls with certainty
- Verify team identity and background
- Audit complex smart contract code
- Guarantee investment safety
- Replace comprehensive due diligence

## Best Practices

### Before Using Results

1. **Verify Token Address**
   - Double-check on Solscan.io
   - Confirm it's the correct token

2. **Combine with Other Tools**
   - RugCheck.xyz
   - Token Sniffer
   - DEXScreener
   - Solscan

3. **Manual Research**
   - Visit project website
   - Check Twitter/Discord
   - Read whitepaper
   - Verify team identity

### After Analysis

1. **Test Small First**
   - Buy small amount ($10-50)
   - Test sell immediately
   - Verify exit is possible

2. **Monitor Continuously**
   - Re-analyze weekly
   - Watch holder changes
   - Track liquidity shifts

3. **Trust Your Instincts**
   - If it feels wrong, it probably is
   - No FOMO - avoid emotional decisions
   - Better safe than sorry

## API Information

### Free APIs Used

- **Solscan Public API**
  - Token metadata
  - Holder information
  - Transfer history
  - Market data

- **Public RPC Endpoints**
  - On-chain data
  - Transaction information

### Rate Limits

Free tier APIs have limitations:
- Solscan: ~10 requests/minute
- Wait 5-10 seconds between analyses
- Use responsibly

### Upgrading to Paid APIs

For higher limits, consider:
- Solscan Pro API (official key)
- Helius RPC (premium tier)
- QuickNode (dedicated nodes)

Update API keys in `src/solana_analyzer.py`:
```python
self.solscan_api = "https://pro-api.solscan.io"
# Add API key to headers
```

## Project Structure

```
rugpulldetector/
├── .claude/
│   └── commands/
│       └── rugpull.md          # Slash command definition
├── src/
│   └── solana_analyzer.py      # Core analysis engine
├── detect.py                    # CLI wrapper script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── EXAMPLES.md                  # Usage examples
```

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'requests'"**
```bash
pip install -r requirements.txt
```

**"API returned 429 - Too Many Requests"**
- Wait 1-2 minutes between analyses
- Free APIs have rate limits
- Consider using paid API tier

**"No holder data available"**
- Token might be brand new
- API temporarily down
- Verify token address

**"Could not fetch token metadata"**
- Check token address is correct
- Token may not be indexed
- Visit Solscan.io to verify

### Getting Help

1. Review EXAMPLES.md for usage patterns
2. Check token address on Solscan.io
3. Test with known token (USDC) first
4. Verify dependencies installed
5. Check Python version (3.7+)

## Contributing

This tool is open for improvements:

- Additional analysis checks
- Support for more DEXes
- Enhanced honeypot detection
- Team verification features
- Historical rug pull database

## Disclaimer

### IMPORTANT - READ CAREFULLY

This tool is for **educational and research purposes only**.

- **NOT FINANCIAL ADVICE**: This tool does not provide investment advice
- **NO GUARANTEES**: Cannot guarantee protection from scams
- **USE AT YOUR OWN RISK**: All cryptocurrency investments are extremely risky
- **TOTAL LOSS POSSIBLE**: You may lose your entire investment
- **DYOR REQUIRED**: Always do your own research
- **TEST FIRST**: Always test with small amounts

### Legal

- No warranty provided, express or implied
- Authors not liable for investment losses
- Use of this tool does not create any advisory relationship
- Users responsible for own investment decisions
- Cryptocurrency regulations vary by jurisdiction

### Security Notice

- Never share private keys or seed phrases
- This tool doesn't require wallet connection
- Only analyzes public blockchain data
- No personal information collected

## License

This project is provided as-is for educational purposes.

## Acknowledgments

Built with:
- Claude Code
- Solscan Public API
- Python Requests library

## Version History

- **v1.0** (2025-01-06)
  - Initial release
  - Solana support
  - 6-dimension analysis framework
  - Free API integration
  - Markdown report generation

## Roadmap

Potential future enhancements:
- Multi-chain support (ETH, BSC, Polygon)
- Enhanced contract analysis
- Team background checks
- Historical scam pattern database
- Real-time monitoring alerts
- Integration with more DEX APIs
- Web interface

---

**Remember**: Crypto is high risk. This tool helps identify obvious red flags but cannot eliminate all risks. Never invest more than you can afford to lose. Always DYOR (Do Your Own Research).

**Stay safe and invest wisely!**
