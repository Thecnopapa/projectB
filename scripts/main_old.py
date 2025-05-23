# Project_B by Iain Visa @ IBMB-CSIC / UB

# Essential imports
import os
import pandas as pd
from utilities import *
import platform




def main(PROCESS_ALL = False,
         LARGE_DATASET = True,
         DO_ONLY = "",
         GENERATE_SYMMETRIES = True,
         MAX_THREADS = 1,
         ):




    # Set up
    vars["do_only"] = DO_ONLY
    print(local.list())

    # Enable garbage collection
    enable_garbage_collector()

    from dataframes import save_dfs, create_dfs
    from imports import pickle, export

    # Download large dataset
    tprint("Downloading large data")
    from imports import download_pdbs
    if "many_pdbs" not in local.list() and LARGE_DATASET:
        download_pdbs(os.path.join(root.pdb_lists,"list_1500"), "many_pdbs", terminal = True)
    eprint("Large data downloaded")


    # Load/Import molecule files
    tprint("Loading files")
    from imports import load_from_files, load_references
    from molecules import Reference, PDB
    vars["references"] = load_references()

    if LARGE_DATASET:
        molecules = load_from_files(local.many_pdbs, force_reload = PROCESS_ALL)
    else:
        molecules = load_from_files(local.experimental, force_reload = PROCESS_ALL)
    eprint("Files loaded")


    # Create dataframes
    sprint("Creating dataframes")
    create_dfs(vars.references)
    eprint("Dataframes created")


    # Generate symmetries and produce dimers
    sprint("Generating dimers")
    from symmetries import symmetries
    progress = ProgressBar(len(molecules))
    for molecule in molecules:
        if GENERATE_SYMMETRIES:
            #molecule.get_all_dimers(force = PROCESS_ALL)
            pass
        else:
            molecule.get_dimers()
        molecule.pickle()
        progress.add(info=molecule.id)
        del molecule
        collect_garbage()
    del molecules
    collect_garbage()
    eprint("Symmetries generated")


    quit()
    # Load/Generate monomer files
    '''tprint("Loading monomers")
    from imports import load_monomers
    monomers = load_monomers(molecules = molecules, force_reload=PROCESS_ALL)
    pickle(monomers)
    eprint("Monomers loaded")'''


    # Align references to monomers
    '''tprint("Aligning monomers")
    progress = ProgressBar(len(monomers))
    try:
        for monomer in monomers:
            monomer.sequence_align(references, force_align = PROCESS_ALL)
            progress.add()
        pickle(monomers)
        save_dfs()
        eprint("Monomers aligned")
    except:
        sprint("Alignments could not be produced")'''



    # Superpose references to monomers
    '''tprint("Superposing monomers")
    progress = ProgressBar(len(monomers))
    for monomer in monomers:
        monomer.superpose(references, force_superpose = PROCESS_ALL)
        progress.add(info=monomer.id)
    pickle(monomers)
    save_dfs()
    eprint("Monomers superposed")'''


    # Load/Generate dimer files
    '''tprint("Loading dimers")
    from imports import load_dimers
    dimers = load_dimers(molecules = molecules, force_reload=PROCESS_ALL)
    pickle(dimers)
    eprint("Dimers loaded")'''

    # Processing dimers
    '''tprint("Processing dimers")
    progress = ProgressBar(len(dimers))
    for dimer in dimers:
        #dimer
        progress.add()
    pickle(dimers)
    save_dfs()
    eprint("Dimers processed")'''



    # Save and exit
    tprint("Saving data")
    save_dfs() # Save dataframes and generate figures

    '''all_files = references + molecules + monomers + dimers # select all loaded files
    progress = ProgressBar(len(all_files))
    for file in all_files:
        file.pickle() # Save the object
        file.export() # Save the pdb
        progress.add()
    eprint("Finished")'''

    # Done xd


if __name__ == "__main__":
    # Setup paths and globals
    import setup

    # Imports that need globals initialised:
    from Globals import root, local, vars

    main(PROCESS_ALL=False, # Ignore saved pickles and generate everything from scratch
         LARGE_DATASET = True, # Use a large dataset (delete all local data previously to avoid errors)
         DO_ONLY = "" # ( list of strings / string) Names of pdbs to be processed (CAPS sensitive, separated by space) e.g ["5N10", "1M2Z"] or "5N10 1M2Z"
         )
    quit()

    from surface import surface
    surface(FORCE_SASA=True,
            FORCE_SIMILARITY=True
            )

    from clustering import clustering
    clustering(FORCE_ALL=False,
               )



