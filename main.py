 import pandas as pd
 from avogadro import molecule, builder, rendering
 # Sample data file with atomic positions (X, Y, Z) for each atom
 data_file = "molecules.xyz"
 def distinguish_diatomic_triatomic(data_path):
 """
 This function analyzes bond angles in a molecule to distinguish
 diatomic and triatomic structures.
 Args:
 data_path (str): Path to the data file containing atomic
 positions.
 Returns:
 list: A list containing molecule IDs and classifications
 ("diatomic" or "triatomic").
 """
 results = []
 # Read data using pandas
 data = pd.read_csv(data_path, sep=" ", header=None, skiprows=2)
7
 # Extract number of atoms per molecule (assuming the first line
 specifies this)
 num_atoms = int(data.iloc[0, 0])
 # Looping through each molecule's data (assuming data is grouped
 by number of atoms)
 for i in range(0, len(data), num_atoms):
 # Extracting atomic positions for the current molecule
 atomic_positions = data.iloc[i+2:i+num_atoms+2,
 1:4].to_numpy(dtype=float)
 # Calculating distances between all atom pairs (using a helper
 function)
 distances = calculate_all_atom_distances(atomic_positions)
 # Checking for diatomic molecule (only one bond distance)
 if len(set(distances.flatten())) == 1:
 results.append((i // num_atoms, "diatomic"))
 continue
 # Check for triatomic molecule (potentially 2 unique bond
 distances)
 if len(set(distances.flatten())) == 2:
 results.append((i // num_atoms, "triatomic"))
 continue
 # If not diatomic or triatomic based on distances, classify as
 "unknown" (potential limitation)
 results.append((i // num_atoms, "unknown"))
8
 return results
 """
 Calculates pairwise distances between all atoms in a molecule.
 Args:
 positions (numpy.ndarray): A numpy array containing atomic
 positions (X, Y, Z coordinates).
 Returns:
 numpy.ndarray: A distance matrix where rows and columns
 represent atom indices and values represent distances.
 """
 def calculate_all_atom_distances(positions):
 num_atoms = positions.shape[0]
 distances = np.zeros((num_atoms, num_atoms))
 for i in range(num_atoms):
 for j in range(i+1, num_atoms):
 # Calculate distance using Euclidean distance formula
 distance = np.linalg.norm(positions[i]-positions[j])
 distances[i, j] = distance
 distances[j, i] = distance # Fill upper triangular matrix for
 symmetry
 return distances
 # Example usage
9
 results = distinguish_diatomic_triatomic(data_file)
 # Print classification results (modify for Avogadro integration)
 for molecule_id, classification in results:
 print(f"Molecule {molecule_id+1} classification:
 {classification}")
 # (Optional) Basic Avogadro visualization (assuming molecule IDs
 correspond to data order)
 for molecule_id, classification in results:
 # Create molecule object and build from positions (example based
 on results[0])
 mol = molecule.Molecule()
 builder.buildMoleculeFromAtoms(mol,
 data.iloc[molecule_id*num_atoms+2:molecule_id*num_atoms+num_atoms+2,
 1:4].to_numpy())
 # Set temporary color based on classification (modify for clarity)
 if classification == "diatomic":
 mol.atomTypes[0].SetColor((1, 0, 0)) # Red for diatomic
 elif classification == "triatomic":
 mol.atomTypes[0].SetColor((0, 0, 1)) # Blue for triatomic
 else:
 mol.atomTypes[0].SetColor((0.5, 0.5, 0.5)) # Grey for unknown
 # Add molecule to viewer and render (replace with your chosen
 rendering method)
 viewer = rendering.MoleculeViewer()
 viewer.AddMolecule(mol)
10
 viewer.render()
