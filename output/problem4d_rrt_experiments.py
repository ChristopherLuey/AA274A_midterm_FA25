def run_case(name, cloud_path, background_path, bounds, x_init, x_goal, eps, max_iters, bx, by, figure_filename):
    """Execute MidtermRRT on the provided map and save the resulting plot."""
    maze_cloud = np.load(cloud_path)
    background = plt.imread(background_path)

    rrt = MidtermRRT(bounds[0], bounds[1], x_init, x_goal, maze_cloud, bx, by, background)
    success = rrt.solve(eps, max_iters)
    path_len = len(rrt.path) if rrt.path is not None else 0

    figure_path = OUTPUT_DIR / figure_filename
    plt.savefig(figure_path, bbox_inches="tight")
    plt.close()

    return {
        "name": name,
        "success": bool(success),
        "path_length": path_len,
        "num_obstacles": len(maze_cloud),
        "figure": str(figure_path),
    }


