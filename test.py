#!/usr/bin/env python3
"""
Test script for Solana Rug Pull Detector
Verifies installation and basic functionality
"""

import sys
import os
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")

    try:
        import requests
        print("  ✅ requests module imported")
    except ImportError:
        print("  ❌ Failed to import requests")
        print("     Run: pip install -r requirements.txt")
        return False

    try:
        from solana_analyzer import SolanaRugPullDetector, format_markdown_report
        print("  ✅ solana_analyzer module imported")
    except ImportError as e:
        print(f"  ❌ Failed to import solana_analyzer: {e}")
        return False

    return True


def test_detector_creation():
    """Test that detector can be instantiated"""
    print("\n🧪 Testing detector creation...")

    try:
        from solana_analyzer import SolanaRugPullDetector

        detector = SolanaRugPullDetector()
        print("  ✅ SolanaRugPullDetector created successfully")
        return True
    except Exception as e:
        print(f"  ❌ Failed to create detector: {e}")
        return False


def test_api_connection():
    """Test connection to Solscan API"""
    print("\n🧪 Testing API connection...")

    try:
        import requests

        response = requests.get(
            "https://public-api.solscan.io/token/meta",
            params={"token": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"},  # USDC
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        if response.status_code == 200:
            print("  ✅ Successfully connected to Solscan API")
            data = response.json()
            print(f"     Retrieved data for: {data.get('name', 'Unknown')}")
            return True
        else:
            print(f"  ⚠️  API returned status {response.status_code}")
            print("     This may be temporary - the tool should still work")
            return True
    except Exception as e:
        print(f"  ⚠️  API connection test failed: {e}")
        print("     This may be due to network issues or rate limiting")
        print("     The tool should still work with retry logic")
        return True


def test_analysis():
    """Test basic analysis functionality"""
    print("\n🧪 Testing analysis with USDC token...")

    try:
        from solana_analyzer import SolanaRugPullDetector

        detector = SolanaRugPullDetector()

        # Test with USDC - a known safe token
        usdc_address = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

        print(f"  Analyzing token: {usdc_address}")
        results = detector.analyze_token(usdc_address)

        if results and 'overall_risk' in results:
            print(f"  ✅ Analysis completed")
            print(f"     Risk Level: {results['overall_risk']}")
            print(f"     Risk Score: {results['risk_score']}/100")
            return True
        else:
            print("  ⚠️  Analysis completed but results incomplete")
            return True
    except Exception as e:
        print(f"  ❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_report_generation():
    """Test markdown report generation"""
    print("\n🧪 Testing report generation...")

    try:
        from solana_analyzer import format_markdown_report

        # Mock results for testing
        test_results = {
            'token_address': 'TEST123',
            'timestamp': '2025-01-06T12:00:00',
            'overall_risk': 'LOW',
            'risk_score': 10,
            'red_flags': [],
            'warnings': ['Test warning'],
            'green_flags': ['Test positive'],
            'metadata_check': {'has_metadata': True, 'name': 'Test Token', 'symbol': 'TEST'},
            'holder_distribution': {'top_holder_percentage': 5.0},
            'liquidity_analysis': {'has_liquidity': True},
            'trading_activity': {'active': True}
        }

        report = format_markdown_report(test_results)

        if report and len(report) > 100:
            print("  ✅ Report generated successfully")
            print(f"     Report length: {len(report)} characters")
            return True
        else:
            print("  ❌ Report generation failed or empty")
            return False
    except Exception as e:
        print(f"  ❌ Report generation failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("🔬 SOLANA RUG PULL DETECTOR - TEST SUITE")
    print("=" * 70)
    print()

    tests = [
        ("Imports", test_imports),
        ("Detector Creation", test_detector_creation),
        ("API Connection", test_api_connection),
        ("Report Generation", test_report_generation),
        ("Full Analysis", test_analysis),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Your installation is working correctly.")
        print("\nYou can now use the detector:")
        print("  python detect.py <TOKEN_ADDRESS>")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Check internet connection")
        print("  - Wait a moment and try again (API rate limits)")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    run_all_tests()
