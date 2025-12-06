# Solana Rug Pull Detector - Usage Examples

This document provides examples of how to use the Solana Rug Pull Detector.

## Basic Usage

### Using the Slash Command (Claude Code)

If you're using Claude Code, simply type:

```
/rugpull <TOKEN_ADDRESS>
```

Example:
```
/rugpull EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```

### Using the CLI Script

```bash
python detect.py <TOKEN_ADDRESS>
```

Example:
```bash
python detect.py EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```

### Using the Python Module Directly

```python
from src.solana_analyzer import SolanaRugPullDetector, format_markdown_report

# Create detector instance
detector = SolanaRugPullDetector()

# Analyze a token
token_address = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
results = detector.analyze_token(token_address)

# Generate markdown report
report = format_markdown_report(results)

# Print or save the report
print(report)
```

## Example Token Addresses for Testing

### Well-Known Tokens (Lower Risk)

**USDC (USD Coin)**
```
EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```
- Established stablecoin
- High holder count
- Good distribution
- Expected Result: LOW risk

**Bonk**
```
DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263
```
- Popular memecoin
- Large community
- Good liquidity
- Expected Result: LOW-MEDIUM risk

### Use Cases

#### 1. Pre-Investment Screening

Before investing in a new token from pump.fun or other platforms:

```bash
python detect.py <NEW_TOKEN_ADDRESS>
```

Check for:
- Holder concentration (top holder should be <15%)
- Liquidity presence
- Trading activity
- Red flags in metadata

#### 2. Honeypot Detection

When you suspect a token might be a honeypot:

```bash
python detect.py <SUSPICIOUS_TOKEN>
```

Look for:
- Inability to verify sells
- Very low holder count
- No liquidity pools
- Extreme holder concentration

#### 3. Comparative Analysis

Compare multiple tokens to choose the safer investment:

```bash
# Analyze token A
python detect.py <TOKEN_A_ADDRESS>

# Analyze token B
python detect.py <TOKEN_B_ADDRESS>

# Compare risk scores and red flags
```

#### 4. Portfolio Audit

Check tokens you already hold:

```bash
# Check each token in your portfolio
python detect.py <HELD_TOKEN_1>
python detect.py <HELD_TOKEN_2>
python detect.py <HELD_TOKEN_3>
```

Review for any developing red flags.

## Understanding the Output

### Risk Levels

- **LOW**: Fewer red flags, but still requires DYOR
- **MEDIUM**: Some concerning indicators, proceed with caution
- **HIGH**: Significant red flags, high risk of loss
- **EXTREME**: Multiple critical issues, likely scam - DO NOT INVEST

### Risk Score

- **0-20**: Generally safer tokens with established presence
- **21-40**: Moderate risk, requires additional research
- **41-60**: High risk, multiple warning signs
- **61-100**: Extreme danger, very likely scam or rug pull

### Key Indicators to Watch

#### Critical Red Flags (Avoid Investment)
- Top holder owns >50% of supply
- No liquidity pools found
- Missing token name/symbol
- Very few holders (<10)
- Top 10 holders control >80%

#### Warning Signs (Extra Caution)
- Top holder owns 15-30%
- Low holder count (10-50)
- Cannot verify liquidity lock
- Limited trading activity
- Suspicious wash trading patterns

#### Positive Indicators
- Holder count >100
- Top holder <10%
- Multiple liquidity pools
- Active trading with diverse addresses
- Complete metadata

## Advanced Usage

### Batch Analysis

Create a script to analyze multiple tokens:

```python
from src.solana_analyzer import SolanaRugPullDetector, format_markdown_report

tokens = [
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",  # BONK
    # Add more tokens
]

detector = SolanaRugPullDetector()

for token in tokens:
    print(f"\n{'='*60}")
    print(f"Analyzing: {token}")
    print('='*60)

    results = detector.analyze_token(token)

    print(f"Risk: {results['overall_risk']} ({results['risk_score']}/100)")
    print(f"Red Flags: {len(results['red_flags'])}")
    print(f"Warnings: {len(results['warnings'])}")
```

### Custom Analysis

Access individual analysis components:

```python
from src.solana_analyzer import SolanaRugPullDetector

detector = SolanaRugPullDetector()

# Just check holder distribution
holders = detector._analyze_holders("TOKEN_ADDRESS")
print(f"Top holder: {holders['top_holder_percentage']}%")

# Just check liquidity
liquidity = detector._analyze_liquidity("TOKEN_ADDRESS")
print(f"Has liquidity: {liquidity['has_liquidity']}")
```

## Integration with Research Workflow

### Recommended Research Process

1. **Initial Discovery**
   - Find token on pump.fun, DEXScreener, or Twitter

2. **Automated Analysis** (This Tool)
   ```bash
   python detect.py <TOKEN_ADDRESS>
   ```

3. **Manual Verification**
   - Visit project website
   - Check Twitter/Discord
   - Review contract on Solscan
   - Search for audit reports

4. **Community Check**
   - Read Reddit/Twitter sentiment
   - Check for scam warnings
   - Look for developer communication

5. **Test Transaction**
   - Buy small amount ($10-50)
   - Immediately test sell
   - Verify you can exit position

6. **Ongoing Monitoring**
   - Re-run analysis weekly
   - Watch for holder changes
   - Monitor liquidity

## Troubleshooting

### Common Issues

**"API returned 429" or "Too Many Requests"**
- Free APIs have rate limits
- Wait 1-2 minutes between analyses
- Consider using official Solscan API key for higher limits

**"No holder data available"**
- Token might be brand new
- API might be temporarily down
- Try again in a few minutes

**"Could not fetch token metadata"**
- Verify the token address is correct
- Token might not be indexed yet
- Check if token exists on Solscan.io

**Import errors**
- Make sure you're in the project directory
- Install dependencies: `pip install -r requirements.txt`
- Check Python version (3.7+ required)

## Best Practices

1. **Never Skip Manual Research**
   - Automated tools help, but can't catch everything
   - Always verify team and project legitimacy

2. **Test Sells Before Big Buys**
   - Buy $10-50 worth first
   - Try to sell immediately
   - Confirm transactions go through

3. **Use Multiple Tools**
   - Combine with RugCheck.xyz
   - Check Token Sniffer
   - Review on DEXScreener

4. **Stay Updated**
   - Scam tactics evolve constantly
   - Re-analyze tokens periodically
   - Follow crypto security researchers

5. **Trust Your Gut**
   - If something feels wrong, it probably is
   - No FOMO - there's always another opportunity
   - Better to miss a gain than take a total loss

## Limitations

This tool has limitations:

- Uses free APIs with rate limits
- Cannot fully simulate transactions
- No team background checks (manual task)
- Cannot predict future scams
- Limited contract code analysis

Always combine with manual research and other tools.

## Getting Help

If you encounter issues:

1. Check this examples file
2. Review README.md
3. Verify dependencies are installed
4. Check token address is valid
5. Try with a known token (like USDC) first

---

**Remember**: This tool is for research purposes only. It does NOT provide financial advice. Always do your own research and never invest more than you can afford to lose.
