"""
Solana Rug Pull Detector - Core Analysis Module
Analyzes Solana tokens for security risks using free APIs and public data
"""

import requests
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict


class SolanaRugPullDetector:
    """Main analyzer for Solana token security"""

    def __init__(self):
        self.solscan_api = "https://public-api.solscan.io"
        self.helius_rpc = "https://api.mainnet-beta.solana.com"
        self.risk_flags = []
        self.warnings = []
        self.info = []

    def analyze_token(self, token_address: str) -> Dict:
        """
        Performs comprehensive security analysis on a Solana token

        Args:
            token_address: The Solana token mint address

        Returns:
            Dictionary containing analysis results across all dimensions
        """
        print(f"🔍 Analyzing token: {token_address}\n")

        results = {
            "token_address": token_address,
            "timestamp": datetime.now().isoformat(),
            "contract_security": {},
            "liquidity_analysis": {},
            "holder_distribution": {},
            "honeypot_detection": {},
            "metadata_check": {},
            "trading_activity": {},
            "overall_risk": "UNKNOWN",
            "risk_score": 0,
            "red_flags": [],
            "warnings": [],
            "green_flags": []
        }

        # Reset flags for new analysis
        self.risk_flags = []
        self.warnings = []
        self.info = []

        try:
            # 1. Get token metadata and basic info
            print("📋 Fetching token metadata...")
            results["metadata_check"] = self._check_metadata(token_address)

            # 2. Analyze holder distribution
            print("👥 Analyzing holder distribution...")
            results["holder_distribution"] = self._analyze_holders(token_address)

            # 3. Check liquidity
            print("💧 Checking liquidity...")
            results["liquidity_analysis"] = self._analyze_liquidity(token_address)

            # 4. Analyze trading activity
            print("📊 Analyzing trading activity...")
            results["trading_activity"] = self._analyze_trading(token_address)

            # 5. Contract security checks
            print("🔒 Performing contract security checks...")
            results["contract_security"] = self._check_contract_security(token_address, results["metadata_check"])

            # 6. Honeypot detection
            print("🍯 Running honeypot detection...")
            results["honeypot_detection"] = self._detect_honeypot(token_address)

            # Calculate overall risk
            results["overall_risk"], results["risk_score"] = self._calculate_risk_score()
            results["red_flags"] = self.risk_flags
            results["warnings"] = self.warnings
            results["green_flags"] = self.info

            print(f"\n✅ Analysis complete!")
            return results

        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")
            results["error"] = str(e)
            return results

    def _check_metadata(self, token_address: str) -> Dict:
        """Check token metadata and basic information"""
        try:
            # Try to get token info from Solscan
            response = requests.get(
                f"{self.solscan_api}/token/meta",
                params={"token": token_address},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()

                result = {
                    "name": data.get("name", "Unknown"),
                    "symbol": data.get("symbol", "Unknown"),
                    "decimals": data.get("decimals", 0),
                    "supply": data.get("supply", 0),
                    "holder_count": data.get("holder", 0),
                    "has_metadata": True
                }

                # Check for red flags in metadata
                if not data.get("name") or data.get("name") == "":
                    self.risk_flags.append("❌ Missing token name")

                if not data.get("symbol") or data.get("symbol") == "":
                    self.risk_flags.append("❌ Missing token symbol")
                else:
                    self.info.append(f"✅ Token name: {data.get('name')} ({data.get('symbol')})")

                # Check holder count
                holder_count = data.get("holder", 0)
                if holder_count < 10:
                    self.risk_flags.append(f"❌ Very few holders: {holder_count}")
                elif holder_count < 50:
                    self.warnings.append(f"⚠️ Low holder count: {holder_count}")
                else:
                    self.info.append(f"✅ Holder count: {holder_count}")

                return result
            else:
                self.warnings.append("⚠️ Could not fetch token metadata from Solscan")
                return {"has_metadata": False, "error": f"API returned {response.status_code}"}

        except Exception as e:
            self.warnings.append(f"⚠️ Error fetching metadata: {str(e)}")
            return {"has_metadata": False, "error": str(e)}

    def _analyze_holders(self, token_address: str) -> Dict:
        """Analyze token holder distribution for concentration risks"""
        try:
            response = requests.get(
                f"{self.solscan_api}/token/holders",
                params={"token": token_address, "offset": 0, "limit": 20},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                holders = data.get("data", [])
                total_supply = data.get("total", 0)

                if not holders:
                    self.risk_flags.append("❌ No holder data available")
                    return {"error": "No holder data"}

                # Calculate concentration
                top_holder_pct = (holders[0].get("amount", 0) / total_supply * 100) if total_supply > 0 else 0
                top_5_pct = sum(h.get("amount", 0) for h in holders[:5]) / total_supply * 100 if total_supply > 0 else 0
                top_10_pct = sum(h.get("amount", 0) for h in holders[:10]) / total_supply * 100 if total_supply > 0 else 0

                result = {
                    "top_holder_percentage": round(top_holder_pct, 2),
                    "top_5_percentage": round(top_5_pct, 2),
                    "top_10_percentage": round(top_10_pct, 2),
                    "total_holders": len(holders)
                }

                # Check for concentration red flags
                if top_holder_pct > 50:
                    self.risk_flags.append(f"❌ EXTREME: Top holder owns {top_holder_pct:.1f}% of supply")
                elif top_holder_pct > 30:
                    self.risk_flags.append(f"❌ HIGH RISK: Top holder owns {top_holder_pct:.1f}% of supply")
                elif top_holder_pct > 15:
                    self.warnings.append(f"⚠️ Top holder owns {top_holder_pct:.1f}% of supply")
                else:
                    self.info.append(f"✅ Top holder owns only {top_holder_pct:.1f}%")

                if top_10_pct > 80:
                    self.risk_flags.append(f"❌ Top 10 holders control {top_10_pct:.1f}% of supply")
                elif top_10_pct > 60:
                    self.warnings.append(f"⚠️ Top 10 holders control {top_10_pct:.1f}% of supply")
                else:
                    self.info.append(f"✅ Top 10 holders: {top_10_pct:.1f}%")

                return result
            else:
                self.warnings.append("⚠️ Could not fetch holder data")
                return {"error": f"API returned {response.status_code}"}

        except Exception as e:
            self.warnings.append(f"⚠️ Error analyzing holders: {str(e)}")
            return {"error": str(e)}

    def _analyze_liquidity(self, token_address: str) -> Dict:
        """Analyze liquidity pools and locks"""
        try:
            # Check for liquidity pools on major DEXes
            # Note: This is a simplified version using available free APIs

            result = {
                "has_liquidity": False,
                "pools_found": [],
                "locked": "UNKNOWN"
            }

            # Try to find pools via Solscan market API
            response = requests.get(
                f"{self.solscan_api}/token/markets",
                params={"token": token_address},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                markets = data.get("data", [])

                if markets:
                    result["has_liquidity"] = True
                    result["pools_found"] = [m.get("market", "") for m in markets[:5]]
                    self.info.append(f"✅ Found {len(markets)} liquidity pool(s)")
                else:
                    self.risk_flags.append("❌ No liquidity pools found")

            else:
                self.warnings.append("⚠️ Could not verify liquidity")

            # Check if this is a pump.fun token (common for new memecoins)
            # pump.fun tokens have specific characteristics
            self.warnings.append("⚠️ Cannot verify liquidity lock status via free APIs")
            result["note"] = "Liquidity lock verification requires premium APIs or manual contract review"

            return result

        except Exception as e:
            self.warnings.append(f"⚠️ Error analyzing liquidity: {str(e)}")
            return {"error": str(e)}

    def _analyze_trading(self, token_address: str) -> Dict:
        """Analyze trading activity for suspicious patterns"""
        try:
            # Get recent transfers to analyze trading patterns
            response = requests.get(
                f"{self.solscan_api}/token/transfer",
                params={"token": token_address, "offset": 0, "limit": 50},
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                transfers = data.get("data", [])

                if not transfers:
                    self.warnings.append("⚠️ No recent trading activity found")
                    return {"active": False}

                # Analyze transfer patterns
                unique_addresses = set()
                transfer_amounts = []

                for transfer in transfers:
                    unique_addresses.add(transfer.get("src", ""))
                    unique_addresses.add(transfer.get("dst", ""))
                    transfer_amounts.append(transfer.get("amount", 0))

                result = {
                    "recent_transfers": len(transfers),
                    "unique_addresses": len(unique_addresses),
                    "active": True
                }

                # Check for suspicious patterns
                if len(unique_addresses) < 5:
                    self.warnings.append(f"⚠️ Very few unique addresses trading: {len(unique_addresses)}")
                else:
                    self.info.append(f"✅ {len(unique_addresses)} unique addresses in recent activity")

                # Check for identical transfer amounts (possible bot/wash trading)
                amount_counts = defaultdict(int)
                for amt in transfer_amounts:
                    amount_counts[amt] += 1

                repeated_amounts = [amt for amt, count in amount_counts.items() if count > 5]
                if repeated_amounts:
                    self.warnings.append(f"⚠️ Suspicious: {len(repeated_amounts)} amounts repeated 5+ times (possible wash trading)")

                return result
            else:
                self.warnings.append("⚠️ Could not fetch trading data")
                return {"error": f"API returned {response.status_code}"}

        except Exception as e:
            self.warnings.append(f"⚠️ Error analyzing trading: {str(e)}")
            return {"error": str(e)}

    def _check_contract_security(self, token_address: str, metadata: Dict) -> Dict:
        """Check contract security features"""
        result = {
            "freeze_authority": "UNKNOWN",
            "mint_authority": "UNKNOWN",
            "verified": False
        }

        # Note: Full contract analysis requires on-chain program inspection
        # With free APIs, we have limited visibility

        # Check if supply is fixed (mint authority should be null)
        supply = metadata.get("supply", 0)
        if supply > 0:
            self.info.append(f"✅ Initial supply: {supply:,.0f}")

        # Warning about limitations
        self.warnings.append("⚠️ Contract security check limited - consider manual verification")
        result["note"] = "Full contract audit requires on-chain program analysis or premium tools"

        # Check for common Solana token program vs custom programs
        result["recommendation"] = "Verify token uses standard SPL Token program, not custom program"

        return result

    def _detect_honeypot(self, token_address: str) -> Dict:
        """Detect potential honeypot characteristics"""
        result = {
            "is_honeypot": "UNKNOWN",
            "checks_performed": []
        }

        # Honeypot detection for Solana is complex and requires:
        # 1. Simulating sells
        # 2. Checking program logs
        # 3. Analyzing transaction patterns

        # With free APIs, we can do basic checks:
        checks = [
            "Transfer history accessible",
            "Holder data available",
            "Liquidity pools visible"
        ]

        result["checks_performed"] = checks
        result["note"] = "Full honeypot testing requires transaction simulation"
        result["recommendation"] = "Test with small amount before large investment"

        self.warnings.append("⚠️ Honeypot detection limited with free APIs - ALWAYS test sells with small amounts")

        return result

    def _calculate_risk_score(self) -> Tuple[str, int]:
        """Calculate overall risk score based on flags"""
        # Risk flags are critical issues
        critical_count = len(self.risk_flags)
        warning_count = len(self.warnings)

        # Calculate score (0-100, higher is riskier)
        score = (critical_count * 20) + (warning_count * 5)
        score = min(score, 100)

        # Determine risk level
        if score >= 60 or critical_count >= 3:
            risk_level = "EXTREME"
        elif score >= 40 or critical_count >= 2:
            risk_level = "HIGH"
        elif score >= 20 or critical_count >= 1:
            risk_level = "MEDIUM"
        elif warning_count >= 3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return risk_level, score


def format_markdown_report(analysis: Dict) -> str:
    """Format analysis results as a markdown report"""

    md = f"""# 🔍 Solana Rug Pull Detector Report

**Token Address**: `{analysis['token_address']}`
**Analysis Date**: {datetime.fromisoformat(analysis['timestamp']).strftime('%Y-%m-%d %H:%M:%S UTC')}

---

## 🎯 Overall Risk Assessment

### Risk Level: **{analysis['overall_risk']}**
**Risk Score**: {analysis['risk_score']}/100

"""

    # Add visual risk indicator
    if analysis['overall_risk'] == "EXTREME":
        md += "```\n🚨🚨🚨 EXTREME DANGER - DO NOT INVEST 🚨🚨🚨\n```\n\n"
    elif analysis['overall_risk'] == "HIGH":
        md += "```\n⛔ HIGH RISK - PROCEED WITH EXTREME CAUTION ⛔\n```\n\n"
    elif analysis['overall_risk'] == "MEDIUM":
        md += "```\n⚠️  MEDIUM RISK - VERIFY CAREFULLY ⚠️\n```\n\n"
    else:
        md += "```\n✅ LOW RISK - Still perform due diligence ✅\n```\n\n"

    # Red Flags Section
    if analysis['red_flags']:
        md += "## 🚩 Critical Red Flags\n\n"
        for flag in analysis['red_flags']:
            md += f"- {flag}\n"
        md += "\n"

    # Warnings Section
    if analysis['warnings']:
        md += "## ⚠️ Warnings\n\n"
        for warning in analysis['warnings']:
            md += f"- {warning}\n"
        md += "\n"

    # Green Flags Section
    if analysis['green_flags']:
        md += "## ✅ Positive Indicators\n\n"
        for flag in analysis['green_flags']:
            md += f"- {flag}\n"
        md += "\n"

    # Detailed Analysis Sections
    md += "---\n\n## 📊 Detailed Analysis\n\n"

    # Metadata
    if analysis['metadata_check'].get('has_metadata'):
        meta = analysis['metadata_check']
        md += f"""### 📋 Token Information

- **Name**: {meta.get('name', 'Unknown')}
- **Symbol**: {meta.get('symbol', 'Unknown')}
- **Decimals**: {meta.get('decimals', 0)}
- **Total Supply**: {meta.get('supply', 0):,.0f}
- **Holder Count**: {meta.get('holder_count', 0):,}

"""

    # Holder Distribution
    if analysis['holder_distribution'] and 'error' not in analysis['holder_distribution']:
        holders = analysis['holder_distribution']
        md += f"""### 👥 Holder Distribution

- **Top Holder**: {holders.get('top_holder_percentage', 0)}%
- **Top 5 Holders**: {holders.get('top_5_percentage', 0)}%
- **Top 10 Holders**: {holders.get('top_10_percentage', 0)}%

"""

    # Liquidity
    if analysis['liquidity_analysis']:
        liq = analysis['liquidity_analysis']
        md += f"""### 💧 Liquidity Analysis

- **Has Liquidity**: {liq.get('has_liquidity', False)}
- **Pools Found**: {len(liq.get('pools_found', []))}
- **Lock Status**: {liq.get('locked', 'Unknown')}

"""

    # Trading Activity
    if analysis['trading_activity'].get('active'):
        trading = analysis['trading_activity']
        md += f"""### 📊 Trading Activity

- **Recent Transfers**: {trading.get('recent_transfers', 0)}
- **Unique Addresses**: {trading.get('unique_addresses', 0)}

"""

    # Recommendations
    md += """---

## 💡 Recommendations

"""

    if analysis['overall_risk'] == "EXTREME":
        md += """
1. **DO NOT INVEST** - Multiple critical red flags detected
2. This token shows characteristics of a potential scam
3. High probability of rug pull or honeypot
4. If you already hold this token, consider exiting immediately with small test transactions first
"""
    elif analysis['overall_risk'] == "HIGH":
        md += """
1. **Exercise extreme caution** - Significant red flags present
2. Conduct additional research on team and project
3. Test sells with very small amounts before larger investments
4. Consider waiting for more holder distribution and liquidity
5. Only invest what you can afford to lose completely
"""
    elif analysis['overall_risk'] == "MEDIUM":
        md += """
1. Perform additional due diligence before investing
2. Verify team identity and project legitimacy
3. Check social media presence and community engagement
4. Test sells with small amounts
5. Monitor holder concentration and liquidity
6. Start with small position if investing
"""
    else:
        md += """
1. Token shows fewer red flags, but still perform DYOR
2. Verify liquidity lock status through official sources
3. Check team background and project roadmap
4. Monitor trading patterns and holder changes
5. Remember: "Low risk" doesn't mean "no risk"
"""

    # Disclaimer
    md += """

---

## ⚠️ Disclaimer

This analysis is for **educational and research purposes only** and does not constitute financial advice.

- The tool uses publicly available data and free APIs with limitations
- Scammers constantly evolve tactics - no tool can guarantee 100% protection
- Always conduct your own research (DYOR)
- Never invest more than you can afford to lose
- Cryptocurrency investments carry extreme risk including total loss
- Test all tokens with small amounts before larger investments

### Data Limitations

This analysis uses free-tier APIs with the following limitations:
- Contract security analysis is basic (full audit requires on-chain inspection)
- Honeypot detection cannot fully simulate transactions
- Liquidity lock status requires manual verification
- Team research not included in automated analysis

### Manual Verification Recommended

1. Check project website and social media
2. Verify team identity (LinkedIn, Twitter)
3. Review smart contract code if available
4. Search for audit reports
5. Check community sentiment
6. Look for similar scam patterns
7. Test sells before buying large amounts

---

**Report Generated by**: Solana Rug Pull Detector v1.0
**Blockchain**: Solana
**Analysis Type**: Automated Multi-Factor Security Scan

"""

    return md


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python solana_analyzer.py <token_address>")
        sys.exit(1)

    token_address = sys.argv[1]

    print("=" * 60)
    print("🔍 SOLANA RUG PULL DETECTOR")
    print("=" * 60)
    print()

    detector = SolanaRugPullDetector()
    results = detector.analyze_token(token_address)

    # Generate report
    report = format_markdown_report(results)

    # Save to file
    filename = f"rugpull_report_{token_address[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n📄 Report saved to: {filename}")
    print("\n" + "=" * 60)
    print(report)
