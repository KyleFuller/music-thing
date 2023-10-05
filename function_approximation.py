from typing import Callable as _Fn
import math as _math

def linear_interpolate(left: float, right: float, /) -> _Fn[[float], float]:

    def interpolation(mu:float):
        return left * (1 - mu) + right * mu
    
    return interpolation

def quadratic_interpolate(left: float, right: float, righter: float, /) -> _Fn[[float], float]:
    def interpolation(mu: float):

        a = 0.5 * (left - 2 * right + righter)
        b = 0.5 * (righter - left)
        c = right
        
        return a * mu**2 + b * mu + c

    return interpolation

def quadratic_approximate(lefter: float, left: float, right: float, righter: float, /) -> _Fn[[float], float]:
    q_left = quadratic_interpolate(lefter, left, right)
    q_right = quadratic_interpolate(righter, right, left)
    def approximation(mu: float):
        return 0.5*q_left(mu) + 0.5*q_right(1 - mu)
    return approximation


def catmull_rom_interpolate(lefter: float, left: float, right: float, righter: float, /) -> _Fn[[float], float]:
    def interpolation(mu: float):
        mu_sq = mu * mu
        a0 = -0.5*lefter + 1.5*left - 1.5*right + 0.5*righter
        a1 = lefter - 2.5*left + 2*right - 0.5*righter
        a2 = -0.5*lefter + 0.5*right
        a3 = left
        return a0*mu*mu_sq+a1*mu_sq+a2*mu+a3
    return interpolation

def cubic_approximate(lefter: float, left: float, right: float, righter: float, /) -> _Fn[[float], float]:
    cr = catmull_rom_interpolate(lefter, left, right, righter)
    q = quadratic_approximate(lefter, left, right, righter)
    
    def approximation(mu:float):
        return 1/3*cr(mu) + 2/3*q(mu)
    
    return approximation

def approximate_int_input_func_on_float_input(f: _Fn[[int], float], real_index: float, /) -> float:

    left_index = _math.floor(real_index)
    right_index = left_index + 1
    
    mu = real_index - left_index
    
    return cubic_approximate(
        f(left_index - 1), 
        f(left_index), 
        f(right_index), 
        f(right_index + 1)
        )(mu)
