import xml.etree.ElementTree as xmlparse
import urlgrabber as ug


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
        print "Error: invalid RSS feed. Quitting ..."
        exit(0)
    except URLError as e:
    	print str(e)
    	exit(0)
    except ValueError as e:
    	print str(e)
    	exit(0)
    except KeyError as e:
    	print str(e)
    	exit(0)

    print all_downloads

    # downloading
    for single_download in all_downloads:
    	print "Starting: "+ single_download
    	g = ug.grabber.URLGrabber(reget='simple',retry=2)
    	response = ug.urlgrab(single_download)
    	print "Completed: "+ single_download
