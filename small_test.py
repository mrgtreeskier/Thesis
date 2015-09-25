__author__ = '2d Lt Kyle Palko, USAF'

# https://nilearn.github.io/manipulating_visualizing/manipulating_images.html#loading-data
from nilearn.masking import apply_mask
from nilearn import plotting as pltt
from matplotlib import pyplot as plt

## Fetch datasets automatically using data_download

my_data = ['pitt3.nii', 'pitt4.nii']
# create images with our data
# pltt.plot_anat('tt_mask_pad.nii', output_file='ttmaskout')
# pltt.plot_anat('tst1.nii', output_file='tst1')
# pltt.plot_anat('tst2.nii', output_file='tst2')

# mask using the tt mask from preprocesssed data
# from nilearn.masking import compute_epi_mask
# mask_img = compute_epi_mask('tt_mask_pad.nii')
# plt.plot_anat(mask_img, output_file='mask')  # create an image of the mask
# masked_data = apply_mask(my_data, mask_img)

# # using preprocessed pitt data
# pltt.plot_anat('pitt3mask.nii', output_file='pitt3mask')
masked_data = apply_mask(my_data[0], 'pitt3mask.nii')
print('Completed Masking')


# # masked_data shape is (timepoints, voxels). We can plot the first 150
# # timepoints from two voxels (converting the 4D image to 2D data)
plt.figure(figsize=(7, 5))
plt.plot(masked_data[:2, :150].T)
plt.xlabel('Time [TRs]', fontsize=16)
plt.ylabel('Intensity', fontsize=16)
plt.xlim(0, 150)
plt.subplots_adjust(bottom=.12, top=.95, right=.95, left=.12)
plt.show()

print('Completed voxel by time comparison plot')

# # Smooth brain (or just show smoothed brain)
from nilearn import image
fmri_img = image.smooth_img(my_data[0], fwhm=0)
mean_img = image.mean_img(fmri_img)
pltt.plot_epi(mean_img, title='Smoothed mean EPI', output_file='smooth')
print('Completed brain smoothing')


# DATA parcellation into a correlation table (what we want but I don't know if it's correct
# https://nilearn.github.io/auto_examples/connectivity/plot_signal_extraction.html#example-connectivity-plot-signal-extraction-py
# https://nilearn.github.io/connectivity/functional_connectomes.html

# plot the tt atlas
pltt.plot_roi('tt_mask_pad.nii', output_file='tt_roi_plot')
print('Completed brain ROI')

# extract signals on parcellation
from nilearn.input_data import NiftiLabelsMasker
masker = NiftiLabelsMasker(labels_img='tt_mask_pad.nii', standardize=True)

time_series = masker.fit_transform(my_data[0])  # size is 19012

import numpy as np
correlation_matrix = np.corrcoef(time_series.T)  # size is only 97x97

# plot the correlation matrix
plt.figure(figsize=(10,10))
plt.imshow(correlation_matrix, interpolation='nearest')
plt.show()

print('Completed Program')