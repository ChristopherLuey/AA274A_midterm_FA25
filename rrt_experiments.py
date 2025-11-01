import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from P4_rrt import MidtermRRT


OUTPUT_DIR = Path("output/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_case(name, cloud_path, background_path, bounds, x_init, x_goal, eps, max_iters, bx, by, figure_filename, seed):
    """Execute MidtermRRT on the provided map and save the resulting plot."""
    np.random.seed(seed)
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


def main() -> None:
    cases = [
        {
            "name": "Cluster",
            "cloud_path": "data/maze_wall_map_cluster.npy",
            "background_path": "data/cluster.png",
            "bounds": ([0, 0, -np.pi / 2], [120, 120, np.pi / 2]),
            "x_init": [10, 20, np.pi / 4],
            "x_goal": [100, 90, np.pi / 6],
            "eps": 10.0,
            "max_iters": 2000,
            "bx": 20.0,
            "by": 10.0,
            "figure": "rrt_cluster.png",
            "seed": 3,
        },
        {
            "name": "Gap",
            "cloud_path": "data/maze_wall_map_gap.npy",
            "background_path": "data/gap.png",
            "bounds": ([0, 0, -np.pi / 2], [120, 120, np.pi / 2]),
            "x_init": [20, 30, -np.pi / 6],
            "x_goal": [90, 25, 0.0],
            "eps": 5.0,
            "max_iters": 2000,
            "bx": 10.0,
            "by": 5.0,
            "figure": "rrt_gap.png",
            "seed": 0,
        },
        {
            "name": "Level 4-3",
            "cloud_path": "data/maze_wall_map_43abridged.npy",
            "background_path": "data/4-3c_abridged.png",
            "bounds": ([0, 0, -np.pi / 2], [1243, 130, np.pi / 2]),
            "x_init": [183, 37, 0.0],
            "x_goal": [545, 59, 0.0],
            "eps": 10.0,
            "max_iters": 2000,
            "bx": 15.0,
            "by": 12.0,
            "figure": "rrt_level43.png",
            "seed": 0,
        },
    ]

    summaries = [
        run_case(
            case["name"],
            case["cloud_path"],
            case["background_path"],
            (np.array(case["bounds"][0]), np.array(case["bounds"][1])),
            case["x_init"],
            case["x_goal"],
            case["eps"],
            case["max_iters"],
            case["bx"],
            case["by"],
            case["figure"],
            case["seed"],
        )
        for case in cases
    ]

    for summary in summaries:
        print(
            f"{summary['name']}: success={summary['success']}, "
            f"path nodes={summary['path_length']}, obstacles={summary['num_obstacles']}, "
            f"figure={summary['figure']}"
        )


if __name__ == "__main__":
    main()
