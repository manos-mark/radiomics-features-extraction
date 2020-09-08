import SimpleITK as sitk
import numpy as np

def main():
    inputImageFileName = 'R01-001.nii'
    inputRoiFileName = 'R01-001_roi.nii'

    reader = sitk.ImageFileReader()
    reader.SetImageIO("NiftiImageIO")

    reader.SetFileName(inputImageFileName)
    imageDicom = reader.Execute();

    reader.SetFileName(inputRoiFileName)
    roiDicom = reader.Execute();

    # As list of 2D SimpleITK images
    list_of_images = [imageDicom[:,:,i] for i in range(imageDicom.GetDepth())]
    list_of_rois = [roiDicom[:,:,i] for i in range(roiDicom.GetDepth())]

    if len(list_of_rois) != len(list_of_images):
        print("Error: Image`s count is not the same as Roi`s count!")
        return

    writer = sitk.ImageFileWriter()

    for index, (image, roi) in enumerate(zip(list_of_images, list_of_rois)):
        writer.SetFileName(inputImageFileName.split('.')[0] + '-' + str(index+1) + '.dcm')
        writer.Execute(image)

        castedImage = sitk.Cast(roi, sitk.sitkUInt8);
        writer.SetFileName(inputRoiFileName.split('.')[0] + '-' +  str(index+1) + '.bmp')
        writer.Execute(castedImage)

if __name__ == '__main__':
    main()



    # # As list of 2D numpy arrays which cannot be modified (no data copied)
    # list_of_2D_images_np_view = [sitk.GetArrayViewFromImage(image[:,:,i]) for i in range(max_index)]
    #
    # # As list of 2D numpy arrays (data copied to numpy array)
    # list_of_2D_images_np = [sitk.GetArrayFromImage(image[:,:,i]) for i in range(max_index)]

    # Join two N-D Vector images to form an (N+1)-D image
    # join = sitk.JoinSeriesImageFilter()
    # joined_image = join.Execute(list_of_2D_images)

    # im = sitk.JoinSeries(list_of_2D_images)

    # # Extract first three channels of joined image (assuming RGB)
    # select = sitk.VectorIndexSelectionCastImageFilter()
    # channel1_image = select.Execute(joined_image, 0, sitk.sitkUInt8)
    # channel2_image = select.Execute(joined_image, 1, sitk.sitkUInt8)
    # channel3_image = select.Execute(joined_image, 2, sitk.sitkUInt8)
    #
    # # Recompose image (should be same as joined_image)
    # compose = sitk.ComposeImageFilter()
    # composed_image = compose.Execute(channel1_image, channel2_image, channel3_image)
