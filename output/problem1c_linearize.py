def linearize_about(x_ref, u_ref, dt=dt_default):
    """
    Affine first-order discrete-time expansion about (x_ref, u_ref):
        x_ref{t+1} ~= f_d(x_ref,u_ref) + A_t (x_ref) + B_t (u_ref)
    """
    A_c, B_c = continuous_jacobians(x_ref, u_ref)
    ######################################################################
    ######################### YOUR CODE HERE #############################
    A_t, B_t = discrete_jacobians(A_c, B_c, dt)
    x_next_ref = f_discrete(x_ref, u_ref, dt)
    ######################################################################

    return A_t, B_t, x_next_ref
