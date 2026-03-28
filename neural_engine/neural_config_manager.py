

import json
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
import time

class ConfigurationProfile(Enum):

    MAXIMUM_ACCURACY = "maximum_accuracy"
    BALANCED_PERFORMANCE = "balanced_performance"
    POWER_EFFICIENT = "power_efficient"
    GAMING_MODE = "gaming_mode"
    ACCESSIBILITY = "accessibility"
    CUSTOM = "custom"

@dataclass
class NeuralProcessingConfig:

    smoothing_factor: float = 0.85
    prediction_strength: float = 0.7
    confidence_threshold: float = 0.6
    stability_requirement: float = 0.8

    max_processing_fps: int = 120
    prediction_horizon: int = 5
    learning_rate: float = 0.01
    adaptation_speed: float = 0.1

    confidence_boost: float = 1.2
    neural_enhancement_enabled: bool = True
    adaptive_thresholds: bool = True
    real_time_optimization: bool = True

    memory_bank_size: int = 10000
    gesture_history_size: int = 1000
    pattern_cache_size: int = 500

    pinch_threshold: float = 60.0
    pinch_confirmation_frames: int = 3
    hand_detection_confidence: float = 0.2
    face_detection_confidence: float = 0.5

    position_smoothing_weight: float = 0.4
    velocity_smoothing_weight: float = 0.3
    acceleration_smoothing_weight: float = 0.2

    predictive_cursor: bool = True
    gesture_learning: bool = True
    auto_calibration: bool = True
    performance_monitoring: bool = True

@dataclass
class SystemOptimizationConfig:

    cpu_usage_target: float = 70.0
    memory_usage_target: float = 75.0
    thermal_management: bool = True

    accuracy_target: float = 95.0
    response_time_target: float = 16.0
    error_rate_target: float = 2.0

    auto_quality_adjustment: bool = True
    performance_scaling: bool = True
    load_balancing: bool = True

class NeuralConfigManager:

    def __init__(self, config_file: str = "neural_config.json"):
        self.config_file = config_file
        self.current_profile = ConfigurationProfile.BALANCED_PERFORMANCE

        self.neural_config = NeuralProcessingConfig()
        self.system_config = SystemOptimizationConfig()
        self.custom_configs = {}

        self.config_history = []
        self.performance_feedback = []

        self.profiles = self._initialize_profiles()

        self.load_configuration()

        print("⚙️ Neural Configuration Manager initialized")
        print(f"   Current Profile: {self.current_profile.value}")
        print(f"   Configuration File: {self.config_file}")
        print(f"   Available Profiles: {len(self.profiles)}")

    def _initialize_profiles(self) -> Dict[ConfigurationProfile, Dict[str, Any]]:

        profiles = {}

        profiles[ConfigurationProfile.MAXIMUM_ACCURACY] = {
            'neural': NeuralProcessingConfig(
                smoothing_factor=0.95,
                prediction_strength=0.9,
                confidence_threshold=0.8,
                stability_requirement=0.9,
                max_processing_fps=60,
                prediction_horizon=8,
                learning_rate=0.005,
                confidence_boost=1.5,
                pinch_confirmation_frames=5,
                hand_detection_confidence=0.1,
                position_smoothing_weight=0.6
            ),
            'system': SystemOptimizationConfig(
                cpu_usage_target=85.0,
                memory_usage_target=80.0,
                accuracy_target=98.0,
                response_time_target=20.0,
                auto_quality_adjustment=False
            )
        }

        profiles[ConfigurationProfile.BALANCED_PERFORMANCE] = {
            'neural': NeuralProcessingConfig(),
            'system': SystemOptimizationConfig()
        }

        profiles[ConfigurationProfile.POWER_EFFICIENT] = {
            'neural': NeuralProcessingConfig(
                smoothing_factor=0.7,
                prediction_strength=0.5,
                confidence_threshold=0.5,
                stability_requirement=0.6,
                max_processing_fps=30,
                prediction_horizon=3,
                learning_rate=0.02,
                confidence_boost=1.0,
                memory_bank_size=5000,
                gesture_history_size=500,
                neural_enhancement_enabled=False,
                real_time_optimization=False
            ),
            'system': SystemOptimizationConfig(
                cpu_usage_target=50.0,
                memory_usage_target=60.0,
                accuracy_target=85.0,
                response_time_target=33.0,
                thermal_management=True,
                performance_scaling=True
            )
        }

        profiles[ConfigurationProfile.GAMING_MODE] = {
            'neural': NeuralProcessingConfig(
                smoothing_factor=0.9,
                prediction_strength=0.8,
                confidence_threshold=0.7,
                stability_requirement=0.85,
                max_processing_fps=144,
                prediction_horizon=6,
                learning_rate=0.015,
                confidence_boost=1.3,
                pinch_confirmation_frames=2,
                predictive_cursor=True,
                auto_calibration=True
            ),
            'system': SystemOptimizationConfig(
                cpu_usage_target=80.0,
                memory_usage_target=85.0,
                accuracy_target=92.0,
                response_time_target=12.0,
                auto_quality_adjustment=True,
                load_balancing=True
            )
        }

        profiles[ConfigurationProfile.ACCESSIBILITY] = {
            'neural': NeuralProcessingConfig(
                smoothing_factor=0.98,
                prediction_strength=0.95,
                confidence_threshold=0.4,
                stability_requirement=0.95,
                max_processing_fps=60,
                prediction_horizon=10,
                learning_rate=0.001,
                confidence_boost=2.0,
                pinch_threshold=80.0,
                pinch_confirmation_frames=6,
                hand_detection_confidence=0.05,
                position_smoothing_weight=0.8,
                gesture_learning=True,
                auto_calibration=True
            ),
            'system': SystemOptimizationConfig(
                cpu_usage_target=90.0,
                memory_usage_target=90.0,
                accuracy_target=99.0,
                response_time_target=25.0,
                auto_quality_adjustment=False,
                performance_scaling=False
            )
        }

        return profiles

    def switch_profile(self, profile: ConfigurationProfile) -> bool:

        if profile not in self.profiles:
            print(f"❌ Profile {profile.value} not found")
            return False

        self._save_to_history()

        profile_config = self.profiles[profile]
        self.neural_config = profile_config['neural']
        self.system_config = profile_config['system']
        self.current_profile = profile

        self.save_configuration()

        print(f"✅ Switched to profile: {profile.value}")
        self._print_profile_summary()

        return True

    def create_custom_profile(self, name: str, neural_config: NeuralProcessingConfig,
                            system_config: SystemOptimizationConfig) -> bool:

        if not self._validate_configuration(neural_config, system_config):
            print(f"❌ Invalid configuration for profile: {name}")
            return False

        self.custom_configs[name] = {
            'neural': neural_config,
            'system': system_config,
            'created_at': time.time()
        }

        print(f"✅ Created custom profile: {name}")
        return True

    def load_custom_profile(self, name: str) -> bool:

        if name not in self.custom_configs:
            print(f"❌ Custom profile {name} not found")
            return False

        self._save_to_history()

        custom_config = self.custom_configs[name]
        self.neural_config = custom_config['neural']
        self.system_config = custom_config['system']
        self.current_profile = ConfigurationProfile.CUSTOM

        print(f"✅ Loaded custom profile: {name}")
        return True

    def auto_tune_configuration(self, performance_metrics: Dict[str, float]) -> bool:

        print("🔧 Auto-tuning configuration based on performance...")

        self.performance_feedback.append({
            'timestamp': time.time(),
            'metrics': performance_metrics,
            'config_snapshot': asdict(self.neural_config)
        })

        if len(self.performance_feedback) > 100:
            self.performance_feedback = self.performance_feedback[-50:]

        tuning_applied = False

        if performance_metrics.get('cpu_usage', 0) > self.system_config.cpu_usage_target:
            if self.neural_config.max_processing_fps > 30:
                self.neural_config.max_processing_fps = max(30, self.neural_config.max_processing_fps - 10)
                tuning_applied = True
                print(f"   Reduced max FPS to {self.neural_config.max_processing_fps}")

        if performance_metrics.get('memory_usage', 0) > self.system_config.memory_usage_target:
            if self.neural_config.memory_bank_size > 5000:
                self.neural_config.memory_bank_size = max(5000, self.neural_config.memory_bank_size - 1000)
                tuning_applied = True
                print(f"   Reduced memory bank size to {self.neural_config.memory_bank_size}")

        if performance_metrics.get('accuracy', 100) < self.system_config.accuracy_target:
            if self.neural_config.smoothing_factor < 0.95:
                self.neural_config.smoothing_factor = min(0.95, self.neural_config.smoothing_factor + 0.05)
                tuning_applied = True
                print(f"   Increased smoothing factor to {self.neural_config.smoothing_factor:.2f}")

            if self.neural_config.confidence_threshold > 0.3:
                self.neural_config.confidence_threshold = max(0.3, self.neural_config.confidence_threshold - 0.1)
                tuning_applied = True
                print(f"   Reduced confidence threshold to {self.neural_config.confidence_threshold:.2f}")

        if performance_metrics.get('response_time', 0) > self.system_config.response_time_target:
            if self.neural_config.prediction_horizon > 3:
                self.neural_config.prediction_horizon = max(3, self.neural_config.prediction_horizon - 1)
                tuning_applied = True
                print(f"   Reduced prediction horizon to {self.neural_config.prediction_horizon}")

        if tuning_applied:
            self.save_configuration()
            print("✅ Auto-tuning completed")
        else:
            print("ℹ️ No tuning needed - performance within targets")

        return tuning_applied

    def get_configuration_summary(self) -> Dict[str, Any]:

        return {
            'current_profile': self.current_profile.value,
            'neural_config': asdict(self.neural_config),
            'system_config': asdict(self.system_config),
            'available_profiles': [p.value for p in self.profiles.keys()],
            'custom_profiles': list(self.custom_configs.keys()),
            'config_history_count': len(self.config_history),
            'performance_feedback_count': len(self.performance_feedback)
        }

    def export_configuration(self, filename: Optional[str] = None) -> str:

        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"neural_config_export_{timestamp}.json"

        export_data = {
            'export_timestamp': time.time(),
            'current_profile': self.current_profile.value,
            'neural_config': asdict(self.neural_config),
            'system_config': asdict(self.system_config),
            'custom_configs': self.custom_configs,
            'config_history': self.config_history[-10:],
            'performance_feedback': self.performance_feedback[-20:]
        }

        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)

            print(f"📁 Configuration exported to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return ""

    def import_configuration(self, filename: str) -> bool:

        try:
            with open(filename, 'r') as f:
                import_data = json.load(f)

            if 'neural_config' not in import_data or 'system_config' not in import_data:
                print("❌ Invalid configuration file format")
                return False

            self._save_to_history()

            self.neural_config = NeuralProcessingConfig(**import_data['neural_config'])
            self.system_config = SystemOptimizationConfig(**import_data['system_config'])

            if 'custom_configs' in import_data:
                self.custom_configs.update(import_data['custom_configs'])

            self.current_profile = ConfigurationProfile.CUSTOM
            self.save_configuration()

            print(f"✅ Configuration imported from: {filename}")
            return True

        except Exception as e:
            print(f"❌ Import failed: {e}")
            return False

    def reset_to_defaults(self) -> bool:

        self._save_to_history()

        self.neural_config = NeuralProcessingConfig()
        self.system_config = SystemOptimizationConfig()
        self.current_profile = ConfigurationProfile.BALANCED_PERFORMANCE

        self.save_configuration()

        print("✅ Configuration reset to defaults")
        return True

    def save_configuration(self) -> bool:

        config_data = {
            'current_profile': self.current_profile.value,
            'neural_config': asdict(self.neural_config),
            'system_config': asdict(self.system_config),
            'custom_configs': self.custom_configs,
            'last_updated': time.time()
        }

        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)

            return True
        except Exception as e:
            print(f"❌ Failed to save configuration: {e}")
            return False

    def load_configuration(self) -> bool:

        if not os.path.exists(self.config_file):
            print("ℹ️ No existing configuration file, using defaults")
            return True

        try:
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)

            if 'neural_config' in config_data:
                self.neural_config = NeuralProcessingConfig(**config_data['neural_config'])

            if 'system_config' in config_data:
                self.system_config = SystemOptimizationConfig(**config_data['system_config'])

            if 'custom_configs' in config_data:
                self.custom_configs = config_data['custom_configs']

            if 'current_profile' in config_data:
                try:
                    self.current_profile = ConfigurationProfile(config_data['current_profile'])
                except ValueError:
                    self.current_profile = ConfigurationProfile.CUSTOM

            print("✅ Configuration loaded successfully")
            return True

        except Exception as e:
            print(f"❌ Failed to load configuration: {e}")
            return False

    def _validate_configuration(self, neural_config: NeuralProcessingConfig,
                              system_config: SystemOptimizationConfig) -> bool:

        if not (0.0 <= neural_config.smoothing_factor <= 1.0):
            return False
        if not (0.0 <= neural_config.prediction_strength <= 1.0):
            return False
        if not (0.0 <= neural_config.confidence_threshold <= 1.0):
            return False
        if not (10 <= neural_config.max_processing_fps <= 240):
            return False
        if not (1 <= neural_config.prediction_horizon <= 20):
            return False

        if not (0.0 <= system_config.cpu_usage_target <= 100.0):
            return False
        if not (0.0 <= system_config.memory_usage_target <= 100.0):
            return False
        if not (0.0 <= system_config.accuracy_target <= 100.0):
            return False

        return True

    def _save_to_history(self):

        history_entry = {
            'timestamp': time.time(),
            'profile': self.current_profile.value,
            'neural_config': asdict(self.neural_config),
            'system_config': asdict(self.system_config)
        }

        self.config_history.append(history_entry)

        if len(self.config_history) > 50:
            self.config_history = self.config_history[-25:]

    def _print_profile_summary(self):

        print(f"\n📋 Profile Summary: {self.current_profile.value}")
        print(f"   Smoothing Factor: {self.neural_config.smoothing_factor:.2f}")
        print(f"   Max FPS: {self.neural_config.max_processing_fps}")
        print(f"   Accuracy Target: {self.system_config.accuracy_target:.1f}%")
        print(f"   CPU Target: {self.system_config.cpu_usage_target:.1f}%")
        print(f"   Neural Enhancement: {'ON' if self.neural_config.neural_enhancement_enabled else 'OFF'}")

config_manager = None

def initialize_config_manager(config_file: str = "neural_config.json") -> NeuralConfigManager:

    global config_manager
    config_manager = NeuralConfigManager(config_file)
    return config_manager

def get_config_manager() -> Optional[NeuralConfigManager]:

    return config_manager