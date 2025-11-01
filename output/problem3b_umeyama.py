def umeyama_alignment(P, Q):
    """
    Closed-form least-squares rigid alignment (Umeyama method).
    Args:
        P: (N,3) source points
        Q: (N,3) target points
    Returns:
        R (3,3), t (3,)
    """
    ### YOUR CODE HERE: compute centroids
    p_bar = P.mean(axis=0)
    q_bar = Q.mean(axis=0)

    ### YOUR CODE HERE: center the data
    P_centered = P - p_bar
    Q_centered = Q - q_bar

    ### YOUR CODE HERE: covariance and SVD
    H = P_centered.T @ Q_centered
    U, S, Vt = np.linalg.svd(H)

    ### YOUR CODE HERE: compute rotation and translation
    V = Vt.T
    D = np.eye(3)
    D[-1, -1] = np.linalg.det(V @ U.T)
    R = V @ D @ U.T
    t = q_bar - R @ p_bar

    return R, t
