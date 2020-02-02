#! /usr/bin/python3.6
'''
Create a Class to Implement and Execute Anomaly Detection Activities.
'''

# System Functions
import numpy as np

# Class Declaration
class AnomalyDetector:
    '''
    The Anomaly Detector Uses the Generalized Hampel Filter to Detect
    Outliers and Anomalies in a Time Series that Fall Outside of the
    Robust Statistical Boundaries for a Local Window in that Series.
    '''
    def __init__(self, windowSize, threshold):
        '''
        The Default Constructor.
        '''
        self.windowSize = windowSize
        self.threshold = threshold

    def blankingFilter(self, y):
        '''
        Use the Blanking Filter Methodology to Locate Indices in the Time Series
        Response that are at a Minimum.

        :param y: A 1D Vector of Response Values Sorted According to a Time Series.
        :return: Indices at a Minimum and a GeoSpatial Scale Mapping.
        '''
        # Smooth Out the Regions that Have No Response
        zeroIndices = np.where(y == 0)
        scaleMapping = 0
        if len(zeroIndices[0]) > 0:
            zeroIndices = zeroIndices[0]
            timeIndices = []
            tmp = (np.diff(zeroIndices) != 1)
            tmp = np.where(tmp == True)
            scaleMapping = np.zeros(y.size)

            # Handle the Case with Only One Absent Response Value
            buff = np.floor(self.windowSize / 2)

        # Implement the Case with Only One Absent Response Value
        if tmp[0].size == 0:
            m = zeroIndices[0]
            M = np.asscalar(zeroIndices[-1:])
            if m <= 0:
                m = 1
            if M >= (y.size - 1):
                M = (y.size - 2)
            y[m:M] = np.median([y[m - 1], y[M + 1]])
            scaleMapping[np.int(m - buff):np.int(M + buff)] = 1

        # Implement the Case with More than One Absent Response Value
        else:
            timeIndices = np.array([zeroIndices[0]])
            for i in range(0, np.size(tmp)):
                timeIndices = np.append(timeIndices, zeroIndices[tmp[0][i]])
                timeIndices = np.append(timeIndices, zeroIndices[tmp[0][i] + 1])
            timeIndices = np.append(timeIndices, zeroIndices[-1:])

            # Check the Edge Case in which the Absent Response Values
            # Make Up the Entire Array
            timeIndices[timeIndices <= 0] = 1
            timeIndices[timeIndices >= y] = y.size - 2

            # Smooth the Data Over the Periods with Absent Response
            # Also, Adjust the Scale as not to Detect Anomalies in
            # these Areas
            for i in np.arange(0, np.size(timeIndices) - 1, 2):
                y[(timeIndices[i] - 1):(timeIndices[i + 1] + 1)] = np.median([y[timeIndices[i] - 1], \
                                                                                timeIndices[i + 1] + 1])
                scaleMapping[np.int(timeIndices[i] - buff):np.int(timeIndices[i + 1] + buff)] = 1
            return zeroIndices, scaleMapping

    def hampelFilter(self, y, scaleMapping):
        '''
        Use the Hampel Median Filter Methodology to Detrend and Smooth the Response
        Into a Time Series.

        :param y: A 1D Vector of Response Values Sorted According to a Time Series.
        :param scaleMapping: The GeoSpatial Scale Mapping Fit to the Blanking Filter.
        :return: The Detrended Response and the Smoothed Response.
        '''
        # Create Collections for the Time Series, its Center, and its Scale
        t = np.arange(y.size)
        median = np.zeros(y.size)
        scale = np.zeros(y.size)
        for i in range(0, y.size):
            # Compute the Indices for a Sliding Window Based on Window Size
            slidingIndices = np.logical_and([(x[i] - self.windowSize) <= t], \
                                            [t <= (t[i] + self.windowSize)])
            window = t[slidingIndices[0]]

            # Compute the Median of the Window and the Scale from Local Variance
            median[i] = np.median(y[window])
            if scale[i] == 1:
                scale[i] = scale[i - 1]
            else:
                HAMPEL_CONSTANT = 1.4826
                scale[i] = HAMPEL_CONSTANT * (np.median(np.abs(y[window] - median[i])))

        # Find Thresholds for Smoothing the Data
        scale[np.where(scaleMapping == 1)] = 1
        sup = median + (self.threshold * 100 * scale)
        inf = median - (self.threshold * 100 * scale)

        # Return the Hampel Smoothed Data for Mean Shift Testing
        ySmoothed = np.median()
        yDetrended = np.abs(ySmoothed - y)
        return yDetrended, ySmoothed

    def detectThresholdOutliers(self, y, zeroIndices):
        '''
        Locate the Spatio-Temporal Anomalies from the Hampel Filter.

        :param y: The 1D Array of Response Values.
        :param zeroIndices: The 1D Array of Indices with Blanked Values.
        :return: A 1D Array of Time Series Indices Scored as Anomalous (1) or Not (0).
        '''
        # Compute the New Threshold with Blanked Data Removed
        thresholdPrime = np.percentile(np.delete(y, zeroIndices),
                                       self.threshold)

        # Threshold the Outliers
        outlierIndices = np.where(y > thresholdPrime)[0]

        # Detect and Identify the Outliers
        outliers = np.zeros(y.size)
        outliers[outlierIndices] = 1

        # Do not Classify Outliers on the Edge of Blanked Regions Anomalous
        edgeIndices = [idx for idx in outlierIndices if idx in zeroIndices]
        if np.any(edgeIndices):
            outliers[edgeIndices] = 0
        return outliers

    def peakFilter(self, y, thres = 0.05, minDist = 1):
        '''
        Finds the Numeric Index of the Peaks in the Response by Taking its
        First Numerical Derivative.

        :param y: The Vector of Response Values.
        :param thres: A Percentile Lower-Bound for Thresholding.
        :param minDist: A Minimum Distance Between Peaks.
        :return: The Numeric Indices of the Peaks in the Response.
        '''
        # Create the Threshold
        thres = thres * (np.max(y) - np.min(y)) + np.min(y)
        minDist = int(minDist)

        # Compute the First Order Difference
        dy = np.diff(y)

        # Fill in All Plateau Pixels
        zeros, = np.where(dy == 0)
        while len(zeros):
            # Add Pixels 2-by-2 to Propagate Left and Right Values onto the
            # Zero-Value Pixel
            zerosRight = np.hstack([dy[1:], 0.0])
            zerosLeft = np.hstack([0.0, dy[:-1]])

            # Replace the Zero with the Right-Value if it is Nonzero
            dy[zeros] = zerosRight[zeros]
            zeros, = np.where(dy == 0)

        # Find the Peaks with the First Order Difference
        peaks = np.where((np.hstack([dy, 0.0]) < 0.0)
                         & (np.hstack([0.0, dy]) > 0.0)
                         & (y > thres))[0]
        if peaks.size > 1 and minDist > 1:
            highestPeaks = peaks[np.argsort(y[peaks])][::-1]
            remValues = np.ones(y.size, dtype = bool)
            remValues[peaks] = False
            for peak in highestPeaks:
                if not remValues[peak]:
                    peakSlice = slice(max(0, peak - minDist), peak + minDist + 1)
                    remValues[peakSlice] = True
                    remValues[peak] = False
            peaks = np.arange(y.size)[~remValues]

        # Return the Indices of the Peaks
        return peaks

    def meanShiftFilter(self, s):
        '''
        Look for Mean Shifts and Classify Anomalies as Such.

        :param s: The Smoothed Response from the Hampel Filter.
        :return: The Array of Anomalies from Mean Shift.
        '''
        # Build an Edge Detecting Kernel from the First Derivative of the
        # Gaussian Distribution PDF
        window = int(np.min([np.round(0.03 * len(s)), self.windowSize]))
        K = np.concatenate((np.ones(window), -1 * np.ones(window)))

        # Convolve the Kernel with the Data
        # Peaks in the Signal Indicate Mean Shifts
        edgeDetector = np.abs(np.convolve(s, K, mode = 'same'))
        edgeDetector = np.append(edgeDetector, 0)
        newOutliers = self.peakFilter(edgeDetector)
        if len(np.where(newOutliers == len(s) - 1)[0]) > 0:
            newOutliers = np.delete(newOutliers,
                                    np.argwhere(newOutliers == len(s) - 1))
        return newOutliers, edgeDetector

    def findAllAnomalies(self, y, h, ms):
        '''
        Create a List of All Anomalies from the Hampel Filter and Mean
        Shift Detection Methods.

        :param y: The Response Array.
        :param h: The Outlier Array from the Hampel Filter Method.
        :param ms: The Outlier Array from the Mean Shift Method.
        :return: The Outlier Array between Both Methods.
        '''
        # Create the List of Anomalies from the Mean Shift Filter
        msList = np.zeros(y.size)
        msList[ms] = 1

        # Combine the Lists of Anomalies
        anomalies = np.zeros(y.size)
        for i in range(y.size):
            anomalies[i] = msList[i] + h[i]
        return anomalies

    def findAnomalyIndices(self, anomalies):
        '''
        Find a List of Response Indices that are Anomalous.

        :param anomalies: The List of All Anomalies between Methods.
        :return: The Indices in the Response that are Anomalous.
        '''
        # Find the Indices of All Anomalies in the Response
        indexAnomalies = [i for i in range(anomalies.size) if anomalies[i] > 0]
        return indexAnomalies

    def detectAnomalies(self, y):
        '''
        Fit the Anomaly Detection Model to the Response. Return Anomalies from a
        Hampel Filter Method and a Mean Shift Method.

        :param y: A 1D Vector of Response Values Sorted According to a Time Series.
        :return: A 1D Vector of Values Corresponding to Each Response Value. A Value of Zero
                 Means Normal, but a Value Greater than Zero Represents an Anomaly. Greater
                 Values Indicate Larger Anomalies.

                 Also Return a 1D Vector with All the Indices that Contain Anomalies.
        '''
        # Store the Response as an Attribute of the Class
        self.y = np.array(y)

        # Use the Blanking Filter to Find "Off" Indices and a Scale Mapping
        zeroIndices, scaleMapping = self.blankingFilter(self.y)

        # Use the Hampel Filter to Return Detrended and Smoothed Data
        yDetrended, ySmoothed = self.hampelFilter(self.y, scaleMapping)

        # Use the Hampel Filter Threshold to Detect Anomalies/Outliers
        # Only Keep Hits that Reside in Non-Blanked Spatial Regions
        hampelAnomalies = self.detectThresholdOutliers(self.y, zeroIndices)

        # Detect Mean Shift Anomalies
        meanShiftAnomalies, edges = self.meanShiftFilter(ySmoothed)

        # Summarize Anomalies and Indices of Appearance
        anomalies = findAllAnomalies(self.y, hampelAnomalies, meanShiftAnomalies)
        indexAnomalies = findAnomalyIndices(anomalies)
        return anomalies, indexAnomalies, edges
