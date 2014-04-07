__Project__ = "RSS-feed-downloader"
__author__  = "Khaled Monsoor <k@kmonsoor.com>"

"""
This is the main module
"""

import xml.etree.ElementTree as xmlparse
import urlparse as up
import urllib2 as u2
import argparse
import os
import sys
import re

os_path_sepeator = '\\' if os.name in 'nt' else '/'


def target_download(remote_path_fname, local_location):
    """
    This function handles individual download.
    It distinguish between HTTP and FTP downloads, and use respective function.
    
    remote_path_fname --> (str) complete link of the target download 
    local_location -->  (str) Complete path of the saving folder/directory
    """
    parsed_address = up.urlparse(link)
    scheme = parsed_address.scheme

    fname = remote_path_fname.split('/')[-1]
    localpath = local_location + os_path_sepeator + fname

    if 'ftp' in scheme:
        download_ftp(remote_path_fname, localpath)
    elif 'http' in scheme:
        download_http(remote_path_fname, localpath)
    else:
        print "Error: Unsupported protocol"
        done = False
        return done
        
    done = True
    return done


def download_ftp(remote_path_fname, localpath, user="anonymous",password="anonymous"):
    parsed_address = up.urlparse(remote_path_fname)
    fname = parsed_address.path
    directory = re.sub(fname, parsed_address.path, '')

    try:
        ftp = ftplib.FTP(parsed_address.netloc)
    except gaierror:
        print "Server Connection error."
    except error:
        print "Server Connection error."
        
    response = ftp.login(user,password)
    if '230' not in response:
        print "Login failed with user:%s / password%s" % (user,password)
        done = False
        return done

    try:
        ftp.cwd(direcory)
    except error_perm:
        print "invalid directory"
        done = False
        return done
        
    with open(localpath) as f:
        response = ftp.retrbinary("RETR " + parsed_address.path, f.write)
    if '226' not in response:
        done = False
        print "Download failed: " + (localpath.split(os_path_sepeator))[-1]
    else:
        done = True
        print "Download successful: " + (localpath.split(os_path_sepeator))[-1]
    return done
    


def download_http(remote_path_fname, localpath):
    start = 0
    end = 0
    chunk_size = 1024 * 50   # 10KB
    
    response = u2.urlopen(remote_path_fname)

    # checking size
    try:
        download_size = int(response.info().getheaders("Content-Length")[0])
    except IndexError:
        print "oops! server couldn't recognize \"Content-Length\" header"
        return False
    print "Download_Size:" + str(download_size)
    
    # checking if local file exists or not
    if os.path.exists(localpath):
        current_size = os.path.getsize(localpath)
        print "Current_Size:" + str(current_size)
        if current_size >= download_size:
            print remote_path_fname.split('/')[-1] + " is already downloaded. skipping ..."
            done = True
            return done
        else:
            start = current_size + 1
            end = download_size
            try:
                local_file_handle = open(localpath,"ab",0)
            except IOError:
                print "Local location couldn't be accessed for writing"
                done = False
                return done
    else:
        try:
            local_file_handle = open(localpath,"wb",0)
        except IOError:
            print "Local saving location couldn't be accessed. skipping"
            done = False
            return done
        
        print "Starting Download: %s \n Size:%sKB" % (fname, download_size/1024)
        end = download_size


    chunk_counter = 0
    while start < end:
        request = u2.Request(remote_path_fname)
        if start + chunk_size > end:
            request.headers['Range'] = 'bytes=%s-%s' % (start, end)
        else:
            request.headers['Range'] = 'bytes=%s-%s' % (start, start + chunk_size)
        try:
            payload_handle = u2.urlopen(request)
            payload = payload_handle.read()
        except HTTPError, URLError:
            print "oops! server couldn't reached properly"
            return None
        # data received, now adding to local file
        try:
            local_file_handle.write(payload)
        except IOError:
            print "Local location couldn't be accessed for writing"
            return False
        start += chunk_size + 1
        chunk_counter += 1
        print chunk_counter,

    done = True
    local_file_handle.close()
    payload_handle.close()
    
    # download is completed
    print "Download completed:" + str(os.path.getsize(localpath)) + "Bytes"
    return True

# def usage(progname):
    # print "Usage: python downloader.py --feed=<RSS-Feed-URL> --output=<PATH-TO-DIRECTORY>"

if __name__ == '__main__':
    cli_command = argparse.ArgumentParser(description='Download contents by grabbing links from a given RSS feed url')
    cli_command.add_argument('--feed', dest='feed_url', action='store', help='URL of the RSS feed')
    cli_command.add_argument('--output', dest='local_location', action='store', help='local folder, where to save the files')
    
    parsed_arguments = cli_command.parse_args(sys.argv[1:])
    
    if parsed_arguments.feed_url==None:
        print "Error: Sorry. Feed-URL cannot be empty. Quitting from this job ..."
        exit(0)
    else:
        feed_url = parsed_arguments.feed_url
    
    if parsed_arguments.local_location==None:
        print "Warning: Saving location is not given. Going to use default location depending on your OS."
        local_location = os.environ['HOMEPATH'] if os.name  in 'nt' else "~/"
        home_drive = os.environ['HOMEDRIVE']
        os_path_sepeator = '\\' if os.name in 'nt' else '/'
        local_location = home_drive + local_location + os_path_sepeator + re.sub("[^0-9a-z]","_",feed_url)
        print "Auto-detected Download location: %s" % local_location
    else:
        local_location = parsed_arguments.local_path

    try:
        parsed_xml = xmlparse.parse(u2.urlopen(feed_url))
    except xmlparse.ParseError:
        print "Error: invalid URL. Quitting ..."
        exit(0)
    all_downloads = [item.findtext('link') for item in parsed_xml.iterfind('channel/item')]
    
    for download in all_downloads:
        target_download(download, local_location)
