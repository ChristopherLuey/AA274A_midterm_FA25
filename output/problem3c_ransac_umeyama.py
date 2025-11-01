def ransac_umeyama(P, Q, correspondences, tau=0.02, n_iter=200):
    """
    Robust Umeyama alignment using RANSAC.

    Args:
        P, Q: source and target point clouds (N,3)
        correspondences: (N,2) index pairs
        tau: inlier threshold
        n_iter: number of RANSAC iterations
    Returns:
        best_R, best_t, best_inliers
    """

    N = correspondences.shape[0]
    best_R = np.eye(3)
    best_t = np.zeros(3)
    best_inliers = np.zeros(N, dtype=bool)
    best_rmse = np.inf
    rng = np.random.default_rng(SEED_REG)

    P_corr = P[correspondences[:, 0]]
    Q_corr = Q[correspondences[:, 1]]

    for _ in range(n_iter):
        # === TODO(c1): randomly sample 3 correspondence pairs ===
        for _ in range(100):
            idx = rng.choice(N, size=SAMPLE_SIZE, replace=False)
            Ps = P_corr[idx]
            Qs = Q_corr[idx]
            area = np.linalg.norm(np.cross(Ps[1] - Ps[0], Ps[2] - Ps[0]))
            if area > 1e-6:
                break
        else:
            continue

        # === TODO(c2): estimate transform using Umeyama ===
        R_k, t_k = umeyama_alignment(Ps, Qs)

        # === TODO(c3): compute transformed distances for all correspondences ===
        P_all = (P_corr @ R_k.T) + t_k
        errors = np.linalg.norm(P_all - Q_corr, axis=1)
        inliers = errors < tau
        inlier_count = int(inliers.sum())
        if inlier_count > 0:
            rmse_k = np.sqrt(np.mean(errors[inliers]**2))
        else:
            rmse_k = np.inf

        best_count = int(best_inliers.sum())
        if (inlier_count > best_count) or (inlier_count == best_count and rmse_k < best_rmse):
            best_inliers = inliers
            best_R, best_t = R_k, t_k
            best_rmse = rmse_k

    # === TODO(c4): refit final (R, t) using inlier subset ===
    if best_inliers.any():
        P_best = P_corr[best_inliers]
        Q_best = Q_corr[best_inliers]
        best_R, best_t = umeyama_alignment(P_best, Q_best)
    else:
        best_R, best_t = umeyama_alignment(P_corr, Q_corr)

    return best_R, best_t, best_inliers
