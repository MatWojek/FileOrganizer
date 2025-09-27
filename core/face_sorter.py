import os 
import shutil 
import numpy

import cv2
import face_recognition 
from sklearn.cluster import DBSCAN

# TODO: Define constants
# - Set constants for image formats to process (e.g., .jpg, .png).
# - Define thresholds for face recognition and clustering.

# TODO: Load training data
# - Traverse the training folders.
# - Extract face encodings for each person from images in their respective folders.
# - Store the encodings and associate them with the folder/person name.

# TODO: Train the model
# - Use clustering (e.g., DBSCAN) or other machine learning techniques to group similar faces.
# - Save the trained model or encodings for later use.

# TODO: Define sorting logic
# - Traverse the folder containing unsorted images.
# - Detect faces in each image.
# - Compare detected faces with the trained encodings to identify the person.
# - Move the image to the corresponding folder based on the identified person.

# TODO: Handle unknown faces
# - If a face does not match any known encoding, move it to an "unknown" folder.
# - Optionally, allow the user to manually classify unknown faces.

# TODO: Optimize performance
# - Use batch processing for face detection and encoding.
# - Skip images without detectable faces to save time.

# TODO: Error handling
# - Handle cases where no faces are detected in an image.
# - Handle corrupted or unsupported image files gracefully.

# TODO: Logging
# - Log the sorting process, including the number of images processed, skipped, or moved.
# - Log errors for debugging purposes.

# TODO: Testing
# - Test the module with a variety of datasets to ensure accuracy.
# - Validate that images are sorted into the correct folders.

# TODO: Integrate with GUI
# - Add a button in the GUI to trigger the face sorting process.
# - Display progress and results in the GUI.

# TODO: Optional enhancements
# - Add support for incremental learning (e.g., adding new faces to the model without retraining from scratch).
# - Allow the user to adjust clustering parameters via the GUI.
# - Add a preview feature to show detected faces before sorting.