# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import cv2
import time
import sys
import os
import socket

class YOLO_TF:
	fromfile = None # 매개 변수로 파일을 입력 받는다
	tofile_img = 'test/output.jpg' # 저장할 이미지 경로
	tofile_txt = 'test/output.txt' # After Detecting, ouput : x,y,w,h,lable 저장할 텍스트 파일 경로
	# checking variable
	imshow = True
	filewrite_img = False
	filewrite_txt = False
	disp_console = True
	#
	weights_file = 'weights/YOLO_small.ckpt' # weight가 저장된 TensorFlow 모델 checkpint : CNN YOLO Model
	# Learning Constant
	alpha = 0.1
	threshold = 0.2
	iou_threshold = 0.5
	num_class = 20
	num_box = 2
	grid_size = 7
	# Classification 분류 클래스
	classes =  ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train","tvmonitor"]

	# Training Parameter
	learning_rate = 0.00001 # training
	training_iterate = 300
	batch_size = 1
	display_step = 1

	w_img = 640 # 이미지 가로
	h_img = 480 # 이미지 높이

	# TCP/IP Socket
	TCP_IP = '192.168.0.51'
	TCP_PORT = 9999
	# socket open
	sock = socket.socket()
	sock.connect((TCP_IP, TCP_PORT))

	# Function : 초기화 함수
	def __init__(self,argvs = []):
		self.argv_parser(argvs)
		self.build_networks() # YOLO Model의 CNN 생성


		# rtsp
		# file_path = "rtsp://61.108.209.254/L01060/video1"
		file_path = "input.avi"
		# test video
		self.read_video(file_path)

		if self.fromfile is not None: self.detect_from_file(self.fromfile)

	# Function : 명령어 입력시 argv 파라미터 처리 함수
	def argv_parser(self,argvs):
		for i in range(1,len(argvs),2):
			if argvs[i] == '-fromfile' : self.fromfile = argvs[i+1]
			if argvs[i] == '-tofile_img' : self.tofile_img = argvs[i+1] ; self.filewrite_img = True
			if argvs[i] == '-tofile_txt' : self.tofile_txt = argvs[i+1] ; self.filewrite_txt = True
			if argvs[i] == '-imshow' :
				if argvs[i+1] == '1' :self.imshow = True
				else : self.imshow = False
			if argvs[i] == '-disp_console' :
				if argvs[i+1] == '1' :self.disp_console = True
				else : self.disp_console = False

	# Function : YOLO Model의 CNN(Convolutional Neural Network)생성
	def build_networks(self):
		if self.disp_console : print("Building YOLO_small graph...")
		self.x = tf.placeholder('float32',[None,448,448,3])
		self.conv_1 = self.conv_layer(1,self.x,64,7,2)
		self.pool_2 = self.pooling_layer(2,self.conv_1,2,2)
		self.conv_3 = self.conv_layer(3,self.pool_2,192,3,1)
		self.pool_4 = self.pooling_layer(4,self.conv_3,2,2)
		self.conv_5 = self.conv_layer(5,self.pool_4,128,1,1)
		self.conv_6 = self.conv_layer(6,self.conv_5,256,3,1)
		self.conv_7 = self.conv_layer(7,self.conv_6,256,1,1)
		self.conv_8 = self.conv_layer(8,self.conv_7,512,3,1)
		self.pool_9 = self.pooling_layer(9,self.conv_8,2,2)
		self.conv_10 = self.conv_layer(10,self.pool_9,256,1,1)
		self.conv_11 = self.conv_layer(11,self.conv_10,512,3,1)
		self.conv_12 = self.conv_layer(12,self.conv_11,256,1,1)
		self.conv_13 = self.conv_layer(13,self.conv_12,512,3,1)
		self.conv_14 = self.conv_layer(14,self.conv_13,256,1,1)
		self.conv_15 = self.conv_layer(15,self.conv_14,512,3,1)
		self.conv_16 = self.conv_layer(16,self.conv_15,256,1,1)
		self.conv_17 = self.conv_layer(17,self.conv_16,512,3,1)
		self.conv_18 = self.conv_layer(18,self.conv_17,512,1,1)
		self.conv_19 = self.conv_layer(19,self.conv_18,1024,3,1)
		self.pool_20 = self.pooling_layer(20,self.conv_19,2,2)
		self.conv_21 = self.conv_layer(21,self.pool_20,512,1,1)
		self.conv_22 = self.conv_layer(22,self.conv_21,1024,3,1)
		self.conv_23 = self.conv_layer(23,self.conv_22,512,1,1)
		self.conv_24 = self.conv_layer(24,self.conv_23,1024,3,1)
		self.conv_25 = self.conv_layer(25,self.conv_24,1024,3,1)
		self.conv_26 = self.conv_layer(26,self.conv_25,1024,3,2)
		self.conv_27 = self.conv_layer(27,self.conv_26,1024,3,1)
		self.conv_28 = self.conv_layer(28,self.conv_27,1024,3,1)
		self.fc_29 = self.fc_layer(29,self.conv_28,512,flat=True,linear=False)
		self.fc_30 = self.fc_layer(30,self.fc_29,4096,flat=False,linear=False)
		#skip dropout_31
		self.fc_32 = self.fc_layer(32,self.fc_30,1470,flat=False,linear=True)
		self.sess = tf.Session() # A class for running TensorFlow operations
		self.sess.run(tf.initialize_all_variables()) # Run operations and evaluates tensors in fetches.
		self.saver = tf.train.Saver() # A class Saves and restores variables.
		self.saver.restore(self.sess,self.weights_file) # Restores previously saved variables. Load!!
		if self.disp_console : print("Loading complete!" + '\n')

	# Function : Convolution Layer : Filter를 사용해 주어진 image의 적절한 feature(Edge, )를 추출한다.
	def conv_layer(self,idx,inputs,filters,size,stride):
		channels = inputs.get_shape()[3] # depth 3 : r,g,b
		# tf.Variable : Variable Declaration
		# tf.truncatd_normal : Outputs random values from a truncated normal distribution. 랜덤 변수
		weight = tf.Variable(tf.truncated_normal([size,size,int(channels),filters], stddev=0.1))
		# tf.constant : Creates a constant tensor
		biases = tf.Variable(tf.constant(0.1, shape=[filters]))

		# padding : input의 경계면의 정보를 살림.
		pad_size = size//2
		pad_mat = np.array([[0,0],[pad_size,pad_size],[pad_size,pad_size],[0,0]])
		# tf.pad : Pads a tensor.
		inputs_pad = tf.pad(inputs,pad_mat)

		# tf.nn.conv2d : Computes a 2-D Convolution given 4-D input and filter tensors.
		# tf.nn.conv2d : 4-D input과 filter Tensor를 이용해 2-D Convolution을 계산한다.
		conv = tf.nn.conv2d(inputs_pad, weight, strides=[1, stride, stride, 1], padding='VALID',name=str(idx)+'_conv')
		# tf.add(x,y) : Returns x+y element-wise
		conv_biased = tf.add(conv,biases,name=str(idx)+'_conv_biased')	# conv(inputs_pad,weights) + bias
		if self.disp_console : print('    Layer  %d : Type = Conv, Size = %d * %d, Stride = %d, Filters = %d, Input channels = %d' % (idx,size,size,stride,filters,int(channels)))
		# tf.maximum : Returns the max of x,y
		"""
		tanh : sigmoid 함수를 재활용하기 위한 함수, sigmoid의 범위를 -1에서 1로 확장
		ReLU : max(0,x) 음수에 대해서 0으로 처리
		Leaky ReLU : ReLU의 변형으로 음수에 대해 1/10로 값을 줄여서 사용
		"""
		return tf.maximum(self.alpha*conv_biased,conv_biased,name=str(idx)+'_leaky_relu') # Leaky ReLU

	# Function : Pooling Layer(Sub-sampling) : Convolution Layer의 feature map을 압축한다.
	def pooling_layer(self,idx,inputs,size,stride):
		if self.disp_console : print('    Layer  %d : Type = Pool, Size = %d * %d, Stride = %d' % (idx,size,size,stride))
		# tf.nn.max_pool : Performs the max pooling on the input.
		return tf.nn.max_pool(inputs, ksize=[1, size, size, 1],strides=[1, stride, stride, 1], padding='SAME',name=str(idx)+'_pool')

	# Function : Fully-Connected Layer : feature map의 size가 작아지면서 전체를 대표하는 feature를 남겨 최적의 인식 결과를 만들어낸다
	def fc_layer(self,idx,inputs,hiddens,flat = False,linear = False):
		input_shape = inputs.get_shape().as_list()		
		if flat:
			dim = input_shape[1]*input_shape[2]*input_shape[3]
			# tf.transpose : Transpose matrix
			inputs_transposed = tf.transpose(inputs,(0,3,1,2))
			# tf.reshape(t,[-1]) : Reshape 1-D Matrix
			inputs_processed = tf.reshape(inputs_transposed, [-1,dim])
		else:
			dim = input_shape[1]
			inputs_processed = inputs
		# line 95,96,98
		weight = tf.Variable(tf.truncated_normal([dim,hiddens], stddev=0.1))
		biases = tf.Variable(tf.constant(0.1, shape=[hiddens]))	
		if self.disp_console : print('    Layer  %d : Type = Full, Hidden = %d, Input dimension = %d, Flat = %d, Activation = %d' % (idx,hiddens,int(dim),int(flat),1-int(linear)))
		if linear : return tf.add(tf.matmul(inputs_processed,weight),biases,name=str(idx)+'_fc')
		ip = tf.add(tf.matmul(inputs_processed,weight),biases) # (input * Weight) + biases
		return tf.maximum(self.alpha*ip,ip,name=str(idx)+'_fc')

	# Function : 실제 이미지를 numpy의 Array로 변환해 CNN 모델인 YOLO에 넣어 결과를 출력한다.
	def detect_from_cvmat(self,img):
		s = time.time() # time.time() : 현재 시간을 가져온다.
		self.h_img,self.w_img,_ = img.shape
		# cv2.resize() : Resize Image Size
		img_resized = cv2.resize(img, (448, 448)) # 448, 448 Resize
		# cv2.cvtColor() : Convert Image To Color-Space
		img_RGB = cv2.cvtColor(img_resized,cv2.COLOR_BGR2RGB) # RGB
		# np.asarray : Convert the input to an array
		img_resized_np = np.asarray( img_RGB ) # Image의 Color-Space를 Array로 변환한다.
		# np.zeros : Return a New array of given shape and type, filled with zeros.
		inputs = np.zeros((1,448,448,3),dtype='float32')
		inputs[0] = (img_resized_np/255.0)*2.0-1.0
		in_dict = {self.x: inputs}
		net_output = self.sess.run(self.fc_32,feed_dict=in_dict) # TensorFlow 연산 실행 : YOLO CNN에 image의 array를 넘겨 output 출력
		self.result = self.interpret_output(net_output[0]) # 나온 output에 대한 결과를 해석한다.
		self.show_results(img,self.result) # 이미지와 결과를 보여준다.
		strtime = str(time.time()-s) # 처음 시간과 현재 시간을 빼 걸린 시간을 구한다.
		if self.disp_console : print('Elapsed time : ' + strtime + ' secs' + '\n')

	# Function : Train, Test 이미지를 읽어와 Detecting 함수를 호출한다.
	def detect_from_file(self,filename):
		if self.disp_console : print('Detect from ' + filename)
		# cv2.imread : 파일로부터 이미지를 읽어온다.
		img = cv2.imread(filename)
		self.detect_from_cvmat(img)

	# Function : 읽어온 비디오의 프레임을 Detecting 함수를 호출한다
	def detect_from_frame(self, frame, index):
		self.filewrite_img = True
		self.tofile_img = "yolo_frame/yolo_frame%d.jpg"%index
		self.detect_from_cvmat(frame)

	# Function : 이미지를 
	def detect_from_crop_sample(self):
		self.w_img = 640
		self.h_img = 420
		f = np.array(open('person_crop.txt','r').readlines(),dtype='float32')
		inputs = np.zeros((1,448,448,3),dtype='float32')
		for c in range(3):
			for y in range(448):
				for x in range(448):
					inputs[0,y,x,c] = f[c*448*448+y*448+x]

		in_dict = {self.x: inputs}
		net_output = self.sess.run(self.fc_32,feed_dict=in_dict)
		self.boxes, self.probs = self.interpret_output(net_output[0])
		img = cv2.imread('person.jpg')
		self.show_results(self.boxes,img)

	# Function : CNN 모델을 통해 나온 결과값으로 Detecting한 Object의 정보를 해석한다.
	def interpret_output(self,output):
		probs = np.zeros((7,7,2,20))
		class_probs = np.reshape(output[0:980],(7,7,20))
		scales = np.reshape(output[980:1078],(7,7,2))
		boxes = np.reshape(output[1078:],(7,7,2,4))
		offset = np.transpose(np.reshape(np.array([np.arange(7)]*14),(2,7,7)),(1,2,0))

		boxes[:,:,:,0] += offset
		boxes[:,:,:,1] += np.transpose(offset,(1,0,2))
		boxes[:,:,:,0:2] = boxes[:,:,:,0:2] / 7.0
		boxes[:,:,:,2] = np.multiply(boxes[:,:,:,2],boxes[:,:,:,2])
		boxes[:,:,:,3] = np.multiply(boxes[:,:,:,3],boxes[:,:,:,3])
		
		boxes[:,:,:,0] *= self.w_img
		boxes[:,:,:,1] *= self.h_img
		boxes[:,:,:,2] *= self.w_img
		boxes[:,:,:,3] *= self.h_img

		for i in range(2):
			for j in range(20):
				probs[:,:,i,j] = np.multiply(class_probs[:,:,j],scales[:,:,i])

		filter_mat_probs = np.array(probs>=self.threshold,dtype='bool')
		filter_mat_boxes = np.nonzero(filter_mat_probs)
		boxes_filtered = boxes[filter_mat_boxes[0],filter_mat_boxes[1],filter_mat_boxes[2]]
		probs_filtered = probs[filter_mat_probs]
		classes_num_filtered = np.argmax(filter_mat_probs,axis=3)[filter_mat_boxes[0],filter_mat_boxes[1],filter_mat_boxes[2]] 

		argsort = np.array(np.argsort(probs_filtered))[::-1]
		boxes_filtered = boxes_filtered[argsort]
		probs_filtered = probs_filtered[argsort]
		classes_num_filtered = classes_num_filtered[argsort]
		
		for i in range(len(boxes_filtered)):
			if probs_filtered[i] == 0 : continue
			for j in range(i+1,len(boxes_filtered)):
				if self.iou(boxes_filtered[i],boxes_filtered[j]) > self.iou_threshold : 
					probs_filtered[j] = 0.0
		
		filter_iou = np.array(probs_filtered>0.0,dtype='bool')
		boxes_filtered = boxes_filtered[filter_iou]
		probs_filtered = probs_filtered[filter_iou]
		classes_num_filtered = classes_num_filtered[filter_iou]

		result = []
		for i in range(len(boxes_filtered)):
			result.append([self.classes[classes_num_filtered[i]],boxes_filtered[i][0],boxes_filtered[i][1],boxes_filtered[i][2],boxes_filtered[i][3],probs_filtered[i]])

		return result

	# Function : 결과를 보여줌
	def show_results(self,img,results):
		img_cp = img.copy()
		if self.filewrite_txt :
			ftxt = open(self.tofile_txt,'w') # 작성할 파일을 쓰기 모드로 open
		for i in range(len(results)):
			x = int(results[i][1]) # Detecting한 Object의 가운데 점의 x 좌표
			y = int(results[i][2]) # Detecting한 Object의 가운데 점의 y 좌표
			w = int(results[i][3])//2 # Detecting한 Object의 width
			h = int(results[i][4])//2 # Detecting한 Object의 height
			if self.disp_console : print('    class : ' + results[i][0] + ' , [x,y,w,h]=[' + str(x) + ',' + str(y) + ',' + str(int(results[i][3])) + ',' + str(int(results[i][4]))+'], Confidence = ' + str(results[i][5]))
			if self.filewrite_img or self.imshow:
			    # cv2.rectangle : 사각형을 그린다
				cv2.rectangle(img_cp,(x-w,y-h),(x+w,y+h),(0,255,0),2) # Detecting한 Object의 가운데를 기준으로 사각형을 그린다.
				cv2.rectangle(img_cp,(x-w,y-h-20),(x+w,y-h),(125,125,125),-1) # Label
				cv2.putText(img_cp,results[i][0] + ' : %.2f' % results[i][5],(x-w+5,y-h-7),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1)
			if self.filewrite_txt :				
				ftxt.write(results[i][0] + ',' + str(x) + ',' + str(y) + ',' + str(w) + ',' + str(h)+',' + str(results[i][5]) + '\n')
		if self.filewrite_img : 
			if self.disp_console : print('    image file writed : ' + self.tofile_img)
			cv2.imwrite(self.tofile_img,img_cp)
		# Socket 통신으로 전송한다.
		if self.socket_transfer:
			size = len(results)
			self.sock.send(str(size).ljust(3))
			for i in range(size):
				x = int(results[i][1])  # Detecting한 Object의 가운데 점의 x 좌표
				y = int(results[i][2])  # Detecting한 Object의 가운데 점의 y 좌표
				w = int(results[i][3]) // 2  # Detecting한 Object의 width
				h = int(results[i][4]) // 2  # Detecting한 Object의 height
				self.socket_transfer_results(x,y,w,h)
		if self.imshow :
			cv2.imshow('YOLO_small detection',img_cp)
			cv2.waitKey(3000)
		if self.filewrite_txt : 
			if self.disp_console : print('    txt file writed : ' + self.tofile_txt)
			ftxt.close()

	def iou(self,box1,box2):
		tb = min(box1[0]+0.5*box1[2],box2[0]+0.5*box2[2])-max(box1[0]-0.5*box1[2],box2[0]-0.5*box2[2])
		lr = min(box1[1]+0.5*box1[3],box2[1]+0.5*box2[3])-max(box1[1]-0.5*box1[3],box2[1]-0.5*box2[3])
		if tb < 0 or lr < 0 : intersection = 0
		else : intersection =  tb*lr
		return intersection / (box1[2]*box1[3] + box2[2]*box2[3] - intersection)

	def training(self): # TODO add training function!
		if self.disp_console : print("Training YOLO ...")

		self.correct_prediction = tf.square(self.prediction - self.y)
		if self.disp_console : print("correct_prediction : ", self.correct_prediction)
		self.accuracy = tf.reduce_mean(self.correct_prediction) * 100
		if self.disp_console : print("accuracy : ", self.accuracy)

		optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.accuracy) # Adam Optimizer

		# Tensorflow 변수 초기화
		init = tf.initialize_all_variables()
		"""
		with tf.Session() as sess:
			sess.run(init)

			x_path = os.path.join('DATA',"CAR", 'yolo_out/')
			self.output_path = os.path.join('DATA', "CAR", 'yolo_out_train/')
			if not os.path.exists(self.output_path): # 디렉터리가 존재하는지 확인한다.
				os.mkdir(self.output_path) # 디렉터리를 만든다

			id = 0;

			# Keep Training until reach max iterations
			while id * self.batch_size < self.training_iterate:

				batch_xs = self.preprocess_training(x_path, self.batch_size, self.num_steps, id)

				if id % self.display_step == 0 :
					# Calculate batch loss
					loss = self.sess.run(self.accuracy, feed_dict={self.x: batch_xs, self.y: batch_ys, self.istate: np.zeros((self.batch_size, 2*self.num_input))})
					if self.disp_console: print "Iter " + str(id*self.batch_size) + ", Minibatch Loss= " + "{:.6f}".format(loss) #+ "{:.5f}".format(self.accuracy)

					total_loss += loss
				id += 1
				if self.disp_console: print(id)
			print('Optimization Finished!!')
			avg_loss = total_loss/id
			print "Avg loss: " + str(avg_loss)
			save_path = self.saver.save(sess, self.rolo_weights_file)
			print("Model saved in file: %s" % save_path)
		"""

	def preprocess_training(self, fold, batch_size, num_steps, id):
		paths = [os.path.join(fold, fn) for fn in next(os.walk(fold))[2]]
		paths = sorted(paths)
		st = id
		ed = id + batch_size * num_steps
		paths_batch = paths[st:ed]

		yolo_output_batch = []
		ct = 0

		for path in paths_batch :
			ct += 1
			yolo_output = np.load(path)
			yolo_output = np.reshape(yolo_output, 4102)
			yolo_output_batch.append(yolo_output)

		yolo_output_batch = np.reshape(yolo_output_batch, [batch_size * num_steps, 4102])

		return

	# Function : socket 통신으로 Detecting 결과인 x,y,w,h
	def socket_transfer_results(self, x, y, w, h):
		stringData='x:'+str(x)+',y:'+str(y)+',w:'+str(w)+',h:'+str(h) # MAX 27
		self.sock.send(stringData.ljust(27)) # 왼쪽 정렬 (비어있는 곳은 공백 처리)

	# Function : socket 통신으로 이미지를 전송한다.
	def socket_transfer_img(self, image):
		encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
		result, img_encode = cv2.imencode('.jpg', image, encode_param)

		data = np.array(img_encode)
		stringData = data.tostring()

		self.sock.send(str(len(stringData)).ljust(16)) # str.ljust(num) : num 만큼의 문자열 크기를 만들고 왼쪽 정렬한다
		self.sock.send(stringData)


	# Function : 파일의 확장자를 확인하여 video 인지 체크한다
	def is_video(self, file_path):
		if os.path.isfile(file_path) and os.path.splitext(file_path)[1][1:] in ['avi', 'mkv', 'mp4']:
			return True
		else:
			return False

	# Funtcion :  비디오를 읽어와 Frame으로 분할하여 CNN 모델을 호출하여 Detecting 한다
	def read_video(self, file_path):
		# RTSP 카메라로 전송일 경우 비디오 체크를 하지 않는다.
		if self.is_video(file_path):
			# 0 : Loacl
			capture = cv2.VideoCapture(file_path)

			# video width, height
			print('image width {}, height {}'.format(capture.get(3), capture.get(4)))
			index = 0

			while (capture.isOpened()): # capture 열려 있다면
				ret, frame = capture.read()

				if ret < 0:
					break

				frame = cv2.resize(frame, (800,600)) # frame을 resize 한다
				cv2.imshow('frame', frame) # frame을 보인다

				# frame 이미지를 저장한다
				# cv2.imwrite("frame/frame%d.jpg" % index, frame)

				# socket으로 이미지를 전송한다.
				self.socket_transfer = True
				self.socket_transfer_img(frame)

				self.detect_from_frame(frame, index)

				index = index+1

		# cap release
		capture.release()

def main(argvs):
	yolo = YOLO_TF(argvs)
	cv2.waitKey(1000)


if __name__=='__main__':	
	main(sys.argv)
