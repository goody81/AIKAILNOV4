"""
Test suite for AIEngine
"""

import pytest
from src.core.ai_engine import AIEngine


class TestAIEngine:
    """Test cases for AIEngine class."""
    
    @pytest.fixture
    def ai_engine(self):
        """Create an AI engine instance for testing."""
        config = {
            'ai': {
                'enabled': True,
                'confidence_threshold': 0.75
            }
        }
        return AIEngine(config)
    
    @pytest.fixture
    def sample_scan_results(self):
        """Create sample scan results."""
        return {
            'target': '192.168.1.100',
            'hosts': [
                {
                    'ip': '192.168.1.100',
                    'state': 'up',
                    'open_ports': [
                        {'port': 80, 'service': 'http'},
                        {'port': 443, 'service': 'https'}
                    ]
                }
            ],
            'total_open_ports': 2,
            'vulnerabilities': [
                {
                    'severity': 'medium',
                    'service': 'http',
                    'description': 'Unencrypted HTTP detected'
                }
            ]
        }
    
    def test_ai_engine_initialization(self, ai_engine):
        """Test AI engine initialization."""
        assert ai_engine is not None
        assert ai_engine.enabled is True
    
    def test_analyze_basic_mode(self, ai_engine, sample_scan_results):
        """Test basic analysis mode."""
        result = ai_engine.analyze(sample_scan_results, mode='basic')
        
        assert 'risk_score' in result
        assert 'risk_level' in result
        assert 'recommendations' in result
        assert isinstance(result['risk_score'], float)
    
    def test_risk_score_calculation(self, ai_engine, sample_scan_results):
        """Test risk score calculation."""
        score = ai_engine._calculate_risk_score(sample_scan_results)
        
        assert isinstance(score, float)
        assert 0.0 <= score <= 10.0
    
    def test_risk_level_determination(self, ai_engine):
        """Test risk level categorization."""
        assert ai_engine._determine_risk_level(1.0) == 'minimal'
        assert ai_engine._determine_risk_level(3.0) == 'low'
        assert ai_engine._determine_risk_level(5.0) == 'medium'
        assert ai_engine._determine_risk_level(7.0) == 'high'
        assert ai_engine._determine_risk_level(9.0) == 'critical'
    
    def test_threat_identification(self, ai_engine, sample_scan_results):
        """Test threat category identification."""
        threats = ai_engine._identify_threats(sample_scan_results)
        
        assert isinstance(threats, list)
    
    def test_recommendations_generation(self, ai_engine, sample_scan_results):
        """Test recommendation generation."""
        recommendations = ai_engine._generate_recommendations(sample_scan_results)
        
        assert isinstance(recommendations, list)
        if recommendations:
            assert 'title' in recommendations[0]
            assert 'priority' in recommendations[0]
