# Import my functions
from sys import path
path.append('../')
from helpers.basePath import basePath

def esgfDownloader(model, varname, test, variant, *kwargs ):
    
    """Access esgf through the API search tool and download the result.
    
    This is very slow because it relies on downloading a WGET script and running that in Bash. Howevery, this seems to be the most reliable method to download data.
    
    """
    
    from pyesgf.search import SearchConnection
    from subprocess import check_output
    
    #The German API connection seems better than the NCI one (more reliable/up to date, so i've been using that. (Maybe its slow?))
    conn = SearchConnection('https://esgf-data.dkrz.de/esg-search')
    #conn = SearchConnection('https://esgf-node.llnl.gov/esg-search')
    #conn = SearchConnection('https://esgf.nci.org.au/esg-search')

    #Search query on the server. I think this is run server side.
    #ToDO: Possible add the CMIP Table. Sometimes it downloads extraneous stuff.
    ctx = conn.new_context(
        latest=True,
        project='CMIP6', 
        source_id=model, 
        experiment_id=test, 
        variable=varname.split('_')[0], 
        table_id=varname.split('_')[1], 
        frequency='mon', 
        variant_label=variant,
        #grid_label='gn'
        #data_node='esgf.nci.org.au'
        #data_node='esgf-data1.llnl.gov'
    )

    #Do the search
    results = ctx.search()
    
    #This line doesn't work reliably??
    if ctx.hit_count==0:
        print(model+varname+test+variant+" file not found on ESGF")

        # The results include every data_node this can be sourced from, so trying to download from every node is somewhat wasteful. However, sometimes a node is down, so this means it will try every node.
        #For every result, grab the Wget script and run it.
        #Linux/Unix only
    for result in results:
        print(result.dataset_id +' downloading')
        with open(basePath()+'CMIP6/'+model+varname+test+'dl.sh', "w") as writer:
            writer.write(
                result.file_context().get_download_script()
            )
        try:
            #There is in annoying feature where this bash file will almost infinitely (esp if there are lots of files) retry the same data node if it doesn't get a response. A better behaviour would be to kill the script and move onto another node.
            check_output('bash ./'+model+varname+test+'dl.sh -s &', shell=True, cwd=basePath()+'CMIP6')
        except Exception as e:
            print(e)
            #Sometimes it may produce an empty file
            #By catching the exception we can keep going and hope to find the same file on another node (in the results list)
            
    return True