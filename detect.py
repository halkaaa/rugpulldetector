#!/usr/bin/env python3
"""
Solana Rug Pull Detector - CLI Wrapper
Simple command-line interface for analyzing Solana tokens
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from solana_analyzer import SolanaRugPullDetector, format_markdown_report


def print_banner():
    """Print welcome banner"""
    print()
    print("=" * 70)
    print("🔍 SOLANA RUG PULL DETECTOR v1.0")
    print("=" * 70)
    print("AI-Powered Crypto Security Analysis Tool")
    print("Identifies scams, honeypots, and red flags in Solana tokens")
    print("=" * 70)
    print()


def print_usage():
    """Print usage information"""
    print("USAGE:")
    print("  python detect.py <SOLANA_TOKEN_ADDRESS>")
    print()
    print("EXAMPLE:")
    print("  python detect.py EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
    print()
    print("OPTIONS:")
    print("  -h, --help     Show this help message")
    print("  -v, --version  Show version information")
    print()


def main():
    """Main CLI entry point"""

    # Check for help flag
    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        print_banner()
        print_usage()
        return

    # Check for version flag
    if '-v' in sys.argv or '--version' in sys.argv:
        print("Solana Rug Pull Detector v1.0")
        print("Created with Claude Code")
        return

    # Get token address
    token_address = sys.argv[1]

    # Validate address (basic check - Solana addresses are base58, 32-44 chars)
    if len(token_address) < 32 or len(token_address) > 44:
        print("❌ Error: Invalid Solana token address format")
        print("   Solana addresses should be 32-44 characters long")
        print()
        print_usage()
        return

    # Print banner
    print_banner()

    # Create detector instance
    detector = SolanaRugPullDetector()

    try:
        # Run analysis
        print(f"🎯 Target Token: {token_address}")
        print()
        print("⏳ Starting comprehensive security analysis...")
        print()

        results = detector.analyze_token(token_address)

        # Check for errors
        if "error" in results:
            print(f"\n❌ Analysis failed: {results['error']}")
            return

        # Generate markdown report
        print("\n📝 Generating detailed report...")
        report = format_markdown_report(results)

        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"rugpull_report_{token_address[:8]}_{timestamp}.md"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✅ Report saved to: {filename}")
        print()

        # Print summary
        print("=" * 70)
        print("📊 ANALYSIS SUMMARY")
        print("=" * 70)
        print()
        print(f"Risk Level: {results['overall_risk']}")
        print(f"Risk Score: {results['risk_score']}/100")
        print()

        if results['red_flags']:
            print("🚩 CRITICAL RED FLAGS:")
            for flag in results['red_flags'][:5]:  # Show first 5
                print(f"  {flag}")
            if len(results['red_flags']) > 5:
                print(f"  ... and {len(results['red_flags']) - 5} more (see full report)")
            print()

        if results['overall_risk'] in ['EXTREME', 'HIGH']:
            print("⚠️  WARNING: This token shows significant risk indicators!")
            print("   DO NOT INVEST without thorough additional research")
            print()

        print(f"📄 Full report: {filename}")
        print()
        print("=" * 70)
        print()

        # Ask if user wants to see full report
        print("💡 Tip: Open the markdown file for the complete detailed analysis")
        print()

    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        print()

    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
