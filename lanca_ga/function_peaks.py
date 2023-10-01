import numpy as np
import matplotlib.pyplot as plt

def function_peaks(input, nplot):
    x = np.linspace(-3, 3, 100)  # Create a grid of x values
    y = np.linspace(-3, 3, 100)  # Create a grid of y values
    X, Y = np.meshgrid(x, y)  # Create a grid of (x, y) points

    # PEAKS function.
    Z = 3 * (1 - X) ** 2 * np.exp(-X ** 2 - (Y + 1) ** 2) \
        - 10 * (X / 5 - X ** 3 - Y ** 5) * np.exp(-X ** 2 - Y ** 2) \
        - 1 / 3 * np.exp(-(X + 1) ** 2 - Y ** 2)

    # Turn off warning.
    np.seterr(all='ignore')

    if nplot == 2:
        fig = plt.figure(figsize=(12, 5))
        
        # 3D Surface Plot
        ax1 = fig.add_subplot(121, projection='3d')
        ax1.plot_surface(X, Y, Z, cmap='viridis')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('3D Surface Plot')
        
        # Contour Plot
        ax2 = fig.add_subplot(122)
        contour = ax2.contourf(X, Y, Z, 20, cmap='viridis')
        plt.colorbar(contour)
        plt.plot(input[0], input[1], marker='o', markersize=10, color='k', markerfacecolor='none', linewidth=2)
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_title('Contour Plot')
        
        plt.tight_layout()
        plt.show()

    return Z
