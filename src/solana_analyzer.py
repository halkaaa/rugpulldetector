"""
Solana Rug Pull Detector - Core Analysis Module
Analyzes Solana tokens for security risks using free APIs and public data
"""

import sys
import io

# Fix Windows console encoding for Unicode/emoji support
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import requests
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict


class SolanaRugPullDetector:
    """Main analyzer for Solana token security"""

    def __init__(self):
        # Primary APIs (more reliable, free)
        self.dexscreener_api = "https://api.dexscreener.com/latest/dex"
        self.jupiter_api = "https://api.jup.ag"
        self.jupiter_price_api = "https://api.jup.ag/price/v2"
        self.rugcheck_api = "https://api.rugcheck.xyz/v1"
        self.helius_rpc = "https://api.mainnet-beta.solana.com"

        # Fallback APIs
        self.solscan_api = "https://public-api.solscan.io"
        self.birdeye_api = "https://public-api.birdeye.so"

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
            # 1. Get RugCheck security report (most comprehensive)
            print("🛡️  Fetching RugCheck security analysis...")
            results["rugcheck"] = self._fetch_rugcheck(token_address)

            # 2. Get DexScreener data (liquidity, price, trading)
            print("📈 Fetching DexScreener market data...")
            results["dexscreener"] = self._fetch_dexscreener(token_address)

            # 3. Get token metadata (from DexScreener or fallback)
            print("📋 Fetching token metadata...")
            results["metadata_check"] = self._check_metadata(token_address, results.get("dexscreener"), results.get("rugcheck"))

            # 4. Analyze holder distribution (from RugCheck)
            print("👥 Analyzing holder distribution...")
            results["holder_distribution"] = self._analyze_holders(token_address, results.get("rugcheck"))

            # 5. Check liquidity (from DexScreener)
            print("💧 Checking liquidity...")
            results["liquidity_analysis"] = self._analyze_liquidity(token_address, results.get("dexscreener"))

            # 6. Analyze trading activity (from DexScreener)
            print("📊 Analyzing trading activity...")
            results["trading_activity"] = self._analyze_trading(token_address, results.get("dexscreener"))

            # 7. Contract security checks (from RugCheck)
            print("🔒 Performing contract security checks...")
            results["contract_security"] = self._check_contract_security(token_address, results.get("rugcheck"))

            # 8. Honeypot detection (from RugCheck)
            print("🍯 Running honeypot detection...")
            results["honeypot_detection"] = self._detect_honeypot(token_address, results.get("rugcheck"))

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

    def _fetch_rugcheck(self, token_address: str) -> Dict:
        """Fetch comprehensive security report from RugCheck.xyz"""
        try:
            response = requests.get(
                f"{self.rugcheck_api}/tokens/{token_address}/report",
                headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                self.info.append("✅ RugCheck security data retrieved")
                return data
            else:
                self.warnings.append(f"⚠️ RugCheck API returned status {response.status_code}")
                return {}

        except Exception as e:
            self.warnings.append(f"⚠️ Could not fetch RugCheck data: {str(e)}")
            return {}

    def _fetch_dexscreener(self, token_address: str) -> Dict:
        """Fetch market data from DexScreener"""
        try:
            response = requests.get(
                f"{self.dexscreener_api}/tokens/{token_address}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                pairs = data.get("pairs", [])
                if pairs:
                    self.info.append(f"✅ Found {len(pairs)} trading pair(s) on DexScreener")
                    return {"pairs": pairs, "has_data": True}
                else:
                    self.warnings.append("⚠️ No trading pairs found on DexScreener")
                    return {"pairs": [], "has_data": False}
            else:
                self.warnings.append(f"⚠️ DexScreener API returned status {response.status_code}")
                return {"pairs": [], "has_data": False}

        except Exception as e:
            self.warnings.append(f"⚠️ Could not fetch DexScreener data: {str(e)}")
            return {"pairs": [], "has_data": False}

    def _check_metadata(self, token_address: str, dexscreener_data: Dict = None, rugcheck_data: Dict = None) -> Dict:
        """Check token metadata from available sources"""
        result = {
            "name": "Unknown",
            "symbol": "Unknown",
            "decimals": 0,
            "supply": 0,
            "has_metadata": False
        }

        # Try to get metadata from DexScreener first
        if dexscreener_data and dexscreener_data.get("pairs"):
            pair = dexscreener_data["pairs"][0]
            base_token = pair.get("baseToken", {})
            result["name"] = base_token.get("name", "Unknown")
            result["symbol"] = base_token.get("symbol", "Unknown")
            result["has_metadata"] = True

            if result["name"] != "Unknown":
                self.info.append(f"✅ Token: {result['name']} ({result['symbol']})")

        # Enrich with RugCheck data
        if rugcheck_data:
            if rugcheck_data.get("tokenMeta"):
                meta = rugcheck_data["tokenMeta"]
                if not result["has_metadata"]:
                    result["name"] = meta.get("name", result["name"])
                    result["symbol"] = meta.get("symbol", result["symbol"])
                result["decimals"] = meta.get("decimals", 0)
                result["has_metadata"] = True

            # Get supply from RugCheck
            if rugcheck_data.get("token"):
                result["supply"] = rugcheck_data["token"].get("supply", 0)

        if not result["has_metadata"]:
            self.warnings.append("⚠️ Limited metadata available")

        return result

    def _analyze_holders(self, token_address: str, rugcheck_data: Dict = None) -> Dict:
        """Analyze token holder distribution from RugCheck data"""
        result = {
            "top_holder_percentage": 0,
            "top_5_percentage": 0,
            "top_10_percentage": 0,
            "total_holders": 0,
            "holder_details": []
        }

        if rugcheck_data and rugcheck_data.get("topHolders"):
            holders = rugcheck_data["topHolders"]
            result["total_holders"] = len(holders)

            if holders:
                # Calculate percentages from RugCheck data
                top_holder_pct = holders[0].get("pct", 0) if holders else 0
                top_5_pct = sum(h.get("pct", 0) for h in holders[:5])
                top_10_pct = sum(h.get("pct", 0) for h in holders[:10])

                result["top_holder_percentage"] = round(top_holder_pct, 2)
                result["top_5_percentage"] = round(top_5_pct, 2)
                result["top_10_percentage"] = round(top_10_pct, 2)

                # Store holder details for report
                for h in holders[:5]:
                    result["holder_details"].append({
                        "address": h.get("address", "")[:8] + "...",
                        "percentage": round(h.get("pct", 0), 2),
                        "is_insider": h.get("insider", False)
                    })

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

                # Check for insider concentration
                insider_count = sum(1 for h in holders if h.get("insider", False))
                if insider_count > 3:
                    self.warnings.append(f"⚠️ {insider_count} insider wallets detected in top holders")

                return result

        self.warnings.append("⚠️ Holder distribution data not available")
        return result

    def _analyze_liquidity(self, token_address: str, dexscreener_data: Dict = None) -> Dict:
        """Analyze liquidity from DexScreener data"""
        result = {
            "has_liquidity": False,
            "total_liquidity_usd": 0,
            "pools": [],
            "main_dex": "Unknown"
        }

        if dexscreener_data and dexscreener_data.get("pairs"):
            pairs = dexscreener_data["pairs"]
            result["has_liquidity"] = True

            total_liq = 0
            for pair in pairs[:5]:  # Top 5 pools
                liq = pair.get("liquidity", {}).get("usd", 0) or 0
                total_liq += liq
                result["pools"].append({
                    "dex": pair.get("dexId", "Unknown"),
                    "liquidity_usd": liq,
                    "pair": pair.get("pairAddress", "")[:12] + "..."
                })

            result["total_liquidity_usd"] = total_liq
            result["main_dex"] = pairs[0].get("dexId", "Unknown") if pairs else "Unknown"

            # Analyze liquidity levels
            if total_liq < 1000:
                self.risk_flags.append(f"❌ CRITICAL: Very low liquidity (${total_liq:,.0f})")
            elif total_liq < 10000:
                self.risk_flags.append(f"❌ Low liquidity (${total_liq:,.0f}) - High slippage risk")
            elif total_liq < 50000:
                self.warnings.append(f"⚠️ Moderate liquidity (${total_liq:,.0f})")
            else:
                self.info.append(f"✅ Good liquidity: ${total_liq:,.0f}")

            # Check for Raydium (usually more established)
            dexes = [p.get("dexId", "") for p in pairs]
            if "raydium" in dexes:
                self.info.append("✅ Listed on Raydium")

            return result

        self.risk_flags.append("❌ No liquidity pools found")
        return result

    def _analyze_trading(self, token_address: str, dexscreener_data: Dict = None) -> Dict:
        """Analyze trading activity from DexScreener data"""
        result = {
            "active": False,
            "price_usd": 0,
            "price_change_24h": 0,
            "volume_24h": 0,
            "txns_24h": {"buys": 0, "sells": 0},
            "market_cap": 0,
            "fdv": 0,
            "pair_created": None
        }

        if dexscreener_data and dexscreener_data.get("pairs"):
            pair = dexscreener_data["pairs"][0]  # Main pair
            result["active"] = True

            result["price_usd"] = float(pair.get("priceUsd", 0) or 0)
            result["price_change_24h"] = pair.get("priceChange", {}).get("h24", 0) or 0
            result["volume_24h"] = pair.get("volume", {}).get("h24", 0) or 0
            result["market_cap"] = pair.get("marketCap", 0) or 0
            result["fdv"] = pair.get("fdv", 0) or 0
            result["pair_created"] = pair.get("pairCreatedAt", None)

            # Transaction counts
            txns = pair.get("txns", {}).get("h24", {})
            result["txns_24h"] = {
                "buys": txns.get("buys", 0),
                "sells": txns.get("sells", 0)
            }

            total_txns = result["txns_24h"]["buys"] + result["txns_24h"]["sells"]

            # Analyze trading patterns
            if total_txns < 10:
                self.warnings.append(f"⚠️ Very low trading activity: {total_txns} transactions in 24h")
            elif total_txns < 100:
                self.info.append(f"✅ Moderate activity: {total_txns} transactions in 24h")
            else:
                self.info.append(f"✅ Active trading: {total_txns} transactions in 24h")

            # Check buy/sell ratio
            if result["txns_24h"]["sells"] > 0:
                buy_sell_ratio = result["txns_24h"]["buys"] / result["txns_24h"]["sells"]
                if buy_sell_ratio < 0.3:
                    self.risk_flags.append(f"❌ Heavy selling pressure (buy/sell ratio: {buy_sell_ratio:.2f})")
                elif buy_sell_ratio < 0.7:
                    self.warnings.append(f"⚠️ More sells than buys (ratio: {buy_sell_ratio:.2f})")

            # Check price change
            if result["price_change_24h"] < -50:
                self.risk_flags.append(f"❌ Massive price drop: {result['price_change_24h']:.1f}% in 24h")
            elif result["price_change_24h"] < -20:
                self.warnings.append(f"⚠️ Significant price drop: {result['price_change_24h']:.1f}% in 24h")

            # Check pair age
            if result["pair_created"]:
                created_ms = result["pair_created"]
                age_hours = (datetime.now().timestamp() * 1000 - created_ms) / (1000 * 60 * 60)
                if age_hours < 24:
                    self.warnings.append(f"⚠️ Very new token: created {age_hours:.1f} hours ago")
                elif age_hours < 72:
                    self.info.append(f"✅ Token age: {age_hours:.0f} hours")

            # Volume analysis
            if result["volume_24h"] > 0:
                self.info.append(f"✅ 24h Volume: ${result['volume_24h']:,.0f}")

            return result

        self.warnings.append("⚠️ No trading data available")
        return result

    def _check_contract_security(self, token_address: str, rugcheck_data: Dict = None) -> Dict:
        """Check contract security features from RugCheck data"""
        result = {
            "mint_authority": "UNKNOWN",
            "freeze_authority": "UNKNOWN",
            "mutable_metadata": "UNKNOWN",
            "risks": [],
            "rugcheck_score": None
        }

        if rugcheck_data:
            # Get RugCheck risk score
            score = rugcheck_data.get("score")
            if score is not None and isinstance(score, (int, float)):
                result["rugcheck_score"] = int(score)
                if score >= 800:
                    self.info.append(f"✅ RugCheck score: {score}/1000 (Good)")
                elif score >= 500:
                    self.warnings.append(f"⚠️ RugCheck score: {score}/1000 (Medium)")
                else:
                    self.risk_flags.append(f"❌ RugCheck score: {score}/1000 (Risky)")

            # Check token authorities
            if rugcheck_data.get("token"):
                token = rugcheck_data["token"]

                # Mint authority
                mint_auth = token.get("mintAuthority")
                result["mint_authority"] = "DISABLED" if mint_auth is None else "ENABLED"
                if mint_auth:
                    self.risk_flags.append("❌ Mint authority ENABLED - New tokens can be minted")
                else:
                    self.info.append("✅ Mint authority disabled - Fixed supply")

                # Freeze authority
                freeze_auth = token.get("freezeAuthority")
                result["freeze_authority"] = "DISABLED" if freeze_auth is None else "ENABLED"
                if freeze_auth:
                    self.risk_flags.append("❌ Freeze authority ENABLED - Your tokens can be frozen")
                else:
                    self.info.append("✅ Freeze authority disabled")

            # Check risks from RugCheck
            if rugcheck_data.get("risks"):
                for risk in rugcheck_data["risks"]:
                    risk_name = risk.get("name", "Unknown risk")
                    risk_level = risk.get("level", "unknown")
                    risk_desc = risk.get("description", "")

                    result["risks"].append({
                        "name": risk_name,
                        "level": risk_level,
                        "description": risk_desc
                    })

                    if risk_level in ["danger", "high"]:
                        self.risk_flags.append(f"❌ {risk_name}: {risk_desc}")
                    elif risk_level in ["warning", "medium"]:
                        self.warnings.append(f"⚠️ {risk_name}: {risk_desc}")

            return result

        self.warnings.append("⚠️ Contract security data not available from RugCheck")
        return result

    def _detect_honeypot(self, token_address: str, rugcheck_data: Dict = None) -> Dict:
        """Detect potential honeypot characteristics from RugCheck"""
        result = {
            "is_honeypot": "UNKNOWN",
            "checks_performed": [],
            "transfer_fee": None,
            "can_sell": "UNKNOWN"
        }

        if rugcheck_data:
            # Check for honeypot indicators in RugCheck risks
            risks = rugcheck_data.get("risks", [])
            honeypot_risks = [r for r in risks if "honeypot" in r.get("name", "").lower() or
                            "sell" in r.get("description", "").lower() or
                            "transfer" in r.get("name", "").lower()]

            if honeypot_risks:
                for risk in honeypot_risks:
                    if risk.get("level") in ["danger", "high"]:
                        result["is_honeypot"] = "LIKELY"
                        self.risk_flags.append(f"❌ HONEYPOT RISK: {risk.get('description', 'Cannot sell')}")
                    else:
                        result["is_honeypot"] = "POSSIBLE"
                        self.warnings.append(f"⚠️ Potential issue: {risk.get('description', '')}")

            # Check transfer fee
            transfer_fee = rugcheck_data.get("transferFee")
            if transfer_fee is not None and isinstance(transfer_fee, (int, float)):
                fee = float(transfer_fee)
                result["transfer_fee"] = fee
                if fee > 10:
                    self.risk_flags.append(f"❌ High transfer fee: {fee}%")
                elif fee > 5:
                    self.warnings.append(f"⚠️ Transfer fee: {fee}%")
                elif fee > 0:
                    self.info.append(f"✅ Low transfer fee: {fee}%")

            # Check if markets exist (can trade)
            if rugcheck_data.get("markets"):
                markets = rugcheck_data["markets"]
                if markets:
                    result["can_sell"] = "YES"
                    self.info.append(f"✅ {len(markets)} active market(s) detected")
                else:
                    result["can_sell"] = "UNKNOWN"

            result["checks_performed"] = [
                "RugCheck risk analysis",
                "Transfer fee check",
                "Market availability check"
            ]

            if result["is_honeypot"] == "UNKNOWN":
                result["is_honeypot"] = "UNLIKELY"
                self.info.append("✅ No honeypot indicators detected by RugCheck")

            return result

        result["checks_performed"] = ["Limited - RugCheck data unavailable"]
        self.warnings.append("⚠️ Honeypot check incomplete - ALWAYS test sells with small amounts")
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

"""

    # Trading Activity (Price & Volume)
    if analysis['trading_activity'].get('active'):
        trading = analysis['trading_activity']
        md += f"""### 💰 Price & Market Data

- **Price**: ${trading.get('price_usd', 0):.10f}
- **24h Change**: {trading.get('price_change_24h', 0):.1f}%
- **24h Volume**: ${trading.get('volume_24h', 0):,.0f}
- **Market Cap**: ${trading.get('market_cap', 0):,.0f}
- **FDV**: ${trading.get('fdv', 0):,.0f}
- **24h Buys**: {trading.get('txns_24h', {}).get('buys', 0)}
- **24h Sells**: {trading.get('txns_24h', {}).get('sells', 0)}

"""

    # Holder Distribution
    if analysis['holder_distribution'] and analysis['holder_distribution'].get('top_holder_percentage', 0) > 0:
        holders = analysis['holder_distribution']
        md += f"""### 👥 Holder Distribution

- **Top Holder**: {holders.get('top_holder_percentage', 0)}%
- **Top 5 Holders**: {holders.get('top_5_percentage', 0)}%
- **Top 10 Holders**: {holders.get('top_10_percentage', 0)}%

"""
        # Add top holder details if available
        if holders.get('holder_details'):
            md += "**Top Holders:**\n"
            for h in holders['holder_details']:
                insider_tag = " (insider)" if h.get('is_insider') else ""
                md += f"- `{h.get('address', '')}`: {h.get('percentage', 0)}%{insider_tag}\n"
            md += "\n"

    # Liquidity
    if analysis['liquidity_analysis']:
        liq = analysis['liquidity_analysis']
        md += f"""### 💧 Liquidity Analysis

- **Has Liquidity**: {liq.get('has_liquidity', False)}
- **Total Liquidity**: ${liq.get('total_liquidity_usd', 0):,.0f}
- **Main DEX**: {liq.get('main_dex', 'Unknown')}

"""
        if liq.get('pools'):
            md += "**Pools:**\n"
            for pool in liq['pools'][:3]:
                md += f"- {pool.get('dex', 'Unknown')}: ${pool.get('liquidity_usd', 0):,.0f}\n"
            md += "\n"

    # Contract Security
    if analysis.get('contract_security'):
        security = analysis['contract_security']
        md += f"""### 🔒 Contract Security

- **Mint Authority**: {security.get('mint_authority', 'UNKNOWN')}
- **Freeze Authority**: {security.get('freeze_authority', 'UNKNOWN')}
- **RugCheck Score**: {security.get('rugcheck_score', 'N/A')}/1000

"""

    # Honeypot Detection
    if analysis.get('honeypot_detection'):
        honeypot = analysis['honeypot_detection']
        md += f"""### 🍯 Honeypot Detection

- **Is Honeypot**: {honeypot.get('is_honeypot', 'UNKNOWN')}
- **Can Sell**: {honeypot.get('can_sell', 'UNKNOWN')}
- **Transfer Fee**: {honeypot.get('transfer_fee', 'None') or 'None'}%

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
