def running_cost(x, u):
  px, vx, py, vy, phi, omega = x
  T1, T2 = u
  ex = px - goal[0]
  ey = py - goal[2]
  cost = (
    q_p * ex**2 +
    q_v * vx**2 +
    q_p * ey**2 +
    q_v * vy**2 +
    q_phi * phi**2 +
    q_omega * omega**2 +
    r_T * ((T1 - T_hov)**2 + (T2 - T_hov)**2)
  )
  return cost
