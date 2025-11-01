def continuous_jacobians(x, u):
    px, vx, py, vy, phi, omega = x
    T1, T2 = u
    A_c = np.zeros((6, 6))
    B_c = np.zeros((6, 2))

    ######################################################################
    ######################### YOUR CODE HERE #############################
    A_c[0, 1] = 1.0
    A_c[1, 4] = -((T1 + T2) / m) * np.cos(phi)
    A_c[2, 3] = 1.0
    A_c[3, 4] = -((T1 + T2) / m) * np.sin(phi)
    A_c[4, 5] = 1.0

    B_c[1, 0] = -np.sin(phi) / m
    B_c[1, 1] = -np.sin(phi) / m
    B_c[3, 0] = np.cos(phi) / m
    B_c[3, 1] = np.cos(phi) / m
    B_c[5, 0] = -ell / Izz
    B_c[5, 1] = ell / Izz
    ######################################################################

    return A_c, B_c
