import os
import random
import pygame

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('png')):
            img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
            images.append(img)
    return images

def display_images(screen, images, num_images=12, blend_mode=pygame.BLEND_RGBA_ADD):
    
    screen.fill((200, 200, 10))  # Light background
    for _ in range(num_images):
        img = random.choice(images)
        img_width, img_height = img.get_width(), img.get_height()
        max_x = max(0, screen.get_width() - img_width)
        max_y = max(0, screen.get_height() - img_height)
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        
        # Apply random opacity
        opacity = random.randint(100, 255)
        img_with_opacity = img.copy()
        img_with_blend = img.copy()
        #img_with_opacity=blurSurf(img_with_opacity,1)
        img_with_opacity.fill((255, 255, 255, opacity*.8), None, special_flags=pygame.BLEND_RGBA_MULT)
        img_with_blend=img_with_opacity.copy()
        img_with_blend.fill((255, 255, 255, opacity), None, special_flags=pygame.BLEND_RGBA_MULT)

        screen.blit(img_with_blend,(x,y), special_flags=pygame.BLEND_RGBA_ADD)

        screen.blit(img_with_opacity, (x, y))#, special_flags=blend_mode)
def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

def main():
    TRANS_IMAGES_DIR = r"C:\\Users\\andre\\Desktop\\onlybig\\test"
    pygame.init()
    screen_size = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Random Image Placement")
    
    images = load_images_from_folder(TRANS_IMAGES_DIR)
    if not images:
        print("No images found in the specified directory.")
        return
    
    # Choose blend mode here
    blend_modes = {
        'add': pygame.BLEND_RGBA_ADD,
        'subtract': pygame.BLEND_RGBA_SUB,
        'multiply': pygame.BLEND_RGBA_MULT,
        'minimum': pygame.BLEND_RGBA_MIN,
        'maximum': pygame.BLEND_RGBA_MAX
    }
    selected_blend_mode = blend_modes['multiply']  # Change this to try different modes
    
    display_images(screen, images, blend_mode=selected_blend_mode)
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
