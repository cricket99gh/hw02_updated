
"""
Cryptographically Secure Distribution Functions
CPE 486/586 Homework 2
"""

import secrets
import math
import numpy as np
from typing import Union

def uniform(a: float = 0.0, b: float = 1.0) -> float:
    """
    Generate cryptographically secure uniform random sample in [a, b)
    
    Args:
        a: Lower bound (inclusive)
        b: Upper bound (exclusive)
        
    Returns:
        Random float uniformly distributed in [a, b)
    """
    # 53 random bits gives 53-bit precision for double
    u = secrets.randbits(53) / (1 << 53)  # in [0, 1)
    return a + (b - a) * u

def exponentialdist(lambd: float) -> float:
    """
    Generate cryptographically secure exponential random sample
    
    Args:
        lambd: Rate parameter (λ > 0)
        
    Returns:
        Random float exponentially distributed with rate λ
    """
    if lambd <= 0:
        raise ValueError("Lambda must be positive")
    
    u = uniform(0.0, 1.0)  # Use our secure uniform function
    return -math.log(u) / lambd

def poissondist(lambd: float) -> int:
    """
    Generate cryptographically secure Poisson random sample
    
    Args:
        lambd: Mean parameter (λ > 0)
        
    Returns:
        Random integer Poisson distributed with mean λ
    """
    if lambd <= 0:
        raise ValueError("Lambda must be positive")
    
    # Inverse transform sampling for discrete distribution
    u = uniform(0.0, 1.0)  # Generate uniform random number
    k = 0
    p = math.exp(-lambd)  # P(X = 0)
    F = p  # Cumulative probability
    
    # Find smallest k such that F(k) >= u
    while u > F:
        k += 1
        p = p * lambd / k  # P(X = k) using recurrence relation
        F += p
    
    return k

def generate_samples(distribution: str, params: dict, n: int = 1000) -> list:
    """
    Generate multiple samples from specified distribution
    
    Args:
        distribution: 'uniform', 'exponential', or 'poisson'
        params: Dictionary of parameters for the distribution
        n: Number of samples to generate
        
    Returns:
        List of generated samples
    """
    samples = []
    
    if distribution == 'uniform':
        a = params.get('a', 0.0)
        b = params.get('b', 1.0)
        for _ in range(n):
            samples.append(uniform(a, b))
            
    elif distribution == 'exponential':
        lambd = params.get('lambd', 1.0)
        for _ in range(n):
            samples.append(exponentialdist(lambd))
            
    elif distribution == 'poisson':
        lambd = params.get('lambd', 1.0)
        for _ in range(n):
            samples.append(poissondist(lambd))
            
    else:
        raise ValueError("Unsupported distribution")
    
    return samples
