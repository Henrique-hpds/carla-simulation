import cv2
import os

def img2vid(image_folder, output_video, fps=30):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()  # Garante a ordem correta das imagens
    
    if not images:
        print("Nenhuma imagem PNG encontrada na pasta.")
        return
    
    first_image = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = first_image.shape
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec alternativo
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)
    
    video.release()
    print(f"Vídeo salvo como {output_video}")