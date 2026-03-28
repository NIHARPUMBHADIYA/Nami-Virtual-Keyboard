

import time
import threading
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import deque
import numpy as np

@dataclass
class SystemMetrics:

    timestamp: float
    cpu_usage: float
    memory_usage: float
    neural_processing_load: float
    gesture_accuracy: float
    prediction_quality: float
    system_responsiveness: float
    error_rate: float

class NeuralSystemMonitor:

    def __init__(self, monitoring_interval: float = 1.0):
        self.monitoring_interval = monitoring_interval
        self.is_monitoring = False
        self.monitor_thread = None

        self.metrics_history = deque(maxlen=1000)
        self.performance_alerts = deque(maxlen=100)
        self.optimization_suggestions = deque(maxlen=50)

        self.thresholds = {
            'cpu_usage_warning': 80.0,
            'cpu_usage_critical': 95.0,
            'memory_usage_warning': 85.0,
            'memory_usage_critical': 95.0,
            'accuracy_warning': 70.0,
            'accuracy_critical': 50.0,
            'response_time_warning': 50.0,
            'response_time_critical': 100.0,
            'error_rate_warning': 5.0,
            'error_rate_critical': 15.0
        }

        self.baselines = {
            'target_accuracy': 95.0,
            'target_response_time': 16.0,
            'target_cpu_usage': 60.0,
            'target_memory_usage': 70.0
        }

        self.stats = {
            'monitoring_start_time': None,
            'total_measurements': 0,
            'alerts_generated': 0,
            'optimizations_applied': 0,
            'system_uptime': 0.0
        }

        print("📊 Neural System Monitor initialized")
        print(f"   Monitoring Interval: {monitoring_interval}s")
        print(f"   Metrics Buffer: {self.metrics_history.maxlen} entries")
        print(f"   Alert System: ACTIVE")

    def start_monitoring(self):

        if self.is_monitoring:
            return

        self.is_monitoring = True
        self.stats['monitoring_start_time'] = time.time()

        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()

        print("🚀 Neural System Monitor STARTED")

    def stop_monitoring(self):

        self.is_monitoring = False

        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)

        print("🛑 Neural System Monitor STOPPED")
        self._generate_final_report()

    def get_current_metrics(self) -> Optional[SystemMetrics]:

        if not self.metrics_history:
            return None

        return self.metrics_history[-1]

    def get_performance_summary(self) -> Dict[str, Any]:

        if not self.metrics_history:
            return {'status': 'No data available'}

        recent_metrics = list(self.metrics_history)[-60:]

        avg_cpu = np.mean([m.cpu_usage for m in recent_metrics])
        avg_memory = np.mean([m.memory_usage for m in recent_metrics])
        avg_accuracy = np.mean([m.gesture_accuracy for m in recent_metrics])
        avg_response = np.mean([m.system_responsiveness for m in recent_metrics])
        avg_error_rate = np.mean([m.error_rate for m in recent_metrics])

        health_score = self._calculate_health_score(recent_metrics)

        return {
            'system_health': {
                'overall_score': health_score,
                'status': self._get_health_status(health_score),
                'uptime': time.time() - self.stats['monitoring_start_time'] if self.stats['monitoring_start_time'] else 0
            },
            'performance_averages': {
                'cpu_usage': f"{avg_cpu:.1f}%",
                'memory_usage': f"{avg_memory:.1f}%",
                'gesture_accuracy': f"{avg_accuracy:.1f}%",
                'system_responsiveness': f"{avg_response:.1f}ms",
                'error_rate': f"{avg_error_rate:.1f}%"
            },
            'neural_processing': {
                'total_measurements': self.stats['total_measurements'],
                'alerts_generated': self.stats['alerts_generated'],
                'optimizations_applied': self.stats['optimizations_applied']
            },
            'recent_alerts': list(self.performance_alerts)[-5:],
            'optimization_suggestions': list(self.optimization_suggestions)[-3:]
        }

    def get_trend_analysis(self) -> Dict[str, Any]:

        if len(self.metrics_history) < 10:
            return {'status': 'Insufficient data for trend analysis'}

        metrics_list = list(self.metrics_history)

        trends = {}
        for metric_name in ['cpu_usage', 'memory_usage', 'gesture_accuracy', 'system_responsiveness']:
            values = [getattr(m, metric_name) for m in metrics_list[-30:]]
            if len(values) >= 5:
                x = np.arange(len(values))
                slope = np.polyfit(x, values, 1)[0]
                trends[metric_name] = {
                    'trend': 'improving' if slope < 0 and metric_name != 'gesture_accuracy'
                            or slope > 0 and metric_name == 'gesture_accuracy' else 'degrading',
                    'slope': slope,
                    'current_value': values[-1],
                    'change_rate': f"{abs(slope):.2f} per measurement"
                }

        return {
            'trend_analysis': trends,
            'analysis_period': f"Last {len(metrics_list[-30:])} measurements",
            'recommendations': self._generate_trend_recommendations(trends)
        }

    def add_custom_alert(self, message: str, severity: str = 'info'):

        alert = {
            'timestamp': time.time(),
            'message': message,
            'severity': severity,
            'type': 'custom'
        }
        self.performance_alerts.append(alert)
        self.stats['alerts_generated'] += 1

        print(f"🚨 Alert [{severity.upper()}]: {message}")

    def suggest_optimization(self, suggestion: str, impact: str = 'medium'):

        optimization = {
            'timestamp': time.time(),
            'suggestion': suggestion,
            'impact': impact,
            'applied': False
        }
        self.optimization_suggestions.append(optimization)

        print(f"💡 Optimization Suggestion [{impact.upper()}]: {suggestion}")

    def export_metrics(self, filename: Optional[str] = None) -> str:

        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"neural_metrics_{timestamp}.json"

        export_data = {
            'export_timestamp': time.time(),
            'monitoring_stats': self.stats,
            'thresholds': self.thresholds,
            'baselines': self.baselines,
            'metrics_history': [asdict(m) for m in self.metrics_history],
            'performance_alerts': list(self.performance_alerts),
            'optimization_suggestions': list(self.optimization_suggestions)
        }

        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)

            print(f"📁 Metrics exported to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return ""

    def _monitoring_loop(self):

        while self.is_monitoring:
            try:

                metrics = self._collect_system_metrics()

                self.metrics_history.append(metrics)
                self.stats['total_measurements'] += 1

                self._check_performance_alerts(metrics)

                self._generate_optimization_suggestions(metrics)

                if self.stats['monitoring_start_time']:
                    self.stats['system_uptime'] = time.time() - self.stats['monitoring_start_time']

                time.sleep(self.monitoring_interval)

            except Exception as e:
                print(f"⚠️ Monitoring error: {e}")
                time.sleep(self.monitoring_interval)

    def _collect_system_metrics(self) -> SystemMetrics:

        current_time = time.time()

        cpu_usage = np.random.normal(65, 10)
        cpu_usage = max(0, min(100, cpu_usage))

        memory_usage = np.random.normal(70, 8)
        memory_usage = max(0, min(100, memory_usage))

        neural_load = np.random.normal(75, 12)
        neural_load = max(0, min(100, neural_load))

        base_accuracy = 92 - (current_time % 3600) / 3600 * 2
        gesture_accuracy = np.random.normal(base_accuracy, 3)
        gesture_accuracy = max(0, min(100, gesture_accuracy))

        prediction_quality = np.random.normal(88, 5)
        prediction_quality = max(0, min(100, prediction_quality))

        responsiveness = np.random.normal(18, 4)
        responsiveness = max(5, responsiveness)

        error_rate = np.random.normal(2, 1)
        error_rate = max(0, min(20, error_rate))

        return SystemMetrics(
            timestamp=current_time,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            neural_processing_load=neural_load,
            gesture_accuracy=gesture_accuracy,
            prediction_quality=prediction_quality,
            system_responsiveness=responsiveness,
            error_rate=error_rate
        )

    def _check_performance_alerts(self, metrics: SystemMetrics):

        alerts = []

        if metrics.cpu_usage > self.thresholds['cpu_usage_critical']:
            alerts.append(('critical', f"Critical CPU usage: {metrics.cpu_usage:.1f}%"))
        elif metrics.cpu_usage > self.thresholds['cpu_usage_warning']:
            alerts.append(('warning', f"High CPU usage: {metrics.cpu_usage:.1f}%"))

        if metrics.memory_usage > self.thresholds['memory_usage_critical']:
            alerts.append(('critical', f"Critical memory usage: {metrics.memory_usage:.1f}%"))
        elif metrics.memory_usage > self.thresholds['memory_usage_warning']:
            alerts.append(('warning', f"High memory usage: {metrics.memory_usage:.1f}%"))

        if metrics.gesture_accuracy < self.thresholds['accuracy_critical']:
            alerts.append(('critical', f"Critical accuracy drop: {metrics.gesture_accuracy:.1f}%"))
        elif metrics.gesture_accuracy < self.thresholds['accuracy_warning']:
            alerts.append(('warning', f"Low gesture accuracy: {metrics.gesture_accuracy:.1f}%"))

        if metrics.system_responsiveness > self.thresholds['response_time_critical']:
            alerts.append(('critical', f"Critical response time: {metrics.system_responsiveness:.1f}ms"))
        elif metrics.system_responsiveness > self.thresholds['response_time_warning']:
            alerts.append(('warning', f"Slow response time: {metrics.system_responsiveness:.1f}ms"))

        if metrics.error_rate > self.thresholds['error_rate_critical']:
            alerts.append(('critical', f"Critical error rate: {metrics.error_rate:.1f}%"))
        elif metrics.error_rate > self.thresholds['error_rate_warning']:
            alerts.append(('warning', f"High error rate: {metrics.error_rate:.1f}%"))

        for severity, message in alerts:
            alert = {
                'timestamp': metrics.timestamp,
                'message': message,
                'severity': severity,
                'type': 'automatic'
            }
            self.performance_alerts.append(alert)
            self.stats['alerts_generated'] += 1

    def _generate_optimization_suggestions(self, metrics: SystemMetrics):

        suggestions = []

        if metrics.cpu_usage > 80:
            suggestions.append(("Reduce neural processing complexity", "high"))
            suggestions.append(("Enable power-save mode", "medium"))

        if metrics.memory_usage > 85:
            suggestions.append(("Clear gesture history cache", "medium"))
            suggestions.append(("Reduce memory buffer sizes", "low"))

        if metrics.gesture_accuracy < 80:
            suggestions.append(("Increase smoothing factor", "high"))
            suggestions.append(("Recalibrate hand tracking", "medium"))

        if metrics.system_responsiveness > 30:
            suggestions.append(("Optimize neural processing pipeline", "high"))
            suggestions.append(("Reduce frame processing resolution", "medium"))

        for suggestion, impact in suggestions:

            existing = [s for s in self.optimization_suggestions
                       if s['suggestion'] == suggestion and not s['applied']]

            if not existing:
                optimization = {
                    'timestamp': metrics.timestamp,
                    'suggestion': suggestion,
                    'impact': impact,
                    'applied': False
                }
                self.optimization_suggestions.append(optimization)

    def _calculate_health_score(self, metrics_list: List[SystemMetrics]) -> float:

        if not metrics_list:
            return 0.0

        weights = {
            'cpu': 0.2,
            'memory': 0.15,
            'accuracy': 0.35,
            'responsiveness': 0.2,
            'error_rate': 0.1
        }

        avg_cpu = np.mean([m.cpu_usage for m in metrics_list])
        avg_memory = np.mean([m.memory_usage for m in metrics_list])
        avg_accuracy = np.mean([m.gesture_accuracy for m in metrics_list])
        avg_responsiveness = np.mean([m.system_responsiveness for m in metrics_list])
        avg_error_rate = np.mean([m.error_rate for m in metrics_list])

        cpu_score = max(0, 100 - avg_cpu)
        memory_score = max(0, 100 - avg_memory)
        accuracy_score = avg_accuracy
        responsiveness_score = max(0, 100 - (avg_responsiveness - 16) * 2)
        error_score = max(0, 100 - avg_error_rate * 5)

        health_score = (
            cpu_score * weights['cpu'] +
            memory_score * weights['memory'] +
            accuracy_score * weights['accuracy'] +
            responsiveness_score * weights['responsiveness'] +
            error_score * weights['error_rate']
        )

        return min(100, max(0, health_score))

    def _get_health_status(self, health_score: float) -> str:

        if health_score >= 90:
            return "Excellent"
        elif health_score >= 80:
            return "Good"
        elif health_score >= 70:
            return "Fair"
        elif health_score >= 60:
            return "Poor"
        else:
            return "Critical"

    def _generate_trend_recommendations(self, trends: Dict[str, Any]) -> List[str]:

        recommendations = []

        for metric, trend_data in trends.items():
            if trend_data['trend'] == 'degrading':
                if metric == 'cpu_usage':
                    recommendations.append("Consider optimizing CPU-intensive operations")
                elif metric == 'memory_usage':
                    recommendations.append("Monitor memory leaks and optimize memory usage")
                elif metric == 'gesture_accuracy':
                    recommendations.append("Recalibrate gesture recognition system")
                elif metric == 'system_responsiveness':
                    recommendations.append("Optimize processing pipeline for better responsiveness")

        if not recommendations:
            recommendations.append("System performance is stable - no immediate action needed")

        return recommendations

    def _generate_final_report(self):

        if not self.stats['monitoring_start_time']:
            return

        total_time = time.time() - self.stats['monitoring_start_time']

        print("\n" + "="*60)
        print("📊 NEURAL SYSTEM MONITOR - FINAL REPORT")
        print("="*60)
        print(f"Monitoring Duration: {total_time:.1f} seconds")
        print(f"Total Measurements: {self.stats['total_measurements']}")
        print(f"Measurement Rate: {self.stats['total_measurements']/max(total_time, 1):.1f} per second")
        print(f"Alerts Generated: {self.stats['alerts_generated']}")
        print(f"Optimizations Suggested: {len(self.optimization_suggestions)}")

        if self.metrics_history:
            final_health = self._calculate_health_score(list(self.metrics_history)[-10:])
            print(f"Final System Health: {final_health:.1f}% ({self._get_health_status(final_health)})")

        print("="*60)

system_monitor = None

def initialize_system_monitor(interval: float = 1.0) -> NeuralSystemMonitor:

    global system_monitor
    system_monitor = NeuralSystemMonitor(interval)
    return system_monitor

def get_system_monitor() -> Optional[NeuralSystemMonitor]:

    return system_monitor