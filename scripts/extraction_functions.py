# extraction_functions.py
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import csv

def extract_article_content(url):
    """
    Extracts structured content, handles Figma, prevents duplicate Tech Stack, formats Project Snapshots.
    Project Snapshots now sequentially numbered (1, 2, 3...), Meta Info restored.
    Handles generic embeds as 'link' type, and specifically identifies Figma embeds.
    Removed "Figure Element Found" and "Embed Wrapper Found" debug prints.
    """
    structured_data = []
    tech_stack_extracted = False

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. Entry Title
        entry_title_tag = soup.select_one('h1.entry-title')
        if entry_title_tag:
            structured_data.append({"type": "entry_title", "content": entry_title_tag.text.strip()})

        # 2. Extract Meta Info
        meta_info_container = soup.select_one('div.td-module-meta-info')
        if meta_info_container:
            meta_info = {}
            author_section = soup.select_one('div.td-module-meta-info div.td-post-author-name')
            if author_section:
                author_by_tag = author_section.find("div", class_="td-author-by")
                author_by = author_by_tag.text.strip() if author_by_tag else ""
                author_name_tag = author_section.find("a")
                author_name = author_name_tag.text.strip() if author_name_tag else ""
                meta_info["author_by"] = author_by
                meta_info["author_name"] = author_name
            date_section = meta_info_container.find("span", class_="td-post-date")
            date = date_section.text.strip() if date_section else "Date not found"
            meta_info["date"] = date
        structured_data.append({"type": "meta_info", "content": meta_info})

        # 3. Block Headings and content
        block_heading_tags = soup.select('h1.wp-block-heading')
        for heading_tag in block_heading_tags:
            heading_text = heading_tag.text.strip()
            content_elements = []
            current_element = heading_tag.find_next_sibling()

            while current_element and current_element.name in ['p', 'ul', 'ol', 'figure']:
                if current_element.name == 'p':
                    content_elements.append({'type': 'paragraph', 'content': current_element.text.strip()})
                elif current_element.name == 'ul' or current_element.name == 'ol':
                    list_type = 'unordered_list' if current_element.name == 'ul' else 'ordered_list'
                    list_items_data = []
                    list_item_tags = current_element.select('li')
                    for li_tag in list_item_tags:
                        list_item_content = {"text": li_tag.text.strip(), "images": []}
                        image_tags = li_tag.select('figure.wp-block-image img[src]')
                        for img_tag in image_tags:
                            list_item_content["images"].append({
                                "src": img_tag['src'],
                                "alt": img_tag.get('alt', '')
                            })
                        list_items_data.append(list_item_content)
                    content_elements.append({'type': list_type, 'list_items': list_items_data})
                    if heading_text.lower() == "tech stack":
                        tech_stack_extracted = True

                elif current_element.name == 'figure': # Handle figures (including embeds)
                    # print("\n --- Figure Element Found ---") # DEBUG LINE - REMOVED

                    if current_element.select_one('.wp-block-embed__wrapper iframe[src]'): # iframe embeds
                        iframe_tag = current_element.select_one('.wp-block-embed__wrapper iframe[src]')
                        embed_url = iframe_tag['src']
                        content_elements.append({'type': 'embed', 'embed_url': embed_url})
                    elif current_element.select_one('figure.wp-block-embed > .wp-block-embed__wrapper'): # Potential Figma or other embeds
                        # print("   --- Embed Wrapper Found ---") # DEBUG LINE - REMOVED
                        embed_text_div = current_element.select_one('figure.wp-block-embed > .wp-block-embed__wrapper')
                        # print(f"   Embed Wrapper HTML: {embed_text_div.prettify()}") # DEBUG LINE - REMOVED
                        embed_url = embed_text_div.text.strip()
                        if "figma.com" in embed_url.lower(): # NEW: Check if URL contains "figma.com"
                            # print("   --- Identified as Figma Embed ---") # DEBUG LINE - REMOVED
                            content_elements.append({'type': 'embed', 'embed_url': embed_url})
                        else: # If it's an embed wrapper but NOT Figma, treat as a generic link
                            # print("   --- NOT a Figma Embed - Treating as Link ---") # DEBUG LINE - REMOVED
                            content_elements.append({'type': 'link', 'link_url': embed_url}) # Use 'link' type for non-Figma embeds
                    elif current_element.find('img'): # Regular images
                        image_tag = current_element.find('img')
                        content_elements.append({'type': 'image', 'images':[{
                            "src": image_tag['src'],
                            "alt": image_tag.get('alt', '')
                        }]})
                current_element = current_element.find_next_sibling()

            structured_data.append({
                "type": "block_heading_section",
                "heading": heading_text,
                "content_elements": content_elements
            })


        # 4. Extract Standalone Lists (specifically EXCLUDE "Tech Stack" listed at the end)
        list_containers = soup.select('ul.wp-block-list, ol.wp-block-list')
        for list_container in list_containers:
            # --- Highly Specific "Tech Stack" Exclusion ---
            previous_element = list_container.find_previous_sibling() # Get the element before the list

            if previous_element and previous_element.name == 'h1': # Check if it's an h1
                if "tech stack" in previous_element.text.lower(): # Check if h1 text is "tech stack"
                    continue  # Skip this list if it's preceded by a "Tech Stack" heading

            is_under_block_heading = list_container.find_parent('h1.wp-block-heading')
            if is_under_block_heading:
                continue # General skip for lists under ANY block heading

            list_items_data = []
            list_item_tags = list_container.select('li')
            for li_tag in list_item_tags:
                list_item_content = {"text": li_tag.text.strip(), "images": []}
                image_tags = li_tag.select('figure.wp-block-image img[src]')
                for img_tag in image_tags:
                    list_item_content["images"].append({
                        "src": img_tag['src'],
                        "alt": img_tag.get('alt', '')
                    })
                list_items_data.append(list_item_content)

            structured_data.append({
                "type": "list_section",
                "list_items": list_items_data
            })

        return structured_data

    except RequestException as e:
        print(f" Request Error for URL: {url} - {e}")
    except AttributeError as e:
        import traceback
        print(f" Parsing Error for URL: {url} - AttributeError: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f" General Error for URL: {url} - {e}")

    return None


if __name__ == '__main__':
    # Test URL
    test_url = "https://insights.blackcoffer.com/ai-and-ml-based-youtube-analytics-and-content-creation-tool-for-optimizing-subscriber-engagement-and-content-strategy/"  # Changed to youtube-analytics for example
    csv_filepath = 'output_single_url.csv' # Define CSV file path for single URL output

    article_data = extract_article_content(test_url)
    print(f"\n--- Content for URL: {test_url} ---")
    if article_data:
        reached_contact_details = False
        # project_snapshot_counter = 1 # Removed project_snapshot_counter

        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile: # Open CSV file
            csv_writer = csv.writer(csvfile) # Create CSV writer

            # CSV Header Row (same as before)
            csv_writer.writerow([
                'URL', 'Section Type', 'Heading', 'Content Type', 'Content', 'Image Source', 'Image Alt Text', 'Link URL', 'Embed URL'
            ])

            for section in article_data:
                if reached_contact_details:
                    break
                if section['type'] == 'block_heading_section' and section['heading'].lower() == "contact details":
                    reached_contact_details = True

                if section['type'] == 'entry_title':
                    csv_writer.writerow([test_url, section['type'], None, None, section['content'], None, None, None, None])
                elif section['type'] == 'meta_info':
                    meta_info_content = section['content']
                    meta_author = meta_info_content.get('author_by', '') + " " + meta_info_content.get('author_name', '')
                    meta_date = meta_info_content.get('date', '')
                    csv_writer.writerow([test_url, section['type'], None, 'author', meta_author.strip(), None, None, None, None])
                    csv_writer.writerow([test_url, section['type'], None, 'date', meta_date.strip(), None, None, None, None])

                elif section['type'] == 'block_heading_section':
                    if not section['heading'].strip() or section['heading'].lower() == "summarize": # Skip empty or "Summarize"
                        continue

                    heading_text = section['heading']
                    if section['content_elements']:
                        for element in section['content_elements']:
                            if element['type'] == 'paragraph':
                                csv_writer.writerow([test_url, section['type'], heading_text, element['type'], element['content'], None, None, None, None])
                            elif element['type'] == 'unordered_list' or element['type'] == 'ordered_list':
                                # list_prefix = "" # Removed list prefixes entirely, no numbering for Project Snapshots
                                # if section['heading'].lower() == "project snapshots": # No numbering for project snapshots
                                #     list_prefix = f"{project_snapshot_counter}. "
                                # elif element['type'] == 'ordered_list':
                                #     list_prefix = "1. "

                                for item in element['list_items']:
                                    list_text = item['text']
                                    if item['images']:
                                        for img in item['images']:
                                            csv_writer.writerow([test_url, section['type'], heading_text, element['type'] + '-item-with-image', list_text, img['src'], img['alt'], None, None])
                                    else:
                                        csv_writer.writerow([test_url, section['type'], heading_text, element['type'] + '-item', list_text, None, None, None, None])
                            elif element['type'] == 'image':
                                # if section['heading'].lower() == "project snapshots": # No numbering for project snapshots
                                #     print(f"{project_snapshot_counter}. Image Source: {element['images'][0]['src']}, Alt Text: {element['images'][0]['alt']}")
                                #     project_snapshot_counter += 1
                                # else:
                                for img in element['images']:
                                    csv_writer.writerow([test_url, section['type'], heading_text, element['type'], None, img['src'], img['alt'], None, None])
                            elif element['type'] == 'embed':
                                csv_writer.writerow([test_url, section['type'], heading_text, element['type'], None, None, None, None, element['embed_url']])
                            elif element['type'] == 'link':
                                csv_writer.writerow([test_url, section['type'], heading_text, element['type'], None, None, None, element['link_url'], None])

                elif section['type'] == 'list_section': # Standalone lists
                    for item in section['list_items']:
                        list_text = item['text']
                        if item['images']:
                            for img in item['images']:
                                csv_writer.writerow([test_url, section['type'], None, 'standalone-list-item-with-image', list_text, img['src'], img['alt'], None, None])
                        else:
                            csv_writer.writerow([test_url, section['type'], None, 'standalone-list-item', list_text, None, None, None, None])

        print(f"\nData saved to '{csv_filepath}' for URL: {test_url}") # Specific message for single URL CSV save
    else:
        print(f"Extraction failed for URL: {test_url}")