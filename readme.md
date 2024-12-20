OCR Teks Pengenalan Plat Nomor Kendaraan dengan Pra-Pemrosesan Gambar
Aplikasi ini menggunakan Tesseract OCR untuk mengekstraksi teks dari gambar, khususnya untuk mengenali plat nomor kendaraan. Beberapa teknik pra-pemrosesan gambar seperti konversi ke grayscale, thresholding, deteksi tepi, pembukaan, dan koreksi kemiringan diterapkan untuk meningkatkan kualitas gambar sebelum ekstraksi teks.

Deskripsi
Proyek ini bertujuan untuk membangun sistem deteksi plat nomor kendaraan menggunakan Optical Character Recognition (OCR) dengan Tesseract OCR dan beberapa teknik pemrosesan citra dari OpenCV. Sistem ini mampu memproses gambar, menghilangkan noise, memperbaiki kemiringan gambar, dan mengekstrak teks dari plat nomor kendaraan.

Fitur utama:

Pra-pemrosesan gambar: Menggunakan berbagai teknik seperti konversi grayscale, thresholding, deteksi tepi, pembukaan, dan koreksi kemiringan.
Ekstraksi teks: Menggunakan Pytesseract, wrapper Python untuk Tesseract OCR, untuk membaca teks dari gambar.
Visualisasi: Menampilkan bounding box di sekitar karakter yang terdeteksi untuk memverifikasi hasil OCR.
Fitur
Mengubah gambar berwarna menjadi gambar grayscale untuk meningkatkan kualitas pemrosesan.
Menggunakan teknik thresholding dan operasi morfologi (opening, dilation, erosion) untuk membersihkan gambar dari noise.
Deteksi tepi dengan metode Canny Edge Detection untuk menonjolkan kontur.
Koreksi kemiringan untuk menyesuaikan gambar yang miring atau tidak rata.
Ekstraksi teks dengan Pytesseract dan menampilkan hasilnya dalam bentuk teks.
Menampilkan bounding box pada karakter yang terdeteksi untuk memverifikasi hasil OCR.
Prasyarat
Sebelum menggunakan aplikasi ini, Anda perlu menginstal beberapa pustaka berikut:

Tesseract OCR: Untuk pengenalan teks pada gambar.
OpenCV: Untuk pemrosesan gambar.
NumPy: Untuk manipulasi array dan matriks.
Pytesseract: Wrapper Python untuk Tesseract OCR.
Langkah-langkah Instalasi
Instalasi Tesseract OCR

Unduh dan instal Tesseract OCR dari tautan resmi Tesseract.

Setelah menginstal Tesseract, pastikan untuk menambahkan path instalasi ke sistem Anda. Pada Windows, path default-nya adalah:
makefile
Copy code
C:\Program Files\Tesseract-OCR\tesseract.exe
Instalasi Pustaka Python

Untuk menginstal pustaka yang diperlukan, jalankan perintah berikut:

bash
Copy code
pip install pytesseract opencv-python numpy
Penggunaan
1. Menyiapkan Gambar
Gambar yang akan diproses harus berada dalam format .jpg atau .png. Gambar tersebut bisa berupa gambar plat nomor kendaraan atau gambar dengan teks yang ingin diekstraksi.

2. Kode Utama
Berikut adalah cara menggunakan aplikasi ini untuk mengekstraksi teks dari gambar.

python
Copy code
import cv2
import pytesseract
from pytesseract import Output
import numpy as np

# Menentukan lokasi pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Fungsi pra-pemrosesan gambar
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.medianBlur(image, 5)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)
    
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def canny(image):
    return cv2.Canny(image, 100, 200)

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# Membaca gambar
image_ = cv2.imread('cropped_image.jpg')

# Pra-pemrosesan gambar
gray = get_grayscale(image_)
thresh = thresholding(gray)
opening = opening(gray)
canny = canny(gray)
deskewed = deskew(canny)

# Memilih gambar yang akan diproses
chosen_image = opening

# Ekstraksi teks menggunakan pytesseract
extracted_text = pytesseract.image_to_string(chosen_image)
print("Teks yang diekstrak:")
print(extracted_text)

# Menampilkan bounding box pada karakter
h, w, c = image_.shape
boxes = pytesseract.image_to_boxes(chosen_image)
for b in boxes.splitlines():
    b = b.split(' ')
    image_ = cv2.rectangle(image_, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# Menampilkan gambar dengan bounding box
cv2.imshow('img', image_)
cv2.waitKey(0)
3. Penjelasan Alur Kerja
Gambar dibaca menggunakan cv2.imread().
Beberapa metode pra-pemrosesan diterapkan untuk mempersiapkan gambar agar lebih mudah diproses oleh Tesseract.
Ekstraksi teks dilakukan dengan menggunakan pytesseract.image_to_string().
Bounding box digambar di sekitar karakter yang terdeteksi menggunakan pytesseract.image_to_boxes().
Gambar yang diubah kemudian ditampilkan dengan OpenCV menggunakan cv2.imshow().
Kontribusi
Jika Anda ingin berkontribusi pada proyek ini, Anda dapat melakukan hal berikut:

Fork repositori ini.
Buat branch baru untuk perbaikan atau penambahan fitur.
Kirimkan pull request dengan penjelasan mengenai perubahan yang telah dilakukan.

source=https://github.com/Muhammad-Zeerak-Khan/Automatic-License-Plate-Recognition-using-YOLOv8.git
