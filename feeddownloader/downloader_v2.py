import xml.etree.ElementTree as xmlparse
import urlparse as up
import urllib2 as u2

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

    local_path = parsed_arguments.local_path







# parsed_xml = xmlparse.parse(u2.urlopen(feed_url))

    try:
  	    all_downloads = [item.findtext('link') for item in xmlparse.parse(u2.urlopen(feed_url)).iterfind('channel/item')]
    except xmlparse.ParseError:
        print "Error: invalid URL. Quitting ..."
        exit(0)
    
