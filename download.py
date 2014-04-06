from xml.etree.ElementTree import parse
import urlparse as up
import urllib2 as u2
import os
import sys

path_sepeator = '\\' if os.name in 'nt' else '/'

def download(feed_url, local_location):
    parsed_xml = parse(u2.urlopen(feed_url))
    all_downloads = [item.findtext('link') for item in parsed_xml.iterfind('channel/item')]
    
    for download in all_downloads:
        target_download(download, local_location)


def target_download(remote_path_fname, local_location):
    parsed_address = up.urlparse(link)
    scheme = parsed_address.scheme

    fname = remote_path_fname.split('/')[-1]
    localpath = local_location + path_sepeator + fname

    if 'ftp' in scheme:
        download_ftp(remote_path_fname, localpath)
    elif 'http' in scheme:
        download_http(remote_path_fname, localpath)
    else:
        print "Error: Unsupported protocol"
        done = False
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
        print "Download failed: " + (localpath.split(path_sepeator))[-1]
    else:
        done = True
        print "Download successful: " + (localpath.split(path_sepeator))[-1]
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

"""
if __name__=="__main__":
    remote = "http://archive.apache.org/dist/apr/binaries/win32/apr-1.2.12-winnt-x86-ipv6-msvcrt60.zip"
    local = "c:\\new"
    print remote
    print local
    download(remote,local)
"""


def usage(progname):
    print "Usage: python downloader.py --feed=<RSS-Feed-URL> --output=<PATH-TO-DIRECTORY>"

if __name__ == '__main__':
    if(len(sys.argv) < 3):
        usage(sys.argv[0])
        sys.exit(1)

    """ 
# to-do: fix command line parsing
    cli_command = argparse.ArgumentParser(description='Download contents by grabbing links from a given RSS feed url')
    cli_command.add_argument('--feed=', dest='feed_url', action='store_const', const=feed_url, help='URL of the RSS feed')
    cli_command.add_argument('--output=', dest='local_path', action='store_const', const=local_path, help='local folder to save the files')
    """
    
    parsed_xml = parse(u2.urlopen(feed_url))
    all_downloads = [item.findtext('link') for item in parsed_xml.iterfind('channel/item')]
    
    for download in all_downloads:
        target_download(download, local_location)
