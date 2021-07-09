def basePath():
    from platform import node
    if node().split('-')[0]=='gadi':
        return '/g/data/oi10/replicas/'    
    else:
        """This is to figure out which computer this is running on""" 
        from platform import system
        operatingSystem = system()
        if operatingSystem == 'Windows':
            return 'E:/CMIP5-PMIP3/'
        if operatingSystem == 'Linux':
            return '/mnt/e/CMIP5-PMIP3/'
        elif operatingSystem == 'Darwin':
            return '/Volumes/Untitled/CMIP5-PMIP3/'  
        else:
            raise EnvironmentError("Can't find where to look for data files. Operating System is " + operatingSystem)