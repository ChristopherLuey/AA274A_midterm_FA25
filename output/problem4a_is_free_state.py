    def is_free_state(self, obstacle_cloud, x, bx, by):
        # Returns True if the robot in pose "x" is not in collision with the obstacle point cloud, otherwise returns False

        # State information
        tau = np.reshape(x[:2],(2,1)) #displacement
        theta = x[2] #angle

        ########## Code starts here ##########
        # Hint: If one of the points in the point cloud is contained in the drone body, return False immediately; you don't need to check the rest.

        # Rotation matrix
        c, s = np.cos(theta), np.sin(theta)
        R = np.array([[c, -s],
                      [s,  c]])

        # Matrix A defining the planes of the rectangle boundaries
        A = np.array([
            [1.0, 0.0],
            [-1.0, 0.0],
            [0.0, 1.0],
            [0.0, -1.0],
        ])

        # b defining distance to the planes
        half_width = 0.5 * bx
        half_height = 0.5 * by
        b = np.array([
            -half_width,
            -half_width,
            -half_height,
            -half_height,
        ])

        R_world_to_body = R.T
        A_world = A @ R_world_to_body
        b_world = b.reshape(-1, 1) - A_world @ tau

        for point in obstacle_cloud:
            q_world = point.reshape(2, 1)
            if np.all(A_world @ q_world + b_world <= 0):
                return False

        return True

        ########## Code ends here ##########

