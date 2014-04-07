rss-feed-downloader
===================

Content downloader from a RSS feed.


You can run like this command:

    python downloader.py --feed=<RSS-Feed-URL> --output=<PATH-TO-DIRECTORY>
    
if no "--output" argument is supplied, default location will be your OS' current user folder


By importing "download" module, you can use this function to initiate download:

    download(rss_link, local_folder)
    
To download a single file from a HTTP server, use this function:

    download_http(remote_path_link, localpath_with_filename)
    

To download a single file from a FTP server, use this function:

    download_ftp(remote_path_link, localpath_with_filename)



Yet TO-DO:

   - completing partial download from FTP server
   - 1-byte bug in HTTP download
   - exhaustive test
