import numpy as np
import matplotlib.pyplot as plt

def function_rastrigin(input, nplot):
    # Constants
    coef = 10
    d = len(input)
    lb = [-5.12] * d
    ub = [5.12] * d

    # Create a grid of (x, y) coordinates
    npts = 100  # Adjust the number of points as needed
    x = np.linspace(lb[0], ub[0], npts)
    y = np.linspace(lb[1], ub[1], npts)
    x, y = np.meshgrid(x, y)

    # Rastrigin function.
    z = -(x**2 + y**2 - coef * (np.cos(2 * np.pi * x) - np.cos(2 * np.pi * y)) + d * coef)

    # Plotting...
    if nplot == 2:
        fig = plt.figure(figsize=(12, 5))
        
        # 3D Surface Plot
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_surface(x, y, z, cmap='viridis')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('3D Surface Plot')
        
        # Contour Plot
        ax2 = fig.add_subplot(122)
        contour = ax2.contourf(x, y, z, 20, cmap='viridis')
        plt.colorbar(contour)
        plt.plot(input[0], input[1], marker='o', markersize=10, color='k', markerfacecolor='none', linewidth=2)
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_title('Contour Plot')
        
        plt.tight_layout()
        plt.show()

    return z