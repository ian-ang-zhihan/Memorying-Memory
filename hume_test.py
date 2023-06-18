import asyncio
# import the opencv library
import cv2
import datetime

from hume import HumeStreamClient
from hume.models.config import FaceConfig

def check_emotion_and_timestamp(emotion_data, start_time):
    positive_emotions = ['admiration', 'adoration', 'aesthetic appreciation', 'amusement', 'awe', 'triumph',
                      'contentment', 'determination', 'ecstasy', 'entrancement', 'excitement', 'interest',
                      'joy', 'love', 'relief', 'pride', 'satisfaction', 'surprise (positive)', 'sympathy']
    
    sad_emotions = ['anxiety', 'boredom', 'disappointment', 'disapproval', 'doubt', 'guilt', 'pain', 'sadness', 'shame', 'tiredness']

    duration = datetime.datetime.now() - start_time
    duration_seconds = int(duration.total_seconds())

    for emotion in emotion_data:
        emotion_name = emotion['name'].lower()
        emotion_score = emotion['score']

        if emotion_name in positive_emotions:
                img = cv2.imread("happy.jpg") # Add path to your image
                window = 'Joy Image'
        elif emotion_name in sad_emotions:
                img = cv2.imread("sad.jpg") # Add path to your image
                window = 'Sad Image'

        if emotion_score > 0.70:
            current_time = datetime.datetime.now()
            print(f"Emotion {emotion_name} exceeded 0.70 at {current_time}, camera has been on for {duration_seconds} seconds.")

            cv2.imshow(window, img)
            cv2.waitKey(1000) # Show the image for 1 second
            cv2.destroyWindow(window)

async def main():
    client = HumeStreamClient("KDshbbSeIuVjzUVn6cGBmmOT8DUwpEVWOSOrongsA9gh730U")
    config = FaceConfig(identify_faces=True)
    async with client.connect([config]) as socket:
        # define a video capture object
        vid = cv2.VideoCapture(0)
        start_time = datetime.datetime.now()

        while(True):
        
            # Capture the video frame
            # by frame
            ret, frame = vid.read()
        
            # Display the resulting frame
            cv2.imshow('frame', frame)
            
            # Saves the frames with frame-count
            cv2.imwrite("frame0.jpg", frame)

            # Send the image to Hume API and get the result
            result = await socket.send_file("frame0.jpg")
            # Check if any faces are detected
            if 'predictions' in result.get('face', {}):
                # Extract emotion data of the first face detected
                emotion_data = result['face']['predictions'][0]['emotions']
                check_emotion_and_timestamp(emotion_data, start_time)
            else:
                print("No faces detected in the frame.")

            
            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()


asyncio.run(main())


