import matplotlib.pyplot as plt
import numpy as np

def plot_potential(x_coords, y_coords, potential, gate_voltage):
    """Plots the electrostatic potential."""
    plt.figure()
    plt.tricontourf(x_coords, y_coords, potential, levels=20, cmap="viridis")
    plt.colorbar(label="Potential (V)")
    plt.xlabel("Position (m)")
    plt.ylabel("Position (m)")
    plt.title(f"FINFET Electrostatic Potential (Vg = {gate_voltage} V)")
    # Save the figure instead of showing it
    plt.savefig("output/potential.png")
    print("Saved potential plot to output/potential.png")
    plt.close()

def main():
    """Main function to plot results."""
    # This is a placeholder.
    # In the future, this will read data from a GTS output file.
    print("Plotting results (placeholder)...")
    # Example data
    x = np.random.rand(100)
    y = np.random.rand(100)
    p = np.sin(x * np.pi) * np.cos(y * np.pi)
    vg = 0.5
    plot_potential(x, y, p, vg)

if __name__ == "__main__":
    main()
