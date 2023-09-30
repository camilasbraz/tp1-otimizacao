import numpy as np
import matplotlib.pyplot as plt

def function_peaks(input, nplot):
    # PEAKS function.
    x = input[0]
    y = input[1]
    
    z = 3 * (1 - x) ** 2 * np.exp(-x ** 2 - (y + 1) ** 2) \
        - 10 * (x / 5 - x ** 3 - y ** 5) * np.exp(-x ** 2 - y ** 2) \
        - 1 / 3 * np.exp(-(x + 1) ** 2 - y ** 2)

    # Turn off warning.
    np.seterr(all='ignore')

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
