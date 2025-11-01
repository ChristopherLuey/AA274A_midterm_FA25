def ransac_line(points, eps=0.08, n_iter=150):
    """
    Robust line fitting y = m x + b using RANSAC.

    Args:
        points: (N,2) array of [x_i, y_i].
        eps:    inlier distance threshold (default 0.08).
        n_iter: number of RANSAC iterations.

    Returns:
        best_m, best_b, inliers_mask
    """
    N = points.shape[0]
    best_m, best_b = 0.0, 0.0
    best_inliers = np.zeros(N, dtype=bool)
    rng = np.random.default_rng(SEED_LINE)

    for k in range(n_iter):
        # --- Sample two distinct points ---
        idx = rng.choice(N, size=2, replace=False)
        (x_a, y_a), (x_b, y_b) = points[idx]

        # --- Fit candidate line y = m x + b ---
        m = (y_b - y_a) / (x_b - x_a)
        b = y_a - m * x_a

        # --- Compute distances and find inliers ---
        denom = np.hypot(m, 1.0)
        distances = np.abs(m * points[:, 0] - points[:, 1] + b) / denom
        inliers = distances <= eps
        if np.sum(inliers) > np.sum(best_inliers):
            best_inliers = inliers
            best_m, best_b = m, b

    # --- Refit line using least squares on all inliers ---
    if np.sum(best_inliers) >= 2:
        A = np.column_stack([points[best_inliers, 0], np.ones(np.sum(best_inliers))])
        y = points[best_inliers, 1]
        best_m, best_b = np.linalg.lstsq(A, y, rcond=None)[0]
    else:
        A = np.column_stack([points[:, 0], np.ones(N)])
        y = points[:, 1]
        best_m, best_b = np.linalg.lstsq(A, y, rcond=None)[0]
        best_inliers = np.ones(N, dtype=bool)

    return best_m, best_b, best_inliers
