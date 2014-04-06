rss-feed-downloader
===================

Content downloader from a RSS feed

It can download content from a RSS feed link

You can run like this command:

    python downloader.py --feed=<RSS-Feed-URL> --output=<PATH-TO-DIRECTORY>
    
    if no "--output" argument is supplied, default location will YOUR_OS_DECLARED_HOME_FOLDER

By importing "download" module, you can use this function to initiate download:

    download(rss_link, local_folder)

Yet TO-DO:
   (.)  completing partial download from FTP server
