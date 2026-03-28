

import sys
import argparse
import time

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.gesture_app import GestureKeyboardApp

try:
    from demos.neural_demo import main as neural_demo_main
    NEURAL_DEMO_AVAILABLE = True
except ImportError:
    NEURAL_DEMO_AVAILABLE = False

def print_startup_banner():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║    🧠 VR-LEVEL PRECISION GESTURE KEYBOARD + NAMI NEURAL ENGINE 🧠    ║
║                                                                      ║
║              Advanced AI-Powered Gesture Recognition                 ║
║                    Neural Engine Always Active                       ║
╚══════════════════════════════════════════════════════════════════════╝
    """)

def setup_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="VR-Level Precision Gesture Keyboard with Integrated Nami Neural Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Run with integrated neural engine
  python main.py --demo                           # Run neural engine demo
  python main.py --debug                          # Run with debug information
        """
    )

    parser.add_argument(
        '--demo',
        action='store_true',
        help='Run neural engine demonstration'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode with verbose output'
    )

    return parser

def run_neural_demo():
    if NEURAL_DEMO_AVAILABLE:
        print("🧠 Starting Neural Engine Demo...")
        neural_demo_main()
    else:
        print("❌ Neural demo not available")
        print("   Demo components may not be installed")

def main():

    parser = setup_argument_parser()
    args = parser.parse_args()

    if args.demo:
        run_neural_demo()
        return

    print_startup_banner()

    try:

        print("🧠 Starting VR Gesture Keyboard with Integrated Neural Engine...")
        print("   Neural processing is seamlessly integrated and always active")

        if args.debug:
            print("\n🔍 Debug mode enabled - verbose output active")

        app = GestureKeyboardApp()
        app.run()

    except KeyboardInterrupt:
        print("\n\n⚠️ Application interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
    finally:
        print("\n👋 Thank you for using Nami Neural Gesture Keyboard!")
        print("   Powered by integrated Nami Neural Engine 🧠")

if __name__ == "__main__":
    main()