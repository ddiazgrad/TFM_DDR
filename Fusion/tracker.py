import numpy as np 
from kalmanFilter import KalmanFilter
from scipy.optimize import linear_sum_assignment
from collections import deque


class Tracks(object):
	"""docstring for Tracks"""
	def __init__(self, detection, trackId,my_track):
		super(Tracks, self).__init__()
		self.KF = KalmanFilter()
		self.KF.predict()
		self.contador = 0
		self.my_track = my_track
		self.KF.correct(np.matrix(detection).reshape(2,1))
		self.trace = deque(maxlen=10)
		self.prediction = detection.reshape(1,2)
		self.trackId = trackId
		self.skipped_frames = 0

	def predict(self,detection):
		self.prediction = np.array(self.KF.predict()).reshape(1,2)
		self.KF.correct(np.matrix(detection).reshape(2,1))


class Tracker(object):
	"""docstring for Tracker"""
	def __init__(self, dist_threshold, max_frame_skipped):
		super(Tracker, self).__init__()
		self.dist_threshold = dist_threshold
		self.max_frame_skipped = max_frame_skipped
		self.trackId = 0
		self.tracks = {}

	def update(self, detections,my_data):
		if len(self.tracks) == 0:
			for i in range(detections.shape[0]):
				track = Tracks(detections[i], self.trackId,my_data[i])
				self.tracks[self.trackId] =track
				self.trackId +=1
				# self.tracks.append(track)
		N = len(self.tracks.keys())
		M = len(detections)
		if (M<N):
			new_row = np.full((1, detections.shape[1]), 99999999999)
			detections = np.vstack((detections, new_row))
		cost = []
		assignment = {}
		for i in self.tracks.keys():
			assignment [i] = {"assign": -1, "cost":-1, "contador":self.tracks[i].contador}
			self.tracks[i].contador+=1
			try:
				diff = np.linalg.norm(self.tracks[i].prediction - detections.reshape(-1,2), axis=1)
			except:
				diff = None
			cost.append(diff)
			
		cost = np.array(cost)
		row, col = linear_sum_assignment(cost)
		for ppp in range(len(row)):
			row[ppp] = list(self.tracks.keys())[ppp]

		for i in range(len(row)):
			assignment[row[i]]["assign"] = col[i]
		
		counter = 0
		for i in assignment.keys():
			if assignment[i]["assign"] != -1:
				assignment[i]["cost"] = cost[counter][assignment[i]["assign"]]
				if ((cost[counter][assignment[i]["assign"]] > self.dist_threshold) and assignment[i]["contador"]>5):
					assignment[i]["assign"] = -1
					self.tracks[i].skipped_frames +=1
				else:
					self.tracks[i].skipped_frames +=1

			else:

				self.tracks[i].skipped_frames +=1
			counter +=1


		del_tracks = []
		for i in self.tracks.keys():
			if self.tracks[i].skipped_frames > self.max_frame_skipped :
				del_tracks.append(i)
		if len(del_tracks) > 0:
			for i in range(len(del_tracks)):
				del self.tracks[del_tracks[i]]
				del assignment[del_tracks[i]]

	
		for i in range(M):
			if i not in assignment and M>len(assignment):
		
				track = Tracks(detections[i], self.trackId,my_data[i])
				self.tracks[self.trackId] =track
				self.trackId +=1




		for i in assignment.keys():
			if(assignment[i]["assign"] != -1):
				self.tracks[i].skipped_frames = 0
				self.tracks[i].predict(detections[assignment[i]["assign"]])
			self.tracks[i].trace.append(self.tracks[i].prediction)


		for i in assignment.keys():
			try:
				self.tracks[assignment[i]["assign"]].my_track["sensor"] = my_data[i]["sensor"]
			except:
				pass



