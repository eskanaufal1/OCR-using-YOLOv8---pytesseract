import torch
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO

class YOLOv5Detector:
    def __init__(self, model_path="yolov5s.pt", conf_thres=0.25, iou_thres=0.45):
        """
        Initialize YOLOv5 detector
        Args:
            model_path: Path to model weights (.pt file)
            conf_thres: Confidence threshold
            iou_thres: NMS IoU threshold
        """
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        
        # Load model
        try:
            self.model = YOLO(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    def detect_image(self, image_path, save_dir='runs/detect'):
        """
        Detect objects in image
        Args:
            image_path: Path to image or numpy array
            save_dir: Directory to save results
        Returns:
            results: List of detections with coordinates and class info
        """
        try:
            # Run inference
            results = self.model.predict(
                stream=True,
                source=image_path,
                conf=self.conf_thres,
                iou=self.iou_thres,
                save=True,
                save_dir=save_dir
            )
            
            # Process results
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    
                    # Get class and confidence
                    conf = float(box.conf[0].cpu().numpy())
                    cls = int(box.cls[0].cpu().numpy())
                    cls_name = result.names[cls]
                    
                    detection = {
                        'bbox': [int(x1), int(y1), int(x2), int(y2)],
                        'class': cls_name,
                        'confidence': conf
                    }
                    detections.append(detection)
            
            return detections
            
        except Exception as e:
            print(f"Error during detection: {e}")
            return []
    
    def detect_video(self, source=0, save_dir='runs/detect'):
        """
        Detect objects in video
        Args:
            source: Video path or camera index (0 for webcam)
            save_dir: Directory to save results
        """
        try:
            # Run inference on video
            results = self.model.predict(
                source=source,
                conf=self.conf_thres,
                iou=self.iou_thres,
                show=True,
                save=True,
                save_dir=save_dir
            )
            
        except Exception as e:
            print(f"Error during video detection: {e}")

def crop_image(img_path, bbox):
    # Membaca gambar menggunakan OpenCV
    image = cv2.imread(img_path)
    
    print("image_path =", img_path)
    if image is None:
        print("Gambar tidak ditemukan!")
        return None

    # Mengambil dimensi gambar
    height, width, _ = image.shape

    # bbox format: [x_center, y_center, width, height] relatif terhadap ukuran gambar
    x_center, y_center, w, h = bbox
    print(f"x_center = {x_center}, y_center = {y_center}, w = {w}, h = {h}")

    # Memotong gambar berdasarkan koordinat bbox
    cropped_image = image[int(y_center):int(h), int(x_center):int(w)]
    image_bbox = cv2.rectangle(image, (int(x_center), int(y_center)), (int(w), int(h)), (0, 255, 0), 2)
    cv2.imshow("Cropped Image", cropped_image)
    cv2.imshow("Image with Bounding Box", image_bbox)
    # Menunggu penekanan tombol (0 berarti menunggu tanpa batas waktu)
    cv2.waitKey(0)

    # # Menutup semua jendela OpenCV
    # cv2.destroyAllWindows()
    return cropped_image, image_bbox

def save_cropped_image(cropped_image, output_path):
    # Menyimpan gambar hasil pemotongan
    if cropped_image is not None:
        cv2.imwrite(output_path, cropped_image)
        # cv2.imshow("Cropped Image", cropped_image)
        # cv2.waitKey(0)
        print(f"Gambar berhasil disimpan di {output_path}")
    else:
        print("Gambar tidak dipotong.")

def main():
    # Example usage
    try:
        # Initialize detector
        detector = YOLOv5Detector(
            model_path="license_plate_detector.pt",
            conf_thres=0.25,
            iou_thres=0.45
        )
        
        # Image detection example
        print("Running image detection...")
        image_path = "license-plate.jpg"  # Replace with your image path
        detections = detector.detect_image(image_path)
        
        # Print results
        print("\nDetected objects:")
        print(detections)
        for det in detections:
            print(f"Class: {det['class']}")
            print(f"Confidence: {det['confidence']:.2f}")
            print(f"Bounding box: {det['bbox']}")
            print("---")
        image='license-plate.jpg'
        output_path = 'cropped_image.jpg'  # Ganti dengan path untuk menyimpan gambar hasil crop
        bbox = det['bbox']  # Misal bbox [x_center, y_center, width, height] relatif terhadap ukuran gambar

        path = 'license-plate.jpg'

       
        # # Memotong gambar
        cropped_image, image_bbox = crop_image(img_path=path, bbox=bbox)

        # # Menyimpan gambar yang telah dipotong
        save_cropped_image(cropped_image, output_path)
        save_cropped_image(image_bbox, "bbox.jpg")
        
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()