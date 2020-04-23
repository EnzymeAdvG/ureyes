import numpy as np
import matplotlib.pyplot as plt
import cv2

from labelrecognition_iqa.brisque import calculate_image_quality_score, calculate_mscn_coefficients, \
                                 calculate_pair_product_coefficients, \
                                 calculate_brisque_features, plot_histogram

def main():


    plt.rcParams["figure.figsize"] = 12, 9

    gray_image = cv2.imread('.\images\expiration_date_rotate.jpg',0)
    gray_image_normalized = cv2.normalize(gray_image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    mscn_coefficients = calculate_mscn_coefficients(gray_image_normalized, 7, 7/6)
    coefficients = calculate_pair_product_coefficients(mscn_coefficients)

    plt.rcParams["figure.figsize"] = 12, 11

    for name, coeff in coefficients.items():
        plot_histogram(coeff.ravel(), name)

    plt.axis([-2.5, 2.5, 0, 1.05])
    plt.legend()
    plt.savefig('Coefficientes_histogram.png')
    plt.show()

    brisque_features = calculate_brisque_features(gray_image_normalized, kernel_size=7, sigma=7/6)
    downscaled_image = cv2.resize(gray_image_normalized, None, fx=1/2, fy=1/2, interpolation = cv2.INTER_CUBIC)
    downscale_brisque_features = calculate_brisque_features(downscaled_image, kernel_size=7, sigma=7/6)
    brisque_features = np.concatenate((brisque_features, downscale_brisque_features))

    score = calculate_image_quality_score(brisque_features)

    print(score)

if __name__ == '__main__':
    main()
