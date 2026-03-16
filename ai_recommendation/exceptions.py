"""
Custom exceptions for the AI recommendation engine.
"""

class RecommendationEngineError(Exception):
    """Base exception for recommendation engine"""
    pass


class InsufficientDataError(RecommendationEngineError):
    """Raised when required data is missing"""
    pass


class InvalidContextError(RecommendationEngineError):
    """Raised when audit context is invalid"""
    pass


class RuleEvaluationError(RecommendationEngineError):
    """Raised when a rule fails to evaluate"""
    pass