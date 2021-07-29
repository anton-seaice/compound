# compound

This is a collection of scripts to examine changing frequenices of compounding impacts from multiple climate drivers upon mainland South East Australia.

Developed using python 3.7

IDE versioning

jupyter core     : 4.7.1
jupyter-notebook : 6.3.0
qtconsole        : 5.0.3
ipython          : 7.22.0
ipykernel        : 5.3.4
jupyter client   : 6.1.12
jupyter lab      : 3.0.14
nbconvert        : 6.0.7
ipywidgets       : 7.6.3
nbformat         : 5.1.3
traitlets        : 5.0.5

Dependencies

xarray 0.18.0
numpy 1.17.0
cartopy 0.18.0
eofs-1.4.0
xesmf

To Run:

output from cesmIndeces is needed for everything else
output from cesmPrecTsMonthly is needed for cesmCompoundsImpact

Descriptions:

1. cesmIndeces
- Calculates monthly indeces (for indeces included in utils/_indexDefinitions.py)
- Calculates warm season averages (time periods defined in utils/_indexDefinitions.py)

2. cesmCompounds
- Plots of annual trends in enso, iod, sam
- Example of how events compound to be fire promoting or not-fire promoting
- Plots of 30 year trends in compounding events

3. cesmCompoundsType
- Plots of 30 years trends in compounding events, seperated by event type (i.e. on of the three pairs or all3)

4. cesmPrecTsMonthly
- Calculates warm season averages for prec and Ts

5. cesmCompoundImpacts
- Rainfall and Temp anomalies for each individial event type, and each compound event type

Source data:
- CESM-LME ensemble outputs
- CMIP5 past1000/historical/rcp outputs
- CVDP outputs (for validation purposes only)

Useful git commands:

normal commit: git commit -m "message", git add
add changed files only: git add -u
tagging: git tag v1.0 ; git push --tags


Undo a commit & redo

$ git commit -m "Something terribly misguided" # (0: Your Accident)
$ git reset HEAD~                              # (1)
[ edit files as necessary ]                    # (2)
$ git add .                                    # (3)
$ git commit -c ORIG_HEAD                      # (4)

    This command is responsible for the undo. It will undo your last commit while leaving your working tree (the state of your files on disk) untouched. You'll need to add them again before you can commit them again).

    Make corrections to working tree files.

    git add anything that you want to include in your new commit.

    Commit the changes, reusing the old commit message. reset copied the old head to .git/ORIG_HEAD; commit with -c ORIG_HEAD will open an editor, which initially contains the log message from the old commit and allows you to edit it. If you do not need to edit the message, you could use the -C option.

Alternatively, to edit the previous commit (or just its commit message), commit --amend will add changes within the current index to the previous commit.

To remove (not revert) a commit that has been pushed to the server, rewriting history with git push origin master --force is necessary.
