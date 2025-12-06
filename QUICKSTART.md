# Quick Start Guide

Get started with the Solana Rug Pull Detector in 5 minutes.

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed requests-2.31.0
```

## 2. Run Your First Analysis

Test with USDC (a safe, established token):

```bash
python detect.py EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```

You should see:
```
==================================================================
🔍 SOLANA RUG PULL DETECTOR v1.0
==================================================================
...
Risk Level: LOW
Risk Score: 0-20/100
```

## 3. Analyze a Real Token

Replace with your target token address:

```bash
python detect.py YOUR_TOKEN_ADDRESS_HERE
```

## 4. Read the Report

The tool saves a markdown report:
```
rugpull_report_EPjFWdd5_20250106_143022.md
```

Open it to see:
- Overall risk assessment
- Red flags and warnings
- Detailed analysis
- Recommendations

## 5. Interpret Results

### If Risk is EXTREME or HIGH:
- **DO NOT INVEST**
- Multiple red flags detected
- Likely scam or rug pull

### If Risk is MEDIUM:
- Proceed with caution
- Do additional research
- Check team and project
- Test with small amount first

### If Risk is LOW:
- Fewer red flags detected
- Still perform DYOR
- No guarantee of safety
- Monitor continuously

## Common Commands

### Help
```bash
python detect.py --help
```

### Version
```bash
python detect.py --version
```

### Using Claude Code Slash Command
```
/rugpull TOKEN_ADDRESS
```

## What to Look For

### Critical Red Flags (Avoid!)
- Top holder owns >50%
- No liquidity pools
- <10 holders
- Missing metadata

### Warning Signs (Caution!)
- Top holder owns >15%
- Low holder count (<50)
- Cannot verify lock
- Suspicious trading

### Good Signs
- Holder count >100
- Top holder <10%
- Multiple pools
- Active trading

## Next Steps

1. **Read EXAMPLES.md** - See more use cases
2. **Read README.md** - Full documentation
3. **Practice** - Analyze known tokens first
4. **Combine Tools** - Use with RugCheck.xyz, DEXScreener
5. **Always DYOR** - Never rely on one tool alone

## Example Workflow

```bash
# 1. Find a token on pump.fun or Twitter
# 2. Copy the token address
# 3. Run analysis
python detect.py <TOKEN_ADDRESS>

# 4. Review the report
# 5. Check website and socials
# 6. Verify on Solscan.io
# 7. Test with $10-20 first
# 8. Monitor after buying
```

## Troubleshooting

**Error: "No module named 'requests'"**
→ Run: `pip install -r requirements.txt`

**Error: "API returned 429"**
→ Wait 1-2 minutes (rate limit)

**Error: "Invalid address"**
→ Check token address is correct

**No output**
→ Check internet connection

## Important Reminders

- This is NOT financial advice
- Always do your own research
- Test sells before big buys
- Never invest more than you can lose
- Crypto is extremely high risk

## Getting Help

- Check EXAMPLES.md for detailed examples
- Read README.md for full documentation
- Verify token on Solscan.io manually
- Use multiple analysis tools

---

**Ready to start? Run your first analysis now!**

```bash
python detect.py EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```
