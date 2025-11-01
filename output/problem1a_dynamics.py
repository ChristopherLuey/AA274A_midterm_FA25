def f_continuous(x, u):
    ######################################################################
    ######################### YOUR CODE HERE #############################
    # Write the continuous dynamics for the planar drone
    T1, T2 = u
    px, vx, py, vy, phi, omega = x
    thrust_sum = T1 + T2
    dx = np.zeros_like(x, dtype=float)
    dx[0] = vx
    dx[1] = -(thrust_sum / m) * np.sin(phi)
    dx[2] = vy
    dx[3] = (thrust_sum / m) * np.cos(phi) - g
    dx[4] = omega
    dx[5] = ((T2 - T1) * ell) / Izz
    ######################################################################
    return dx

def f_discrete(x, u, dt=dt_default):
    ######################################################################
    ######################### YOUR CODE HERE #############################
    # Write the discrete dynamics for the planar drone
    dx = x + dt * f_continuous(x, u)
    ######################################################################
    return dx
