import yaml
import xml.etree.ElementTree as xml_tree
import xml

with open('feed.yaml', 'r') as feed:
    feed_yaml = yaml.safe_load(feed)
    
    #https://help.apple.com/itc/podcasts_connect/#/itcbaf351599

    rss_element = xml_tree.Element('rss', {
        'version':'2.0',
        'xmlns:itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content':'http://purl.org/rss/1.0/modules/content/'
    })

channel_subElemnet = xml_tree.SubElement(rss_element, 'channel')

link_prefix = feed_yaml['link']

xml_tree.SubElement(channel_subElemnet, 'title').text = feed_yaml['title']
xml_tree.SubElement(channel_subElemnet, 'format').text = feed_yaml['format']
xml_tree.SubElement(channel_subElemnet, 'itunes:author').text = feed_yaml['author']
xml_tree.SubElement(channel_subElemnet, 'description').text = feed_yaml['description']
xml_tree.SubElement(channel_subElemnet, 'itunes:image', {'href':link_prefix + feed_yaml['image']})
xml_tree.SubElement(channel_subElemnet, 'language').text = feed_yaml['language']
xml_tree.SubElement(channel_subElemnet, 'itunes:category', {'text': feed_yaml['category']})

for item in feed_yaml['item']:
    item_element = xml_tree.SubElement(channel_subElemnet, 'item')
    xml_tree.SubElement(item_element, 'title').text = item['title']
    xml_tree.SubElement(item_element, 'itunes:author').text = feed_yaml['author']
    xml_tree.SubElement(item_element, 'description').text = item['description']
    xml_tree.SubElement(item_element, 'itunes:duration').text = item['duration']
    xml_tree.SubElement(item_element, 'pubDate').text = item['published']
    xml_tree.SubElement(item_element, 'enclosure', {
        'url': link_prefix + item['file'],
        'type': 'audio/mpeg',
        'length': item['length']
    })


output_tree = xml_tree.ElementTree(rss_element)
xml.etree.ElementTree.indent(output_tree, space='  ', level=0)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)

