import numpy as np
import matplotlib.pyplot as plt

def function_Ackley(input, nplot):
    x = np.linspace(-35, 35, 100)  # Create a grid of x values
    y = np.linspace(-35, 35, 100)  # Create a grid of y values
    X, Y = np.meshgrid(x, y)  # Create a grid of (x, y) points

    d = len(input)
    a = 20
    b = 0.2
    c = 2 * np.pi

    # Ackley function.
    sum1 = X**2 + Y**2
    sum2 = np.cos(c * X) + np.cos(c * Y)
    term1 = -a * np.exp(-b * np.sqrt(sum1 / d))
    term2 = -np.exp(sum2 / d)

    # Value should be multiplied by -1 (maximization)
    Z = -(term1 + term2 + a + np.exp(1))

    # Plotting...
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
