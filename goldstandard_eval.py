import numpy as np
import PIL.Image
import PIL.ImageDraw
import xml.etree.ElementTree as ET

# for testing purposes
import matplotlib.pyplot as plt

def get_polygons_from_XML(XML):
    """
    Takes in an XML file and returns the union of the mask of all polygons present in the XML file.
    :param XML: the XML formatted file
    :return: a mask of all polygons on the image
    """
    tree = ET.parse(XML)
    root = tree.getroot()

    # first, retrieve the dimensions of the image
    num_rows = int(root.find('imagesize/nrows').text)
    num_cols = int(root.find('imagesize/ncols').text)

    print("num_rows: " + str(num_rows))
    print("num_cols: " + str(num_cols))

    # create the result array
    result = np.zeros((num_rows, num_cols), dtype=np.uint8)
    print(result.shape)


    # iterate through each polygon
    objects = root.findall('object')
    for object in objects:

        polygon = object.find('polygon')
        polygon_points = polygon.findall('pt')
        points_list = []

        # Collect all x, y coordinate pairs into a list
        for point in polygon_points:
            x = int(point.find('x').text)
            y = int(point.find('y').text)

            points_list.append(x)
            points_list.append(y)

        # flood fill polygon points, store in mask
        temp = np.zeros((num_rows, num_cols), dtype=np.uint8)
        temp_mask = PIL.Image.fromarray(temp)
        PIL.ImageDraw.Draw(temp_mask).polygon(xy=points_list, outline=1, fill=1)
        mask = np.array(temp_mask, dtype=int)

        # combine with result array
        result = np.where(result > 0, result, mask)

    return result

def evaluate(gold, submitted):
    temp = np.where(submitted == gold, gold, np.zeros(gold.shape))
    plt.imshow(temp)
    gold_intersect_sub = temp.sum()

    return (gold_intersect_sub / gold.sum(), gold_intersect_sub / submitted.sum())


test_mask = get_polygons_from_XML('/Users/k_yang/Downloads/test.xml')
test_gold = get_polygons_from_XML('/Users/k_yang/Downloads/test_gold.xml')

print(evaluate(test_mask, test_gold))
#plt.imshow(test_mask)
#plt.show()