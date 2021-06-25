def awsDownloader(model, varname, test, variant ): 

    import boto3
    import botocore
    import s3fs
    
    #source: https://github.com/aradhakrishnanGFDL/gfdl-aws-analysis/blob/community/examples/s3_list_example.py

    '''
    This script provides an example on how to list files (all Amon tas fields in the gfdl-esgf bucket) in the gfdl-esgf bucket with anonymous access
    You can edit the prefix, delimiters, search facets such as miptable/varname as you see fit.
    '''
    
    
    region = 'us-east-2'
    s3client = boto3.client('s3',region_name=region,
                            config=botocore.client.Config(signature_version=botocore.UNSIGNED)
                           )

    paginator = s3client.get_paginator('list_objects')

    source_bucket = 'esgf-world'

    #miptable = "Amon"
    s3prefix = "s3:/"

    #pat = re.compile(r'key\/.+\/<pattern>\/.+.gz')

    fileObjs = list()

    fs_s3 = s3fs.S3FileSystem(anon=True)

    if any([test=='historical', test=='piControl']):
        source_prefix='CMIP6/CMIP/'
    elif test.find('ssp')>=0:
        source_prefix='CMIP6/ScenarioMIP/'
    
    source_prefix = source_prefix + institutionFinder(model) +'/'+ model +'/'+ test + '/' + variant
    print(source_prefix)

    fileList=list()
    
    for result in paginator.paginate(Bucket=source_bucket, Prefix=source_prefix, Delimiter='.nc'):
        for prefixes in result.get('CommonPrefixes'):
            commonprefix = prefixes.get('Prefix')
            searchpath = commonprefix

     #       print(searchpath)
            pat = re.compile('({}/{}/)'.format(varname.split('_')[1],varname.split('_')[0]))
            m = re.search(pat, searchpath)
            if m is not None:
                lst = commonprefix.split('/')
                print('Downloading ' + lst[-1])
                path=('{}/{}/{}'.format(s3prefix,source_bucket,commonprefix))
                fs_s3.download(path, basePath()+'CMIP6/'+lst[-1])
                fileList.append(basePath()+'CMIP6/'+lst[-1])
                
    if len(fileList)==0:
        print("file not found on AWS")
    return fileList
                