from typing import Callable as _Fn
import math as _math

def linear_interpolate(left: float, right: float, /) -> _Fn[[float], float]:
    """
    Takes the value on the left and right and returns a linear function that interpolates between them at a given 
    fraction mu along from the left point toward the right point.  mu < 0 or mu > 1 gives extrapolation.
    """
    def interpolation(mu:float):
        return left * (1 - mu) + right * mu
    
    return interpolation

def quadratic_interpolate(left: float, right: float, righter: float, /) -> _Fn[[float], float]:
    """
    Works similarly to quadratic approximate, but the returned function is guaranteed to interpolate through the input
    values, at the cost of worse overall convergence.

    Produces asymptotically faster convergence as linear_interpolate.
    """
    def interpolation(mu: float):

        a = 0.5 * (left - 2 * right + righter)
        b = 0.5 * (righter - left)
        c = right
        
        return a * mu**2 + b * mu + c

    return interpolation

def quadratic_approximate(lefter: float, left: float, right: float, righter: float, /) -> _Fn[[float], float]:
    """
    Takes a value on the left, a value on the right, and a value one more step to the right from there, and returns a 
    quadratic approximation function where the input mu determines a potentially fractional or negative number of steps 
    from the left at which to approximate.

    Produces asymptotically faster convergence than quadratic_interpolate, and has the same rate of convergence as 
    catmull_rom_interpolate, although it does not interpolate through all four points provided.
    """
    q_left = quadratic_interpolate(lefter, left, right)
    q_right = quadratic_interpolate(righter, right, left)
    def approximation(mu: float):
        return 0.5*q_left(mu) + 0.5*q_right(1 - mu)
    return approximation


def catmull_rom_interpolate(lefter: float, left: float, right: float, righter: float, /) -> _Fn[[float], float]:
    """
    Takes four values at equally spaced steps and returns a function that interpolates through all of them, where the 
    input to the interpolant is the possibly fractional or negative number of steps from the left at which to interpolate.

    Produces asymptotically faster convergence than quadratic_interpolate, and the same rate of 
    convergence as quadratic_approximate.
    """
    def interpolation(mu: float):
        mu_sq = mu * mu
        a0 = -0.5*lefter + 1.5*left - 1.5*right + 0.5*righter
        a1 = lefter - 2.5*left + 2*right - 0.5*righter
        a2 = -0.5*lefter + 0.5*right
        a3 = left
        return a0*mu*mu_sq+a1*mu_sq+a2*mu+a3
    return interpolation

def cubic_approximate(lefter: float, left: float, right: float, righter: float, /) -> _Fn[[float], float]:
    """
    Takes four values at equally spaced steps and returns a function that approximate through all of them, where the 
    input to the approximation function is the possibly fractional or negative number of steps from the left at which 
    to approximate.  This function might actually interpolate between the four points given, but we haven't yet bothered
    to prove this to be the case.  

    This method of approximation seems to produce asymptotically faster convergence than catmull_rom_interpolate or
    quadratic_approximate.
    """
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
