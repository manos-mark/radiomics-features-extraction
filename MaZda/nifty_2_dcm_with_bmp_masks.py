import SimpleITK as sitk
import os,glob
import numpy as np
import binascii
import cv2

def read_and_save_data(path_file, path_roi, save_path):
    # Read patient images
    image = sitk.ReadImage(path_file)
    image = np.squeeze(sitk.GetArrayFromImage(image))
    image_shape = np.shape(image)

    roi = sitk.ReadImage(path_roi)
    roi = np.squeeze(sitk.GetArrayFromImage(roi))
    roi_shape = np.shape(roi)

    # ta arxeia nifti einai ena dicom series ta opoia theloume na eksagoume
    # to mazda xreiazetai sigekrimenh katalhksh arxeiou gia na to diabasei
    # to image prepei na exe katalhksh .dcm
    # kai to mask prepei na exei katalhskh .roi h .bmp
    for i in range(image_shape[0]):
        # an yparxoun dicom mesa sto arxeio nifti
        if  np.sum(roi[i,:,:]) > 0:
            casted_roi = np.ones((roi_shape[1], roi_shape[2]), dtype=np.uint8)

            # xreiazetai to mask value na einai 0 kai girw girw 16
            casted_roi[roi[i,:,:]==0] = 16
            casted_roi[roi[i,:,:]==1] = 0

            # gia na apothikeutei se binary
            roi_bytearray = bytearray(casted_roi)

            # gia na diabasei to arxeio to mazda xreiazetai head kai tail
            header = '42 4D 36 04 04 00 00 00 00 00 36 04 00 00 28 00 00 00 00 02 00 00 00 02 00 00 01 00 08 00 00 00 00 00 00 00 04 00 E8 03 00 00 E8 03 00 00 00 00 00 00 00 00 00 00 00 00 FF 00 00 FF 00 00 FF 00 00 00 FF FF 00 00 FF 00 FF 00 00 FF FF 00 00 80 FF 00 80 00 FF 00 00 FF 80 00 80 FF 00 00 FF 00 80 00 FF 80 00 00 00 C4 FF 00 00 FF C4 00 FF 00 C4 00 C4 FF 00 00 00 00 00 00 01 01 01 00 02 02 02 00 03 03 03 00 04 04 04 00 05 05 05 00 06 06 06 00 07 07 07 00 08 08 08 00 09 09 09 00 0A 0A 0A 00 0B 0B 0B 00 0C 0C 0C 00 0D 0D 0D 00 0E 0E 0E 00 0F 0F 0F 00 10 10 10 00 11 11 11 00 12 12 12 00 13 13 13 00 14 14 14 00 15 15 15 00 16 16 16 00 17 17 17 00 18 18 18 00 19 19 19 00 1A 1A 1A 00 1B 1B 1B 00 1C 1C 1C 00 1D 1D 1D 00 1E 1E 1E 00 1F 1F 1F 00 20 20 20 00 21 21 21 00 22 22 22 00 23 23 23 00 24 24 24 00 25 25 25 00 26 26 26 00 27 27 27 00 28 28 28 00 29 29 29 00 2A 2A 2A 00 2B 2B 2B 00 2C 2C 2C 00 2D 2D 2D 00 2E 2E 2E 00 2F 2F 2F 00 30 30 30 00 31 31 31 00 32 32 32 00 33 33 33 00 34 34 34 00 35 35 35 00 36 36 36 00 37 37 37 00 38 38 38 00 39 39 39 00 3A 3A 3A 00 3B 3B 3B 00 3C 3C 3C 00 3D 3D 3D 00 3E 3E 3E 00 3F 3F 3F 00 40 40 40 00 41 41 41 00 42 42 42 00 43 43 43 00 44 44 44 00 45 45 45 00 46 46 46 00 47 47 47 00 48 48 48 00 49 49 49 00 4A 4A 4A 00 4B 4B 4B 00 4C 4C 4C 00 4D 4D 4D 00 4E 4E 4E 00 4F 4F 4F 00 50 50 50 00 51 51 51 00 52 52 52 00 53 53 53 00 54 54 54 00 55 55 55 00 56 56 56 00 57 57 57 00 58 58 58 00 59 59 59 00 5A 5A 5A 00 5B 5B 5B 00 5C 5C 5C 00 5D 5D 5D 00 5E 5E 5E 00 5F 5F 5F 00 60 60 60 00 61 61 61 00 62 62 62 00 63 63 63 00 64 64 64 00 65 65 65 00 66 66 66 00 67 67 67 00 68 68 68 00 69 69 69 00 6A 6A 6A 00 6B 6B 6B 00 6C 6C 6C 00 6D 6D 6D 00 6E 6E 6E 00 6F 6F 6F 00 70 70 70 00 71 71 71 00 72 72 72 00 73 73 73 00 74 74 74 00 75 75 75 00 76 76 76 00 77 77 77 00 78 78 78 00 79 79 79 00 7A 7A 7A 00 7B 7B 7B 00 7C 7C 7C 00 7D 7D 7D 00 7E 7E 7E 00 7F 7F 7F 00 80 80 80 00 81 81 81 00 82 82 82 00 83 83 83 00 84 84 84 00 85 85 85 00 86 86 86 00 87 87 87 00 88 88 88 00 89 89 89 00 8A 8A 8A 00 8B 8B 8B 00 8C 8C 8C 00 8D 8D 8D 00 8E 8E 8E 00 8F 8F 8F 00 90 90 90 00 91 91 91 00 92 92 92 00 93 93 93 00 94 94 94 00 95 95 95 00 96 96 96 00 97 97 97 00 98 98 98 00 99 99 99 00 9A 9A 9A 00 9B 9B 9B 00 9C 9C 9C 00 9D 9D 9D 00 9E 9E 9E 00 9F 9F 9F 00 A0 A0 A0 00 A1 A1 A1 00 A2 A2 A2 00 A3 A3 A3 00 A4 A4 A4 00 A5 A5 A5 00 A6 A6 A6 00 A7 A7 A7 00 A8 A8 A8 00 A9 A9 A9 00 AA AA AA 00 AB AB AB 00 AC AC AC 00 AD AD AD 00 AE AE AE 00 AF AF AF 00 B0 B0 B0 00 B1 B1 B1 00 B2 B2 B2 00 B3 B3 B3 00 B4 B4 B4 00 B5 B5 B5 00 B6 B6 B6 00 B7 B7 B7 00 B8 B8 B8 00 B9 B9 B9 00 BA BA BA 00 BB BB BB 00 BC BC BC 00 BD BD BD 00 BE BE BE 00 BF BF BF 00 C0 C0 C0 00 C1 C1 C1 00 C2 C2 C2 00 C3 C3 C3 00 C4 C4 C4 00 C5 C5 C5 00 C6 C6 C6 00 C7 C7 C7 00 C8 C8 C8 00 C9 C9 C9 00 CA CA CA 00 CB CB CB 00 CC CC CC 00 CD CD CD 00 CE CE CE 00 CF CF CF 00 D0 D0 D0 00 D1 D1 D1 00 D2 D2 D2 00 D3 D3 D3 00 D4 D4 D4 00 D5 D5 D5 00 D6 D6 D6 00 D7 D7 D7 00 D8 D8 D8 00 D9 D9 D9 00 DA DA DA 00 DB DB DB 00 DC DC DC 00 DD DD DD 00 DE DE DE 00 DF DF DF 00 E0 E0 E0 00 E1 E1 E1 00 E2 E2 E2 00 E3 E3 E3 00 E4 E4 E4 00 E5 E5 E5 00 E6 E6 E6 00 E7 E7 E7 00 E8 E8 E8 00 E9 E9 E9 00 EA EA EA 00 EB EB EB 00 EC EC EC 00 ED ED ED 00 EE EE EE 00 EF EF EF 00'
            header = header.split(' ')

            # to tail einai keno gia na erthei to roi sto katallhlo megethos
            tail = '10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10'
            tail = tail.split(' ')

            # roi name
            roi_output = save_path + name + '_roi_slice_' + str(i) + '.bmp'

            # save roi
            with open(roi_output, "wb") as f:
                for item in header:
                    # metatrepoume to header apo string se hex
                    f.write(binascii.unhexlify(item))
                # grafoume sto binary arxeio to periexomeno ths eikonas
                f.write(roi_bytearray)
                # grafoume to tail
                for item in tail:
                   # metatrepoume to header apo string se hex
                   f.write(binascii.unhexlify(item))

            # Read roi image and flip upside down and save again
            roi_reopened = sitk.ReadImage(roi_output)
            roi_reopened = np.squeeze(sitk.GetArrayFromImage(roi_reopened))
            roi_flipped = np.flipud(roi_reopened)
            cv2.imwrite(roi_output, roi_flipped)

            image_output = save_path + name + '_slice_' + str(i) + '.dcm'

            # save image
            sitk.WriteImage(sitk.GetImageFromArray(image[i,:,:]), image_output)

            # Write txt file for mazda macro
            with open(path + macro_file, 'a') as f:
                f.write('\n' + 'LoadImage ' + image_output + '\n' + 'LoadROI ' + roi_output)
                f.write('\n' + 'RunAnalysis' + '\n' + 'SaveReport .\\reports\\result_' + name + '_roi_slice_' + str(i) + '.xls')


if __name__ == '__main__':
    dataset_path = 'C:\\Users\\manosmark\\Desktop\\dataset\\'
    path = 'C:\\Users\\manosmark\\Desktop\\radiomic_features\\MaZda\\'
    save_path = 'C:\\Users\\manosmark\\Desktop\\radiomic_features\\MaZda\\bmp_images\\'

    macro_file = 'load_and_analyze.txt.txt'

    # Remove macro file if exists
    if (os.path.isfile(path + macro_file)):
        os.remove(path + macro_file)

    os.chdir(dataset_path)
    name_list = glob.glob('*.nii')
    patient_names = []

    for i in range(len(name_list)):
        if '_roi' not in name_list[i]:
            patient_names.append(name_list[i][:-4])

    for name in patient_names:
        print(name)
        path_roi = dataset_path + name + '_roi.nii'
        path_file = dataset_path + name + '.nii'

        read_and_save_data(path_file, path_roi, save_path)
