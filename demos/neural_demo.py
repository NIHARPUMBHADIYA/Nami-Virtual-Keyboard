

import time
import numpy as np
from typing import Dict, Any

from ..neural_engine.nami_neural_engine import initialize_neural_engine, NeuralProcessingMode
from ..neural_engine.neural_config_manager import initialize_config_manager, ConfigurationProfile
from ..neural_engine.neural_system_monitor import initialize_system_monitor

def print_demo_banner():

    print()

def simulate_gesture_data(frame_count: int) -> tuple:

    angle = (frame_count * 0.1) % (2 * np.pi)
    center_x, center_y = 640, 360
    radius = 100 + 50 * np.sin(frame_count * 0.05)

    noise_x = np.random.normal(0, 2)
    noise_y = np.random.normal(0, 2)

    index_x = int(center_x + radius * np.cos(angle) + noise_x)
    index_y = int(center_y + radius * np.sin(angle) + noise_y)

    thumb_x = index_x + 20 + int(10 * np.sin(frame_count * 0.2))
    thumb_y = index_y + 15 + int(10 * np.cos(frame_count * 0.2))

    near_face = (frame_count % 100) < 10

    return ((index_x, index_y), (thumb_x, thumb_y), near_face)

def demo_neural_processing():

    print("🧠 Neural Processing Demo")
    print("=" * 50)

    neural_engine = initialize_neural_engine(NeuralProcessingMode.ADAPTIVE)
    neural_engine.start()

    print("Processing 100 simulated gestures...")

    processing_times = []
    accuracy_scores = []

    for frame in range(100):
        start_time = time.time()

        hand_data = simulate_gesture_data(frame)

        result = neural_engine.process_gesture(hand_data, (720, 1280))

        processing_time = (time.time() - start_time) * 1000
        processing_times.append(processing_time)

        if result['neural_enhanced']:
            accuracy_scores.append(result['confidence'] * 100)

        if frame % 20 == 0:
            print(f"   Frame {frame}: {processing_time:.2f}ms, Confidence: {result.get('confidence', 0):.2%}")

    avg_processing_time = np.mean(processing_times)
    avg_accuracy = np.mean(accuracy_scores) if accuracy_scores else 0

    print(f"\n📊 Neural Processing Results:")
    print(f"   Average Processing Time: {avg_processing_time:.2f}ms")
    print(f"   Average Accuracy: {avg_accuracy:.1f}%")
    print(f"   Neural Enhancements: {len(accuracy_scores)}/100")

    neural_engine.stop()
    return avg_processing_time, avg_accuracy

def demo_configuration_profiles():

    print("\n⚙️ Configuration Profiles Demo")
    print("=" * 50)

    config_manager = initialize_config_manager()

    profiles = [
        ConfigurationProfile.BALANCED_PERFORMANCE,
        ConfigurationProfile.MAXIMUM_ACCURACY,
        ConfigurationProfile.GAMING_MODE,
        ConfigurationProfile.POWER_EFFICIENT
    ]

    for profile in profiles:
        print(f"\n🔄 Switching to {profile.value}...")

        start_time = time.time()
        success = config_manager.switch_profile(profile)
        switch_time = (time.time() - start_time) * 1000

        if success:
            config = config_manager.get_configuration_summary()
            neural_config = config['neural_config']

            print(f"   ✅ Switch completed in {switch_time:.2f}ms")
            print(f"   Smoothing Factor: {neural_config['smoothing_factor']:.2f}")
            print(f"   Max FPS: {neural_config['max_processing_fps']}")
            print(f"   Confidence Threshold: {neural_config['confidence_threshold']:.2f}")
        else:
            print(f"   ❌ Switch failed")

def demo_system_monitoring():

    print("\n📊 System Monitoring Demo")
    print("=" * 50)

    monitor = initialize_system_monitor(0.5)
    monitor.start_monitoring()

    print("Monitoring system for 10 seconds...")

    time.sleep(10)

    summary = monitor.get_performance_summary()

    print(f"\n📈 Monitoring Results:")
    print(f"   System Health: {summary['system_health']['overall_score']:.1f}% ({summary['system_health']['status']})")
    print(f"   Uptime: {summary['system_health']['uptime']:.1f}s")
    print(f"   Total Measurements: {summary['neural_processing']['total_measurements']}")
    print(f"   Alerts Generated: {summary['neural_processing']['alerts_generated']}")

    print(f"\n📊 Performance Averages:")
    for metric, value in summary['performance_averages'].items():
        print(f"   {metric.replace('_', ' ').title()}: {value}")

    trends = monitor.get_trend_analysis()
    if 'trend_analysis' in trends:
        print(f"\n📈 Trend Analysis:")
        for metric, trend_data in trends['trend_analysis'].items():
            print(f"   {metric.replace('_', ' ').title()}: {trend_data['trend']} ({trend_data['change_rate']})")

    monitor.stop_monitoring()

def demo_neural_insights():

    print("\n🔍 Neural Insights Demo")
    print("=" * 50)

    neural_engine = initialize_neural_engine(NeuralProcessingMode.PRECISION)
    neural_engine.start()

    for i in range(50):
        hand_data = simulate_gesture_data(i)
        neural_engine.process_gesture(hand_data, (720, 1280))
        time.sleep(0.01)

    insights = neural_engine.get_neural_insights()

    print(f"🧠 Neural Engine Status: {insights['engine_status']}")
    print(f"📊 Processing Mode: {insights['processing_mode']}")

    print(f"\n⚡ Real-time Metrics:")
    for metric, value in insights['real_time_metrics'].items():
        print(f"   {metric.replace('_', ' ').title()}: {value}")

    print(f"\n📈 Performance Stats:")
    for stat, value in insights['performance_stats'].items():
        print(f"   {stat.replace('_', ' ').title()}: {value}")

    print(f"\n💾 Memory Usage:")
    for usage, value in insights['memory_usage'].items():
        print(f"   {usage.replace('_', ' ').title()}: {value}")

    neural_engine.stop()

def demo_performance_comparison():

    print("\n🏁 Performance Comparison Demo")
    print("=" * 50)

    modes = [
        NeuralProcessingMode.POWER_SAVE,
        NeuralProcessingMode.PERFORMANCE,
        NeuralProcessingMode.PRECISION
    ]

    results = {}

    for mode in modes:
        print(f"\n🔄 Testing {mode.value} mode...")

        neural_engine = initialize_neural_engine(mode)
        neural_engine.start()

        processing_times = []

        for i in range(30):
            start_time = time.time()
            hand_data = simulate_gesture_data(i)
            result = neural_engine.process_gesture(hand_data, (720, 1280))
            processing_time = (time.time() - start_time) * 1000
            processing_times.append(processing_time)

        avg_time = np.mean(processing_times)
        results[mode.value] = avg_time

        print(f"   Average Processing Time: {avg_time:.2f}ms")

        neural_engine.stop()
        time.sleep(0.5)

    print(f"\n🏆 Performance Comparison Results:")
    print("=" * 40)
    for mode, avg_time in sorted(results.items(), key=lambda x: x[1]):
        print(f"   {mode.replace('_', ' ').title()}: {avg_time:.2f}ms")

def main():

    print_demo_banner()

    try:

        demo_neural_processing()
        demo_configuration_profiles()
        demo_system_monitoring()
        demo_neural_insights()
        demo_performance_comparison()

        print("\n" + "=" * 70)
        print("🎉 Nami Neural Engine Demo Complete!")
        print("=" * 70)
        print("✅ Neural processing capabilities demonstrated")
        print("✅ Configuration profiles showcased")
        print("✅ System monitoring validated")
        print("✅ Performance analysis completed")
        print("\n🚀 Ready to experience the future of gesture recognition!")

    except KeyboardInterrupt:
        print("\n\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()