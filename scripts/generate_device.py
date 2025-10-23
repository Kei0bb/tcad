import subprocess
import os

def generate_finfet_geo(fin_width, fin_height, gate_length, oxide_thickness, source_drain_length, geo_filename):
    """Generates a Gmsh .geo file for a simplified 2D FINFET."""
    geo_content = f"""
// Gmsh .geo file for a simplified 2D FINFET

// Device dimensions (in meters)
fin_width = {fin_width};
fin_height = {fin_height};
gate_length = {gate_length};
oxide_thickness = {oxide_thickness};
source_drain_length = {source_drain_length};
channel_length = gate_length;

// Points for the fin (Silicon)
Point(1) = {{{{0, 0, 0, 1e-9}}}}; 
Point(2) = {{{{source_drain_length, 0, 0, 1e-9}}}}; 
Point(3) = {{{{source_drain_length + channel_length, 0, 0, 1e-9}}}}; 
Point(4) = {{{{source_drain_length + channel_length + source_drain_length, 0, 0, 1e-9}}}}; 
Point(5) = {{{{0, fin_height, 0, 1e-9}}}}; 
Point(6) = {{{{source_drain_length, fin_height, 0, 1e-9}}}}; 
Point(7) = {{{{source_drain_length + channel_length, fin_height, 0, 1e-9}}}}; 
Point(8) = {{{{source_drain_length + channel_length + source_drain_length, fin_height, 0, 1e-9}}}}; 

// Lines for the fin
Line(1) = {{{{1, 2}}}}; // Source bottom
Line(2) = {{{{2, 3}}}}; // Channel bottom
Line(3) = {{{{3, 4}}}}; // Drain bottom
Line(4) = {{{{4, 8}}}}; // Drain right
Line(5) = {{{{8, 7}}}}; // Drain top
Line(6) = {{{{7, 6}}}}; // Channel top
Line(7) = {{{{6, 5}}}}; // Source top
Line(8) = {{{{5, 1}}}}; // Source left

// Fin surface
Curve Loop(1) = {{{{1, 2, 3, 4, 5, 6, 7, 8}}}}; 
Plane Surface(1) = {{{{1}}}}; 
Physical Surface("fin") = {{{{1}}}}; 

// Points for the gate oxide
Point(9) = {{{{source_drain_length, fin_height, 0, 1e-9}}}}; // Same as Point(6)
Point(10) = {{{{source_drain_length + channel_length, fin_height, 0, 1e-9}}}}; // Same as Point(7)
Point(11) = {{{{source_drain_length, fin_height + oxide_thickness, 0, 1e-9}}}}; 
Point(12) = {{{{source_drain_length + channel_length, fin_height + oxide_thickness, 0, 1e-9}}}}; 

// Lines for the gate oxide
Line(9) = {{{{9, 10}}}}; // Oxide bottom (fin top) 
Line(10) = {{{{10, 12}}}}; // Oxide right
Line(11) = {{{{12, 11}}}}; // Oxide top
Line(12) = {{{{11, 9}}}}; // Oxide left

// Gate oxide surface
Curve Loop(2) = {{{{9, 10, 11, 12}}}}; 
Plane Surface(2) = {{{{2}}}}; 
Physical Surface("gate_oxide") = {{{{2}}}}; 

// Points for the gate metal
Point(13) = {{{{source_drain_length, fin_height + oxide_thickness, 0, 1e-9}}}}; // Same as Point(11)
Point(14) = {{{{source_drain_length + channel_length, fin_height + oxide_thickness, 0, 1e-9}}}}; // Same as Point(12)
Point(15) = {{{{source_drain_length, fin_height + oxide_thickness + fin_height, 0, 1e-9}}}}; // Simplified gate height
Point(16) = {{{{source_drain_length + channel_length, fin_height + oxide_thickness + fin_height, 0, 1e-9}}}}; // Simplified gate height

// Lines for the gate metal
Line(13) = {{{{13, 14}}}}; // Gate bottom (oxide top)
Line(14) = {{{{14, 16}}}}; // Gate right
Line(15) = {{{{16, 15}}}}; // Gate top
Line(16) = {{{{15, 13}}}}; // Gate left

// Gate metal surface
Curve Loop(3) = {{{{13, 14, 15, 16}}}}; 
Plane Surface(3) = {{{{3}}}}; 
Physical Surface("gate") = {{{{3}}}}; 

// Physical Lines for contacts
Physical Line("source_contact") = {{{{1}}}}; // Source bottom line
Physical Line("drain_contact") = {{{{3}}}}; // Drain bottom line
Physical Line("gate_contact") = {{{{15}}}}; // Gate top line
"""
    with open(geo_filename, "w") as f:
        f.write(geo_content)
    print(f"Generated {geo_filename}")

def create_mesh(geo_filename, msh_filename):
    """Runs Gmsh to generate a .msh file."""
    try:
        subprocess.run(["gmsh", "-2", geo_filename, "-o", msh_filename, "-format", "msh2"], check=True)
        print(f"Generated {msh_filename} using Gmsh.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Gmsh: {e}")
        raise
    except FileNotFoundError:
        print("Gmsh command not found. Please ensure Gmsh is installed and in your PATH.")
        raise

def main():
    """Main function to generate device geometry and mesh."""
    # Device dimensions (example values, can be adjusted)
    fin_width = 10e-9  # 10 nm
    fin_height = 30e-9 # 30 nm
    gate_length = 20e-9 # 20 nm
    oxide_thickness = 1e-9 # 1 nm
    source_drain_length = 30e-9 # 30 nm

    # Output directory
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    geo_filename = os.path.join(output_dir, "finfet.geo")
    msh_filename = os.path.join(output_dir, "finfet.msh")

    # 1. Generate Gmsh .geo file
    generate_finfet_geo(fin_width, fin_height, gate_length, oxide_thickness, source_drain_length, geo_filename)

    # 2. Run Gmsh to generate .msh file
    create_mesh(geo_filename, msh_filename)

if __name__ == "__main__":
    main()
