from gurobipy import *
from vehicle import Vehicle
from obstacle import Obstacle
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    # Inputs to the generation of the obstacles
    min_size = 1         # minimum size of the obstacle
    max_size = 2         # maximum size of the obstacle


    # Inputs to the generation of the vehicles
    vehicle_mass = 5        # mass of the vehicles
    v_max = 0.225           # maximum velocity of the vehicle
    paper = 8               # figure from the original paper that wants to be verified

    # Figure 7 in the paper: 3 vehicles
    if paper == 7:
        area_size = 2.5  # window size
        wp = False       # switch for use of waypoints. True: waypoints can be used. False: function deactivated
        diag_x = 0.0857  # initial x-velocity component of the aircraft flying in a diagonal direction
        diag_y = 0.15    # initial y-velocity component of the aircraft flying in a diagonal direction

        vx_init = [0.17246, -diag_x, -diag_x]  # initial x-component of velocity
        vy_init = [0.03, diag_y, -diag_y]      # initial y-component of velocity
        f_max = 0.2                            # maximum force experienced by a vehicle
        T = 30                                 # maximum time of travel
        dt = 0.5                               # time step size
        obs_coords = []                        # array containing all obstacles in [x_min,x_max,y_min,y_max] format
        veh_coords = [[-2, 0, 2, 0], [1, -1.732, -1, 1.732],
                      [1, 1.732, -1, -1.732]]  # array containing all vehicles in [x_0,y_0,x_fin,y_fin] format
        wp_coords = [[], [], []]               # array containing all waypoint in [x_wp,y_wp] format for each vehicle
        name = 'multi-vehicles.png'            # name of the figure to be saved

    # Figure 8 in the paper: 4 vehicles
    if paper == 8:
        area_size = 4            # window size
        wp = False               # switch for use of waypoints. True: waypoints can be used. False: function deactivated

        f_max = 0.29             # maximum force experienced by a vehicle
        T = 30                   # maximum time of travel
        dt = 1                   # time step size
        obs_coords = []          # array containing all obstacles in [x_min,x_max,y_min,y_max] format
        veh_coords = [[-2, -4, 2, 0], [2, -2, 0, 0],
                      [-2, 0, 2, -2], [-2, -2, 2, 2]]  # array containing all vehicles in [x_0,y_0,x_fin,y_fin] format
        facs = 0.037             # factor to scale the initial velocity such that is lower than the maximum velocity
        vx_init = [(veh_coords[0][2] - veh_coords[0][0]) * facs, (veh_coords[1][2] - veh_coords[1][0]) * facs,
                   (veh_coords[2][2] - veh_coords[2][0]) * (facs + 0.01),
                   (veh_coords[3][2] - veh_coords[3][0]) * (facs)]  # initial x-component of velocity
        vy_init = [(veh_coords[0][3] - veh_coords[0][1]) * facs, (veh_coords[1][3] - veh_coords[1][1]) * facs,
                   (veh_coords[2][3] - veh_coords[2][1]) * (facs - 0.04),
                   (veh_coords[3][3] - veh_coords[3][1]) * (facs)]  # initial y-component of velocity
        wp_coords = [[], [], []]    # array containing all waypoint in [x_wp,y_wp] format
        name = 'four aircraft.png'  # name of the figure to be saved


    # Figure 9 in the paper: waypoints without obstacle
    if paper == 9:
        area_size = 10  # window size
        wp = True       # switch for use of waypoints. True: waypoints can be used. False: function deactivated
        vx_init = [0]   # initial x-component velocity
        vy_init = [0]   # initial y-component velocity
        f_max = 0.2     # maximum force experienced by a vehicle
        T = 100         # maximum time of travel
        dt = 4          # time step size
        obs_coords = []                  # array containing all obstacles in [x_min,x_max,y_min,y_max] format
        veh_coords = [[5, 5, 0, -2]]     # array containing all vehicles in [x_0,y_0,x_fin,y_fin] format
        wp_coords = [[[-0.7, 6], [-5, 4]]]  # array containing all waypoint in [x_wp,y_wp] format
        name = 'waypoints.png'              # name of the figure to be saved

    # Figure 10 in the paper: waypoint with obstacle
    if paper == 10:
        area_size = 10      # window size
        wp = True           # switch for use of waypoints. True: waypoints can be used. False: function deactivated
        vx_init = [-0.19]   # initial x-component velocity
        vy_init = [-0.1]    # initial y-component velocity
        f_max = 0.15        # maximum force experienced by a vehicle
        T = 200             # maximum time of travel
        dt = 4.             # time step size
        obs_coords = [[0, 1.7, 0, 9]]     # array containing all obstacles in [x_min,x_max,y_min,y_max] format
        veh_coords = [[5, 5, -0.7, 6]]    # array containing all vehicles in [x_0,y_0,x_fin,y_fin] format
        wp_coords = [[[0, -2], [-5, 4]]]  # array containing all waypoint in [x_wp,y_wp] format
        name = 'waypoints_obs.png'        # name of the figure to be saved

    steps = int(T / dt)                             # number of steps
    obstacles = []                                  # list which will contain all obstacles
    for ob in obs_coords:                           # for every obstacle
        tmp = Obstacle(ob[0], ob[1], ob[2], ob[3])  # local obstacle variable
        tmp.draw()                                  # draw local obstacle
        obstacles.append(tmp)                       # attach obstacle to obstacle list


    # Create initial and final positions

    num_vehicles = len(veh_coords)
    x0 = []; y0 = []                                 # initial positions for all vehicles
    x_fin = []; y_fin = []                           # final positions for all vehicles
    for i in range(num_vehicles):
        x0.append(veh_coords[i][0])
        y0.append(veh_coords[i][1])
        x_fin.append(veh_coords[i][2])
        y_fin.append(veh_coords[i][3])

    # Create location of all waypoints for all vehicles
    n_way_points = len(wp_coords[0])
    x_wp = []; y_wp = []                             # position of all waypoints of all vehicles
    if wp:                                           # if wp is True, waypoints are used
        for i in range(num_vehicles):
            x_dummy = []; y_dummy = []               # position of all waypoints of one vehicle
            for j in range(n_way_points):
                x_dummy.append(wp_coords[i][j][0])
                y_dummy.append(wp_coords[i][j][1])

            x_wp.append(x_dummy)
            y_wp.append(y_dummy)

    # Initialize model
    m = Model("ppl")

    # Create vehicles and add model main variables
    vehicles = []
    for i in range(num_vehicles):
        if wp:
            vehicles.append(
                Vehicle(vehicle_mass, dt, T, x0[i], y0[i], i, obstacles, m, v_max, f_max, area_size, x_fin[i], y_fin[i],
                        wp, x_wp[i], y_wp[i]))
        else:
            vehicles.append(
                Vehicle(vehicle_mass, dt, T, x0[i], y0[i], i, obstacles, m, v_max, f_max, area_size, x_fin[i], y_fin[i],
                        wp))
    # Add constraints and add model secondary variables
    for i in range(num_vehicles):
        vehicles[i].constrain(m, vehicles, vx_init[i], vy_init[i])

    # Obtaining the objective function
    total = 0                                # total number of time steps between all the vehicles (minimize)
    epsilon = 0.01
    for veh in range(len(vehicles)):
        for i in range(steps):
            total += vehicles[veh].b[i] * i + vehicles[veh].fm[i]*epsilon


    m.setObjective(total, GRB.MINIMIZE)

    # Optimizing the model and obtaining the values of he parameters and the objective function
    m.optimize()
    m.getVars()

    # Plotting the results

    for i in range(num_vehicles):
        z = 0
        if paper == 7:
            # Plot a bold point at the 18th point as done in the paper
            plt.scatter(vehicles[i].x[18].x, vehicles[i].y[18].x, facecolor = 'blue', edgecolor = 'blue')
            # Plot dashed lines connecting initial and final points for all vehicles
            plt.plot([veh_coords[i][0], veh_coords[i][2]], [veh_coords[i][1], veh_coords[i][3]], 'k--', alpha = 0.5)
        elif paper == 8:
            # Plot dashed lines connecting initial and final points for all vehicles
            plt.plot([veh_coords[i][0], veh_coords[i][2]], [veh_coords[i][1], veh_coords[i][3]], 'k--', alpha=0.5)
        elif paper == 9 or paper == 10:
            # Plot arrow as shown in the paper
            plt.arrow(7.5, 5, -2, 0, length_includes_head=True, head_width=0.3)
        for k in range(steps):                 # obtaining time step at which vehicle reaches the final point
            Z = str(vehicles[i].b[k])
            if Z[-5] == "1":
                z = k
                break
        coords = np.zeros([z,2])
        for j in range(z):                    # obtaining the coordinates to plot
            coords[j, :] = [vehicles[i].x[j].x,vehicles[i].y[j].x]
        if wp:                                # plotting the location of the waypoints
            for jj in range(len(x_wp[i])):
                plt.plot(x_wp[i][jj], y_wp[i][jj], '*', color='b')
        plt.scatter(coords[:,0], coords[:,1], facecolor = 'none', edgecolor = 'blue')  # plot the trajectories of the vehicles
        plt.plot(vehicles[i].x_fin, vehicles[i].y_fin, '*', color='b')    # plot the final points star
        plt.scatter(vehicles[i].x_fin, vehicles[i].y_fin, facecolor = 'none', edgecolor = 'blue')  # plot the final points circle

    plt.xlim([-area_size, area_size])   # limit the plot space
    plt.ylim([-area_size, area_size])   # limit the plot space
    plt.savefig(name)                   # save the resulting plot
    plt.show()
