"""
Lightweight ML-based ranking for recommendations (Phase 2).

Uses a tiny linear regression model trained on synthetic samples to compute
priority scores without external dependencies.
"""

from __future__ import annotations

from typing import List, Tuple
from .models import Recommendation, AuditContext, DifficultyLevel, ImpactLevel


def _difficulty_score(level: DifficultyLevel) -> float:
    return {
        DifficultyLevel.EASY: 1.0,
        DifficultyLevel.MEDIUM: 0.7,
        DifficultyLevel.HARD: 0.4,
    }.get(level, 0.5)


def _impact_score(level: ImpactLevel) -> float:
    return {
        ImpactLevel.HIGH: 1.0,
        ImpactLevel.MEDIUM: 0.6,
        ImpactLevel.LOW: 0.3,
    }.get(level, 0.4)


def _train_linear_model() -> List[float]:
    """
    Train a tiny linear regression model on synthetic samples.

    Features: [1, saving_pct, co2_savings_tonnes, difficulty_score, impact_score]
    Target: composite priority score (synthetic)
    """
    # Synthetic training data (small, deterministic)
    # (saving_pct, co2_savings, difficulty_score, impact_score, target_score)
    samples = [
        (12.0, 120.0, 1.0, 1.0, 0.95),
        (8.0, 60.0, 0.7, 0.6, 0.70),
        (4.0, 20.0, 1.0, 0.6, 0.55),
        (15.0, 200.0, 0.4, 1.0, 0.80),
        (3.0, 8.0, 1.0, 0.3, 0.35),
        (10.0, 90.0, 0.7, 1.0, 0.82),
    ]

    # Build X and y
    X = []
    y = []
    for saving_pct, co2_savings, diff, impact, target in samples:
        X.append([1.0, saving_pct, co2_savings, diff, impact])
        y.append(target)

    # Solve (X^T X + lambda I) w = X^T y (ridge for stability)
    lam = 1e-6
    XtX = _mat_mul(_transpose(X), X)
    for i in range(len(XtX)):
        XtX[i][i] += lam
    Xty = _mat_vec_mul(_transpose(X), y)
    w = _solve_linear_system(XtX, Xty)
    return w


def _score_recommendation(rec: Recommendation, weights: List[float]) -> float:
    features = [
        1.0,
        rec.estimated_saving_pct,
        rec.co2_savings_tonnes,
        _difficulty_score(rec.difficulty),
        _impact_score(rec.impact_level),
    ]
    return sum(w * x for w, x in zip(weights, features))


def rank_recommendations_ml(
    recommendations: List[Recommendation],
    context: AuditContext
) -> List[Recommendation]:
    """
    Rank recommendations using a lightweight ML-based score.
    Falls back to the input order if training fails.
    """
    if not recommendations:
        return recommendations

    try:
        weights = _train_linear_model()
    except Exception:
        return recommendations

    scored: List[Tuple[Recommendation, float]] = []
    for rec in recommendations:
        score = _score_recommendation(rec, weights)
        scored.append((rec, score))

    scored.sort(key=lambda item: item[1], reverse=True)
    return [rec for rec, _ in scored]


def _transpose(mat: List[List[float]]) -> List[List[float]]:
    return [list(row) for row in zip(*mat)]


def _mat_mul(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    result = [[0.0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for k in range(len(b)):
            for j in range(len(b[0])):
                result[i][j] += a[i][k] * b[k][j]
    return result


def _mat_vec_mul(a: List[List[float]], v: List[float]) -> List[float]:
    result = [0.0 for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(v)):
            result[i] += a[i][j] * v[j]
    return result


def _solve_linear_system(a: List[List[float]], b: List[float]) -> List[float]:
    """Solve Ax = b via Gauss-Jordan elimination (small matrices only)."""
    n = len(a)
    # Augment matrix
    aug = [row[:] + [b[i]] for i, row in enumerate(a)]

    for col in range(n):
        # Pivot
        pivot = aug[col][col]
        if abs(pivot) < 1e-9:
            # Find a row to swap
            for r in range(col + 1, n):
                if abs(aug[r][col]) > 1e-9:
                    aug[col], aug[r] = aug[r], aug[col]
                    pivot = aug[col][col]
                    break
        if abs(pivot) < 1e-9:
            raise ValueError("Singular matrix")

        # Normalize row
        for j in range(col, n + 1):
            aug[col][j] /= pivot

        # Eliminate others
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            for j in range(col, n + 1):
                aug[r][j] -= factor * aug[col][j]

    return [aug[i][-1] for i in range(n)]
